import telnetlib
import time
import re
import argparse
import os
from dotenv import load_dotenv
from utils import insert_into_db_olt_customer_mac
from enums import BDCOM_EPON, BDCOM_GPON, CDATA_GPON, VSOL_EPON, VSOL_GPON

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_sid = os.getenv("DB_SID")

# Regex to remove ANSI escape sequences from terminal output
ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

# --- Vendor-specific commands and pagination prompts ---
VENDOR_COMMANDS = {
    CDATA_GPON: {
        "enable": "enable",
        "config": "config",
        "show_mac": "show mac-address all",
        "pagination_text": b"--More ( Press 'Q' to quit )--",
    },
    BDCOM_EPON: {
        "enable": "enable",
        "config": "config",
        "show_mac": "show mac address-table",
        "pagination_text": "--More--",
    },
    BDCOM_GPON: {
        "enable": "enable",
        "config": "config",
        "show_mac": "show mac address-table",
        "pagination_text": "--More--",
    },
    VSOL_EPON: {
        "enable": "enable",
        "config": "configure terminal",
        "show_mac": "show mac address-table",
        "pagination_text": "--More--",
    },
    VSOL_GPON: {
        "enable": "enable",
        "config": "configure terminal",
        "show_mac": "show mac address-table pon",
        "pagination_text": "--More--",
    },
}


def detect_prompt(tn):
    """Detects the device's command prompt."""
    tn.write(b"\n")
    time.sleep(1)
    response = tn.read_very_eager()
    lines = response.strip().split(b"\n")
    if lines:
        last_line = lines[-1].strip()
        if b">" in last_line or b"#" in last_line:
            # Split by the last occurrence of > or #
            prompt_char = b">" if b">" in last_line else b"#"
            prompt = last_line.rsplit(prompt_char, 1)[0] + prompt_char
            return prompt
    raise ValueError("Failed to detect device prompt.")


def flush_extra_output(tn):
    """Clears any unread data from the telnet buffer."""
    tn.write(b"\n" * 3)
    time.sleep(0.5)
    _ = tn.read_very_eager()


def clean_terminal_text(text):
    """Removes ANSI escape codes and cleans up whitespace."""
    cleaned_lines = []
    for line in text.splitlines():
        line = ansi_escape.sub("", line)
        line = line.replace("\t", " ")
        line = re.sub(r"\s+", " ", line)
        cleaned_lines.append(line.strip())
    return cleaned_lines


def get_cdata_data(tn, command, prompt, more_prompt):
    """Sends a command, handles pagination, and waits for the prompt to return."""
    print(f"[+] Sending command: {command}")

    flush_extra_output(tn)
    time.sleep(1)

    # Send the command
    tn.write(command.encode("ascii") + b"\n")
    output = b""

    while True:
        chunk = tn.read_until(more_prompt, timeout=5)
        output += chunk
        if more_prompt in chunk:
            print("[+] More data found, sending SPACE")
            tn.write(b" ")
        else:
            # Ensure final prompt is received
            remaining = tn.read_until(prompt, timeout=10)
            output += remaining
            break
    return output.decode("utf-8", errors="ignore")


def get_vsol_data(tn, command, prompt, more_prompt):
    """Sends a command, handles pagination, and waits for the prompt to return."""
    print(f"[+] Sending command: {command}")
    flush_extra_output(tn)
    time.sleep(1)
    tn.write(command.encode("ascii") + b"\n")
    output = b""

    more_prompt_bytes = more_prompt.encode("ascii")
    prompt_bytes = prompt if isinstance(prompt, bytes) else prompt.encode("ascii")

    while True:
        # Read until either the "more" prompt or the command prompt
        index, _, chunk = tn.expect([more_prompt_bytes, prompt_bytes], timeout=10)
        output += chunk

        if index == 0:  # Matched the "more" prompt
            print("[+] More data found, sending SPACE")
            tn.write(b" ")
            time.sleep(0.5)
        elif index == 1:  # Matched the command prompt
            print("[+] Command finished, prompt detected.")
            break
        else:  # Timeout
            print("[-] Timeout waiting for prompt or more data.")
            # Try to read any remaining data before breaking
            remaining = tn.read_very_eager()
            if remaining:
                output += remaining
            break

    return output.decode("utf-8", errors="ignore")


