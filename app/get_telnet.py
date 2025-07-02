import telnetlib
import time
import re
import argparse
import os
from dotenv import load_dotenv
from .utils import insert_into_db_olt_customer_mac
from .enums import BDCOM_EPON, BDCOM_GPON, CDATA_GPON, VSOL_EPON, VSOL_GPON
from .constants import telnet_commands
from .parsers.telnet_parsers import (
    parse_cdata_gpon,
    parse_vsol_gpon,
    parse_vsol_epon,
    parse_bdcom_epon,
    parse_bdcom_gpon,
)

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_sid = os.getenv("DB_SID")


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

    if VENDOR not in telnet_commands:
        print(f"[-] Vendor '{VENDOR}' not supported.")
        print(f"[-] Supported vendors are: {', '.join(telnet_commands.keys())}")
        return

    commands = telnet_commands[VENDOR]
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
