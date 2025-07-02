import re

# Regex to remove ANSI escape sequences from terminal output
ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def clean_terminal_text(text):
    """Removes ANSI escape codes and cleans up whitespace."""
    cleaned_lines = []
    for line in text.splitlines():
        line = ansi_escape.sub("", line)
        line = line.replace("\t", " ")
        line = re.sub(r"\s+", " ", line)
        cleaned_lines.append(line.strip())
    return cleaned_lines


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
                    "PORT": port.upper().split("-")[
                        0
                    ],  # The port format is already correct
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