def get_bdcom_data(tn, command, prompt, more_prompt):
    """Sends a command, handles pagination, and waits for the prompt to return."""
    print(f"[+] Sending command: {command}")
    flush_extra_output(tn)
    time.sleep(1)
    tn.write(command.encode("ascii") + b"\n")
    output = b""

    more_prompt_bytes = more_prompt.encode("ascii")
    prompt_bytes = prompt if isinstance(prompt, bytes) else prompt.encode("ascii")

    while True:
        # Read until either the "more" prompt or the command prompt
        index, _, chunk = tn.expect([more_prompt_bytes, prompt_bytes], timeout=10)
        output += chunk

        if index == 0:  # Matched the "more" prompt
            print("[+] More data found, sending SPACE")
            tn.write(b" ")
            time.sleep(0.5)
        elif index == 1:  # Matched the command prompt
            print("[+] Command finished, prompt detected.")
            break
        else:  # Timeout
            print("[-] Timeout waiting for prompt or more data.")
            # Try to read any remaining data before breaking
            remaining = tn.read_very_eager()
            if remaining:
                output += remaining
            break

    return output.decode("utf-8", errors="ignore")


# ----------------- PARSING FUNCTIONS -----------------


def parse_cdata_gpon(text: str) -> list[dict]:
    """
    Parses 'show mac-address all' output from a C-Data GPON OLT,
    returning ONLY the entries found on PON ports.

    Args:
        text: The raw string output from the CLI command.

    Returns:
        A list of dictionaries for each MAC entry found on a PON port.
    """
    mac_entries = []
    lines = text.strip().splitlines()
    data_started = False

    for line in lines:
        if "---" in line:
            data_started = True
            continue
        if not data_started:
            continue

        match = re.match(
            r"^\s*"
            r"((?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2})\s+"  # 1: MAC
            r"(\d+)\s+"  # 2: VLAN
            r"(-|\d+)\s+"  # 3: Sport
            r"(\S+)\s+"  # 4: Port
            r"(-|\d+)\s+"  # 5: Onu
            r"(-|\d+)\s+"  # 6: Gemid
            r"(dynamic|static)",  # 7: MAC-Type
            line,
        )

        if match:
            mac, vlan, sport, port, onu, gemid, mac_type = match.groups()

            # --- NEW: Skip entry if the port is not a PON port ---
            if not port.startswith("pon"):
                continue  # Move to the next line

            # Since we only process PON ports, 'onu' will always be a number.
            # We can directly format the port string.
            formatted_port = f"g{port}:{onu}"

            mac_entries.append(
                {
                    "MAC": mac,
                    "VLAN": int(vlan),
                    "PORT": formatted_port.upper(),
                }
            )

    return mac_entries


def parse_bdcom_epon(text: str) -> list[dict]:
    """
    Parses 'show mac address-table' output from a BDCOM EPON OLT.

    It filters for and returns only the MAC entries learned on EPON ONU ports
    (e.g., 'epon0/1:26').

    Args:
        text: The raw string output from the CLI command.

    Returns:
        A list of dictionaries, where each dictionary represents a MAC entry.
    """
    print("[+] Parsing MAC table for BDCOM_EPON vendor...")
    mac_entries = []
    lines = text.strip().splitlines()
    data_started = False

    # This regex is designed to capture the columns from the BDCOM output.
    # Groups: 1=VLAN, 2=MAC, 3=Type, 4=Port
    line_pattern = re.compile(
        r"^\s*(\d+)\s+"  # 1: Vlan
        r"([0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4})\s+"  # 2: Mac Address
        r"(\S+)\s+"  # 3: Type
        r"(\S+)"  # 4: Ports
    )

    for line in lines:
        # Skip header lines until we see the separator
        if "---" in line:
            data_started = True
            continue
        if not data_started:
            continue

        match = line_pattern.match(line.strip())
        if match:
            vlan, raw_mac, mac_type, port = match.groups()

            # --- This is the crucial filter ---
            # We only care about ports that match the 'epon' format.
            if not port.lower().startswith("epon0/"):
                continue  # Skip this line and move to the next

            # Standardize the MAC address format from xxxx.xxxx.xxxx to XX:XX:XX:XX:XX:XX
            clean_mac = raw_mac.replace(".", "").upper()
            formatted_mac = ":".join(clean_mac[i : i + 2] for i in range(0, 12, 2))

            mac_entries.append(
                {
                    "MAC": formatted_mac,
                    "VLAN": int(vlan),
                    "PORT": port.upper(),  # The port format is already correct
                }
            )

    print(f"[+] Parsed {len(mac_entries)} MAC entries from EPON ports.")
    return mac_entries


