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


def get_paginated_data(tn, command, prompt, more_prompt):
    """
    Sends a command, handles pagination for any vendor, and waits for the prompt to return.
    This function intelligently handles whether the prompts are strings or bytes.
    """
    print(f"[+] Sending command: {command}")
    flush_extra_output(tn)
    time.sleep(1)
    tn.write(command.encode("ascii") + b"\n")
    output = b""

    # Intelligently handle both string and bytes prompts
    more_prompt_bytes = (
        more_prompt if isinstance(more_prompt, bytes) else more_prompt.encode("ascii")
    )
    prompt_bytes = prompt if isinstance(prompt, bytes) else prompt.encode("ascii")

    while True:
        # Use tn.expect() to wait for either the "more" prompt or the final command prompt
        index, _, chunk = tn.expect(
            [more_prompt_bytes, prompt_bytes], timeout=15
        )  # Increased timeout for reliability
        output += chunk

        if index == 0:  # Matched the "more" prompt
            print("[+] More data found, sending SPACE")
            tn.write(b" ")
            time.sleep(0.5)
        elif index == 1:  # Matched the command prompt
            print("[+] Command finished, prompt detected.")
            break
        else:  # Timeout (index == -1)
            print("[-] Timeout waiting for prompt or more data.")
            # Try to read any remaining data before breaking
            remaining = tn.read_very_eager()
            if remaining:
                output += remaining
            break

    return output.decode("utf-8", errors="ignore")


def get_parser_for_brand(brand):
    """Returns the correct parsing function based on the brand string."""
    if brand == CDATA_GPON:
        return parse_cdata_gpon
    elif brand == VSOL_GPON:
        return parse_vsol_gpon
    elif brand == VSOL_EPON:
        return parse_vsol_epon
    elif brand == BDCOM_EPON:
        return parse_bdcom_epon
    elif brand == BDCOM_GPON:
        return parse_bdcom_gpon
    else:
        raise ValueError(f"Unsupported brand: {brand}")


def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Telnet MAC Address Table Fetcher")
    parser.add_argument("-i", required=True, help="Target device IP address")
    parser.add_argument("-p", type=int, default=23, help="Telnet port (default: 23)")
    parser.add_argument("-u", required=True, help="Username for telnet login")
    parser.add_argument("-ps", required=True, help="Password for telnet login")
    parser.add_argument(
        "-v",
        "--brand",
        required=True,
        help="Brand identifier (e.g., CDATA-GPON, VSOL-EPON)",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Parse data but do not insert into database",
    )
    return parser.parse_args()


def connect_and_login(
    host: str, port: int, username: str, password: str
) -> telnetlib.Telnet:
    """Establishes a Telnet connection and logs in."""
    print(f"[+] Connecting to {host}:{port} ...")
    tn = telnetlib.Telnet(host, port, timeout=10)
    print("[+] Connected.")

    print("[+] Waiting for username prompt...")
    tn.read_until(b"Username:", timeout=5)
    tn.write(username.encode("ascii") + b"\n")

    print("[+] Waiting for password prompt...")
    tn.read_until(b"Password:", timeout=5)
    tn.write(password.encode("ascii") + b"\n")

    time.sleep(2)  # Wait for login to complete
    print("[+] Login sequence sent.")
    return tn


def fetch_mac_address_data(tn: telnetlib.Telnet, commands: dict, password: str) -> str:
    """Navigates through device modes and fetches the MAC address table."""
    # Detect the initial prompt after login
    prompt = detect_prompt(tn)
    print(f"[+] Detected initial prompt: {prompt.decode(errors='ignore')}")
    flush_extra_output(tn)

    print("[+] Entering enable mode...")
    tn.write(commands["enable"].encode("ascii") + b"\n")
    time.sleep(0.5)
    # Handle devices that require a password for enable mode
    if b"Password" in tn.read_very_eager():
        tn.write(password.encode("ascii") + b"\n")
    time.sleep(1)

    prompt = detect_prompt(tn)
    print(f"[+] Detected enable mode prompt: {prompt.decode(errors='ignore')}")
    flush_extra_output(tn)

    print("[+] Entering config mode...")
    tn.write(commands["config"].encode("ascii") + b"\n")
    time.sleep(1)
    prompt = detect_prompt(tn)
    print(f"[+] Detected config mode prompt: {prompt.decode(errors='ignore')}")
    flush_extra_output(tn)

    print("[+] Fetching MAC address table...")
    output = get_paginated_data(
        tn, commands["show_mac"], prompt, commands["pagination_text"]
    )
    return output


def process_and_store_data(output: str, parse_function, host: str, dry_run: bool):
    """Parses the raw data and stores it in the database if not a dry run."""
    parsed_output = parse_function(output)
    print("\n--- Parsed Data ---")
    for entry in parsed_output:
        print(entry)
    print("-------------------\n")

    if not dry_run:
        print("[+] Inserting data into the database...")
        insert_into_db_olt_customer_mac(
            parsed_output, host, db_host, db_port, db_user, db_pass, db_sid
        )
        print("[+] Data insertion process completed.")
    else:
        print("[+] Dry run mode: Data will not be inserted into the database.")


def main():
    """Main function to orchestrate the data fetching and processing."""
    args = parse_arguments()
    host = args.i
    brand = args.brand.upper()
    password = args.ps  # Store password for potential re-use in enable mode

    if brand not in telnet_commands:
        print(f"[-] Brand '{brand}' not supported.")
        print(f"[-] Supported brands are: {', '.join(telnet_commands.keys())}")
        return

    commands = telnet_commands[brand]
    parse_function = get_parser_for_brand(brand)
    tn = None

    try:
        tn = connect_and_login(host, args.p, args.u, password)
        raw_output = fetch_mac_address_data(tn, commands, password)
        process_and_store_data(raw_output, parse_function, host, args.dry_run)

    except Exception as e:
        print(f"[-] An error occurred: {e}")
        import traceback

        traceback.print_exc()
    finally:
        if tn:
            tn.close()
            print("[+] Telnet connection closed.")


if __name__ == "__main__":
    main()