def parse_bdcom_gpon(text: str) -> list[dict]:
    """
    Parses 'show mac address-table' output from a BDCOM GPON OLT.

    It filters for and returns only the MAC entries learned on GPON ONU ports
    (e.g., 'gpon0/1:26').

    Args:
        text: The raw string output from the CLI command.

    Returns:
        A list of dictionaries, where each dictionary represents a MAC entry.
    """
    print("[+] Parsing MAC table for BDCOM_GPON vendor...")
    mac_entries = []
    lines = text.strip().splitlines()
    data_started = False

    # This regex is designed to capture the columns from the BDCOM output.
    # Groups: 1=VLAN, 2=MAC, 3=Type, 4=Port
    line_pattern = re.compile(
        r"^\s*(\d+)\s+"  # 1: Vlan
        r"([0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4})\s+"  # 2: Mac Address
        r"(\S+)\s+"  # 3: Type
        r"(\S+)"  # 4: Ports
    )

    for line in lines:
        # Skip header lines until we see the separator
        if "---" in line:
            data_started = True
            continue
        if not data_started:
            continue

        match = line_pattern.match(line.strip())
        if match:
            vlan, raw_mac, mac_type, port = match.groups()

            # --- This is the crucial filter ---
            # We only care about ports that match the 'gpon' format.
            if not port.lower().startswith("gpon0/"):
                continue  # Skip this line and move to the next

            # Standardize the MAC address format from xxxx.xxxx.xxxx to XX:XX:XX:XX:XX:XX
            clean_mac = raw_mac.replace(".", "").upper()
            formatted_mac = ":".join(clean_mac[i : i + 2] for i in range(0, 12, 2))

            mac_entries.append(
                {
                    "MAC": formatted_mac,
                    "VLAN": int(vlan),
                    "PORT": port.upper().split('-')[0],  # The port format is already correct
                }
            )

    print(f"[+] Parsed {len(mac_entries)} MAC entries from GPON ports.")
    return mac_entries


def parse_vsol_gpon(text):
    print("[+] Parsing MAC table for VSOL vendor...")

    lines = clean_terminal_text(text)

    mac_entries = []
    combined_line = ""
    fields_collected = 0

    for line_num, line in enumerate(lines):
        if re.match(r"^[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4}$", line, re.IGNORECASE):
            if combined_line and fields_collected >= 6:
                mac_entries.append(parse_combined_line(combined_line))
            combined_line = line
            fields_collected = 1
        else:
            combined_line += f" {line}"
            fields_collected += 1

    if combined_line and fields_collected >= 6:
        mac_entries.append(parse_combined_line(combined_line))

    print(f"[+] Parsed {len(mac_entries)} MAC entries.")
    return mac_entries


def parse_combined_line(line):
    line_pattern = re.compile(
        r"^([0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})\s+"
        r"(\d+)\s+\w+\s+(\S+)\s+\d+\s+\d+\s+\w+$",
        re.IGNORECASE,
    )

    match = line_pattern.match(line)
    if match:
        raw_mac, vlan, raw_port = match.groups()

        clean_mac = raw_mac.replace(".", "").upper()
        mac = ":".join([clean_mac[i : i + 2] for i in range(0, 12, 2)])

        port = raw_port
        port_match = re.match(r"\w+(\d+)/(\d+):(\d+)", raw_port)
        if port_match:
            port = (
                f"GPON{port_match.group(1)}/{port_match.group(2)}:{port_match.group(3)}"
            )

        return {"MAC": mac, "VLAN": int(vlan), "PORT": port}


def parse_vsol_epon(text):
    """
    Parses MAC table for VSOL EPON devices, specifically targeting
    the format '... EPON0/X:Y ...'
    """
    print("[+] Parsing MAC table for VSOL_EPON vendor (specific format)...")
    mac_entries = []
    lines = text.strip().splitlines()

    # Stricter regex to match only the 'EPON0/1:18' port format.
    # It requires 'EPON' to be followed by digits (no space) and a colon-number suffix.
    data_line_regex = re.compile(
        r"^\s*(?P<vlan>\d+)\s+"
        r"(?P<mac>[0-9a-fA-F]{4}:[0-9a-fA-F]{4}:[0-9a-fA-F]{4})\s+"
        r"Dynamic\s+"
        r"(?P<port>EPON\d+/\d+:\d+)\s+"  # This part is now more specific
        r"Aging"
    )

    for line in lines:
        match = data_line_regex.match(line.strip())
        if match:
            data = match.groupdict()

            # Standardize MAC address format from xxxx:xxxx:xxxx to XX:XX:XX:XX:XX:XX
            raw_mac = data["mac"]
            clean_mac = raw_mac.replace(":", "").upper()
            formatted_mac = ":".join(clean_mac[i : i + 2] for i in range(0, 12, 2))

            port = data["port"]  # PORT is already in the desired format

            mac_entries.append(
                {"MAC": formatted_mac, "VLAN": int(data["vlan"]), "PORT": port}
            )

    print(f"[+] Parsed {len(mac_entries)} MAC entries.")
    return mac_entries


def get_parser_for_vendor(vendor):
    """Returns the correct parsing function based on the vendor string."""
    if vendor == CDATA_GPON:
        return parse_cdata_gpon
    elif vendor == VSOL_GPON:
        return parse_vsol_gpon
    elif vendor == VSOL_EPON:
        return parse_vsol_epon
    elif vendor == BDCOM_EPON:
        return parse_bdcom_epon
    elif vendor == BDCOM_GPON:
        return parse_bdcom_gpon
    else:
        raise ValueError(f"Unsupported vendor: {vendor}")


def main():
    """Main function to connect to the device, fetch, parse, and store data."""
    parser = argparse.ArgumentParser(description="Telnet MAC Address Table Fetcher")
    parser.add_argument("-i", required=True, help="Target device IP address")
    parser.add_argument("-p", type=int, default=23, help="Telnet port (default: 23)")
    parser.add_argument("-u", required=True, help="Username for telnet login")
    parser.add_argument("-ps", required=True, help="Password for telnet login")
    parser.add_argument(
        "-v",
        "--vendor",
        required=True,
        help="Vendor identifier (e.g., CDATA-GPON, VSOL-EPON, VSOL-GPON)",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Parse data but do not insert into database",
    )

    args = parser.parse_args()
    HOST = args.i
    PORT = args.p
    USERNAME = args.u
    PASSWORD = args.ps
    VENDOR = args.vendor.upper()

    if VENDOR not in VENDOR_COMMANDS:
        print(f"[-] Vendor '{VENDOR}' not supported.")
        print(f"[-] Supported vendors are: {', '.join(VENDOR_COMMANDS.keys())}")
        return

    commands = VENDOR_COMMANDS[VENDOR]
    parse_function = get_parser_for_vendor(VENDOR)

    try:
        print(f"[+] Connecting to {HOST}:{PORT} ...")
        tn = telnetlib.Telnet(HOST, PORT, timeout=10)
        print("[+] Connected.")

        print("[+] Waiting for username prompt...")
        tn.read_until(b"Username:", timeout=5)
        tn.write(USERNAME.encode("ascii") + b"\n")

        print("[+] Waiting for password prompt...")
        tn.read_until(b"Password:", timeout=5)
        tn.write(PASSWORD.encode("ascii") + b"\n")

        time.sleep(2)  # Wait for login to process

        # Expecting a prompt like 'VSOL-2-FUTURE>' or 'CDATA#'
        initial_output = tn.read_very_eager().decode("ascii", errors="ignore")
        print(f"Initial login output: {initial_output}")
        prompt = detect_prompt(tn)
        print(f"[+] Detected prompt: {prompt.decode(errors='ignore')}")

        flush_extra_output(tn)

        print("[+] Entering enable mode...")
        tn.write(commands["enable"].encode("ascii") + b"\n")
        time.sleep(0.5)
        # Some devices ask for password again for enable mode
        if "Password" in tn.read_very_eager().decode("ascii", errors="ignore"):
            tn.write(PASSWORD.encode("ascii") + b"\n")
        time.sleep(1)

        # After enable, the prompt character might change (e.g., from > to #)
        prompt = detect_prompt(tn)
        print(f"[+] Detected enable mode prompt: {prompt.decode(errors='ignore')}")
        flush_extra_output(tn)

        print("[+] Entering config mode...")
        tn.write(commands["config"].encode("ascii") + b"\n")
        time.sleep(1)
        # After config, the prompt might change again
        prompt = detect_prompt(tn)
        print(f"[+] Detected config mode prompt: {prompt.decode(errors='ignore')}")
        flush_extra_output(tn)

        if VENDOR == CDATA_GPON:
            output = get_cdata_data(
                tn, commands["show_mac"], prompt, commands["pagination_text"]
            )

        elif VENDOR == VSOL_EPON or VENDOR == VSOL_GPON:
            output = get_vsol_data(
                tn, commands["show_mac"], prompt, commands["pagination_text"]
            )

        elif VENDOR == BDCOM_EPON or VENDOR == BDCOM_GPON:
            output = get_bdcom_data(
                tn, commands["show_mac"], prompt, commands["pagination_text"]
            )

        parsed_output = parse_function(output)
        print("\n--- Parsed Data ---")
        for entry in parsed_output:
            print(entry)
        print("-------------------\n")

        tn.close()
        print("[+] Telnet connection closed.")

        if not args.dry_run:
            # Assuming insert_into_db_olt_customer_mac is defined elsewhere
            # and handles the database connection and insertion.
            print("[+] Inserting data into the database...")
            insert_into_db_olt_customer_mac(
                parsed_output, HOST, db_host, db_port, db_user, db_pass, db_sid
            )
        else:
            print("[+] Dry run mode: Data not inserted into the database.")

    except Exception as e:
        print(f"[-] An error occurred: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()