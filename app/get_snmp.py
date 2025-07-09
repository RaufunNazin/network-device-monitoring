import asyncio
import argparse
import json
from operator import index
import os
import re
from datetime import datetime
from typing import Dict, Any, Optional

from dotenv import load_dotenv

from .constants import branches, supported_brands
from .enums import (
    ADMIN_STATUS,
    ADMIN_STATUS_DB,
    BDCOM_EPON,
    BDCOM_GPON,
    CDATA_EPON,
    CDATA_GPON,
    DESC,
    DESC_DB,
    DISTANCE,
    DISTANCE_DB,
    IFINDEX2_DB,
    MAC,
    MAC_DB,
    MODEL,
    MODEL_DB,
    ONU,
    ONU_DB,
    ONU_ID,
    OPERATION_STATUS,
    OPERATION_STATUS_DB,
    PON,
    PON_DB,
    PON_ID,
    POWER,
    POWER_DB,
    SERIAL_NO,
    SERIAL_NO_DB,
    SLOT_ID,
    UP_SINCE,
    UP_SINCE_DB,
    VENDOR,
    VENDOR_DB,
    VSOL_EPON,
    VSOL_GPON,
    EPON,
    GPON,
)
from .utils import get_olt_information
from .converters.index_decoders import _index_decoder
from .dictionaries.oid_name_dict import oid_name_dictionary
from .parsers.snmp_parsers import (
    _parse_descr,
    _parse_hex_string,
    _parse_hex_to_ascii,
    _parse_mac,
    _parse_power,
    _parse_status,
    _parse_up_since,
)
from .utils import insert_into_db

load_dotenv()

target_ip = os.getenv("TARGET_IP")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_sid = os.getenv("DB_SID")


def parse_snmp_output(
    data_array, brand, branch, all_oid, desc_data=None, onu_index=None
):
    """
    Parses a list of SNMP string outputs into a structured dictionary of ONUs.
    For BDCOM_EPON, it requires desc_data to map indexes to ports.
    """
        # --- NEW: Special handling for single ONU, single branch queries ---
    if onu_index and not all_oid and branch:
        # This regex is simpler, designed to just grab the value after the colon.
        value_regex = re.compile(r'\=\ [A-Za-z0-9\-]+:\s*"?([^"\n]+)"?')
        
        if not data_array:
            return None # No data returned from SNMP

        # A single-OID query should only have one line in the result.
        raw_line = data_array[0]
        match = value_regex.search(raw_line)

        if not match:
            return None # Could not parse the value from the line

        raw_value = match.group(1).strip()
        parsed_value = None

        try:
            # Use the branch constant to determine which parser to use
            if branch == POWER:
                parsed_value = _parse_power(raw_value, brand)
            elif branch == MAC:
                parsed_value = _parse_mac(raw_value, brand)
            elif branch == OPERATION_STATUS or branch == ADMIN_STATUS:
                parsed_value = _parse_status(raw_value, branch)
            elif branch == UP_SINCE:
                parsed_value = _parse_up_since(raw_value, brand)
            elif branch == SERIAL_NO:
                parsed_value = (
                    _parse_hex_string(raw_value, mode="serial")
                    if brand == CDATA_EPON
                    else _parse_mac(raw_value, brand)
                )
            elif branch == VENDOR or branch == MODEL:
                 if brand in [CDATA_EPON, CDATA_GPON]:
                    parsed_value = _parse_hex_to_ascii(raw_value)
                 else:
                    parsed_value = raw_value
            elif branch == DISTANCE:
                parsed_value = int(raw_value)
            else:
                # Default case for simple string values
                parsed_value = raw_value
        except (ValueError, TypeError) as e:
            print(f"Could not parse single value for branch {branch}: {e}")
            return None

        return parsed_value

    # --- EXISTING LOGIC FOR FULL SNMP WALKS (UNCHANGED) ---
    onus = {}
    # Regex updated to handle OID keys with hyphens or dots (e.g., 'IF-MIB::ifName')
    line_regex = re.compile(
        r'::([a-zA-Z0-9]+)\.((?:\d+\.)*\d+)\s*=\s*(?:[a-zA-Z \-0-9]+):\s*"?([^"\n]+)"?'
    )

    branch_map = {
        MAC: (MAC_DB, str),
        SERIAL_NO: (SERIAL_NO_DB, str),
        OPERATION_STATUS: (OPERATION_STATUS_DB, int),
        ADMIN_STATUS: (ADMIN_STATUS_DB, int),
        DISTANCE: (DISTANCE_DB, int),
        UP_SINCE: (UP_SINCE_DB, datetime),
        POWER: (POWER_DB, float),
        VENDOR: (VENDOR_DB, str),
        MODEL: (MODEL_DB, str),
        ONU: (ONU_DB, int),
        PON: (PON_DB, int),
        DESC: (DESC_DB, str),
    }

    # Map OID names to the final DB key and data type for parsing.
    key_map = {
        oid_name_dictionary.get(MAC, {}).get(brand): (MAC_DB, str),
        oid_name_dictionary.get(SERIAL_NO, {}).get(brand): (SERIAL_NO_DB, str),
        oid_name_dictionary.get(OPERATION_STATUS, {}).get(brand): (
            OPERATION_STATUS_DB,
            int,
        ),
        oid_name_dictionary.get(ADMIN_STATUS, {}).get(brand): (ADMIN_STATUS_DB, int),
        oid_name_dictionary.get(DISTANCE, {}).get(brand): (DISTANCE_DB, int),
        oid_name_dictionary.get(UP_SINCE, {}).get(brand): (UP_SINCE_DB, datetime),
        oid_name_dictionary.get(VENDOR, {}).get(brand): (VENDOR_DB, str),
        oid_name_dictionary.get(MODEL, {}).get(brand): (MODEL_DB, str),
        oid_name_dictionary.get(POWER, {}).get(brand): (POWER_DB, float),
        oid_name_dictionary.get(PON, {}).get(brand): (PON_DB, int),
        oid_name_dictionary.get(ONU, {}).get(brand): (ONU_DB, int),
    }
    # Filter out None keys that result from missing OID definitions
    key_map = {k: v for k, v in key_map.items() if k is not None}

    # --- SPECIALIZED PARSING FOR BDCOM_EPON AND GPON ---
    if brand in [BDCOM_EPON, BDCOM_GPON]:
        if not desc_data:
            print(
                "Error: BDCOM_EPON requires description data for index mapping, but none was provided."
            )
            return {}

        # PASS 1: Build the Index-to-Port Map from the separate description data
        index_to_port_onu_map = {}

        for line in desc_data:
            match = line_regex.search(line)
            if not match:
                continue

            _oid_key, index, raw_value = match.groups()
            if (
                (EPON in raw_value or GPON in raw_value)
                and "/" in raw_value
                and ":" in raw_value
            ):
                try:
                    pon_onu_part = raw_value.split("/")[-1]
                    port_onu_key = pon_onu_part.replace(":", ".")
                    index_to_port_onu_map[index] = port_onu_key
                except (ValueError, IndexError):
                    continue

        # PASS 2: Populate ONU Data using the created map
        for line in data_array:
            match = line_regex.search(line)
            if not match:
                continue

            oid_key, index, raw_value = match.groups()

            if index in index_to_port_onu_map:
                port_onu_key = index_to_port_onu_map[index]

                # Ensure the sub-dictionary exists for this ONU
                onus.setdefault(port_onu_key, {})

                # **THE FIX IS HERE:** Get a reference to the ONU's dictionary
                onu_data = onus[port_onu_key]

                if oid_key in key_map:
                    target_key, value_type = key_map[oid_key]
                    try:
                        # This complete if/elif/else chain handles all data types
                        if target_key in [OPERATION_STATUS_DB, ADMIN_STATUS_DB]:
                            onu_data[target_key] = _parse_status(raw_value, target_key)
                        elif target_key == MAC_DB:
                            onu_data[target_key] = _parse_mac(raw_value, brand)
                        elif target_key == POWER_DB:
                            onu_data[target_key] = _parse_power(raw_value, brand)
                        elif target_key == UP_SINCE_DB:
                            onu_data[target_key] = _parse_up_since(raw_value, brand)
                        elif target_key == SERIAL_NO_DB and brand == BDCOM_EPON:
                            # Per your logs, Serial for BDCOM is parsed like a MAC
                            onu_data[target_key] = _parse_mac(raw_value, brand)
                        else:
                            # This handles other types like DISTANCE, VENDOR etc.
                            if callable(value_type):
                                onu_data[target_key] = value_type(raw_value.strip())

                    except (ValueError, TypeError) as e:
                        print(
                            f"Could not process value for BDCOM key '{target_key}' on ONU {port_onu_key}: {e}"
                        )

                if all_oid:
                    onu_data[IFINDEX2_DB] = index

        # PASS 3: Generate derived data like PON, ONU, and Description
        for key, onu_data in onus.items():
            # This check is good practice to avoid errors on malformed keys
            if "." not in key:
                continue
            try:
                # Split the key '7.12' into pon=7, onu=12
                pon_id, onu_id = map(int, key.split("."))
                onu_data[PON_DB] = pon_id
                onu_data[ONU_DB] = onu_id
                onu_data[DESC_DB] = _parse_descr(pon_id, onu_id, brand)
            except (ValueError, TypeError) as e:
                print(f"Could not decode PON/ONU for key '{key}': {e}")

        # --- Final cleanup and sorting ---
        for onu_data in onus.values():
            onu_data.pop(ADMIN_STATUS_DB, None)

        # Return early after BDCOM processing is complete
        try:
            sorted_items = sorted(
                onus.items(), key=lambda item: tuple(map(int, item[0].split(".")))
            )
            return dict(sorted_items)
        except (ValueError, TypeError):
            return onus

    # --- GENERIC PARSING FOR ALL OTHER BRANDS (VSOL, CDATA, etc.) ---
    mac_oid_name, port_oid_name = (None, None)
    if brand == VSOL_GPON:
        mac_oid_name = oid_name_dictionary.get(MAC, {}).get(brand)
        port_oid_name = "macFlappingCurrentPort"

    # PASS 1: Parse all fundamental data
    for line in data_array:
        match = line_regex.search(line)
        if not match:
            continue

        oid_key, full_index, raw_value = match.groups()

        if brand == VSOL_GPON and oid_key in [mac_oid_name, port_oid_name]:
            continue

        try:
            if brand == CDATA_EPON or brand == CDATA_GPON:
                device_id = int(full_index.split(".")[0])
                decoded_ids = _index_decoder(device_id, brand)
                onu_key = f"{decoded_ids[SLOT_ID]}.{decoded_ids[PON_ID]}.{decoded_ids[ONU_ID]}"
                onu_data = onus.setdefault(onu_key, {})
                if all_oid:
                    onu_data.update(
                        {PON_DB: decoded_ids[PON_ID], ONU_DB: decoded_ids[ONU_ID]}
                    )
            else:  # VSOL
                index_parts = full_index.split(".")
                if len(index_parts) >= 2:
                    # Create a consistent 'pon.onu' key, e.g., "3.39"
                    onu_key = f"{index_parts[-2]}.{index_parts[-1]}"
                else:
                    onu_key = full_index  # Fallback for unexpected formats

                if (
                    brand == VSOL_GPON
                    and (all_oid or branch == MAC)
                    and "." not in onu_key
                ):
                    continue
                onu_data = onus.setdefault(onu_key, {})

            if all_oid:
                onu_data[IFINDEX2_DB] = full_index
        except (ValueError, KeyError) as e:
            print(f"Could not decode index for line '{line}': {e}")
            continue

        if oid_key in key_map:
            target_key, value_type = key_map[oid_key]
            try:
                if target_key in [OPERATION_STATUS_DB, ADMIN_STATUS_DB]:
                    onu_data[target_key] = _parse_status(raw_value, target_key)
                elif target_key == MAC_DB:
                    onu_data[target_key] = _parse_mac(raw_value, brand)
                elif target_key == POWER_DB:
                    onu_data[target_key] = _parse_power(raw_value, brand)
                elif target_key == UP_SINCE_DB:
                    onu_data[target_key] = _parse_up_since(raw_value, brand)
                elif target_key == SERIAL_NO_DB:
                    onu_data[target_key] = (
                        _parse_hex_string(raw_value, mode="serial")
                        if brand == CDATA_EPON
                        else _parse_mac(raw_value, brand)
                    )
                elif target_key in [VENDOR_DB, MODEL_DB] and brand in [
                    CDATA_EPON,
                    CDATA_GPON,
                ]:
                    onu_data[target_key] = _parse_hex_to_ascii(raw_value)
                else:
                    if callable(value_type):
                        onu_data[target_key] = value_type(raw_value.strip())
            except (ValueError, TypeError) as e:
                print(
                    f"Could not process value for key '{target_key}' on ONU {onu_key}: {e}"
                )

    # PASS 2: Generate derived data
    if all_oid or branch == DESC:
        if brand in [CDATA_EPON, CDATA_GPON]:
            for key, onu_data in onus.items():
                slot_id, pon_id, onu_id = map(int, key.split("."))
                onu_data[DESC_DB] = _parse_descr(pon_id, onu_id, brand, slot_id)
        else:
            for onu_data in onus.values():
                pon_id, onu_id = onu_data.get(PON_DB, 0), onu_data.get(ONU_DB, 0)
                onu_data[DESC_DB] = _parse_descr(pon_id, onu_id, brand)

    # PASS 3: VSOL-GPON MAC address mapping
    if (all_oid or branch == MAC) and brand == VSOL_GPON:
        index_to_mac_map, index_to_port_onu_map = {}, {}
        for line in data_array:
            match = line_regex.search(line)
            if not match:
                continue
            oid_key, index, raw_value = match.groups()
            if oid_key == mac_oid_name:
                index_to_mac_map[index] = _parse_mac(raw_value, brand)
            elif oid_key == port_oid_name:
                index_to_port_onu_map[index] = raw_value.strip().replace(":", ".")
        for index, port_onu_key in index_to_port_onu_map.items():
            if index in index_to_mac_map and port_onu_key in onus:
                onus[port_onu_key][MAC_DB] = index_to_mac_map[index]

    # --- Final cleanup and sorting ---
    for onu_data in onus.values():
        onu_data.pop(ADMIN_STATUS_DB, None)

    try:
        sorted_items = sorted(
            onus.items(), key=lambda item: tuple(map(int, item[0].split(".")))
        )
        return dict(sorted_items)
    except (ValueError, TypeError):
        return onus


# --- Core Reusable Function for API ---


async def retrieve_olt_data(
    target_ip: str,
    community_string: str,
    brand: str,
    branch: str,
    port: int = 161,
    version: int = 0,
    retries: int = 3,
    timeout: int = 3,
    onu_index_str: Optional[str] = None,
    all_oid: bool = False,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """
    Retrieves, parses, and optionally stores OLT information via SNMP.

    This function is self-contained and can be imported and called from an API.

    Args:
        target_ip: The IP address or hostname of the OLT.
        community_string: The SNMP community string for read access.
        brand: The brand of the OLT (must be in `supported_brands`).
        port: The SNMP port.
        version: The SNMP version (0 for v1, 1 for v2c).
        retries: The number of SNMP retries.
        timeout: The SNMP timeout in seconds.
        branch: The specific OID branch to query.
        onu_index_str: A specific interface index string to query.
        all_oid: If True, query all OID branches for the brand.
        dry_run: If True, data is processed but not inserted into the database.

    Returns:
        A dictionary containing the parsed ONU data.
    """
    selected_branch_constant = branches.get(branch) if branch else None
    if branch and not selected_branch_constant:
        raise ValueError(f"Error: Invalid branch name '{branch}'.")

    print(f"Querying branch '{branch or 'ALL'}' for brand '{brand}' on {target_ip}")

    # --- Main execution logic ---
    result = await get_olt_information(
        target_ip=target_ip,
        community_string=community_string,
        port=port,
        version=version,
        retries=retries,
        timeout=timeout,
        branch=selected_branch_constant,
        brand=brand,
        onu_index_str=onu_index_str,
        all_oid=all_oid,
    )

    # Specific logic for brands that require an extra query for descriptions
    descrs = None
    if brand in [BDCOM_EPON, BDCOM_GPON]:
        print("BDCOM brand detected, fetching interface descriptions for mapping...")
        descrs = await get_olt_information(
            target_ip=target_ip,
            community_string=community_string,
            port=port,
            version=version,
            retries=retries,
            timeout=timeout,
            branch=DESC,
            brand=brand,
            onu_index_str=onu_index_str,
            all_oid=False,
        )

    processed_data = parse_snmp_output(
        result,
        brand,
        selected_branch_constant,
        all_oid,
        desc_data=descrs,
        onu_index=onu_index_str,
    )

    if not dry_run:
        success = insert_into_db(
            processed_data, target_ip, db_host, db_port, db_user, db_pass, db_sid
        )

    return processed_data, success if not dry_run else None


# --- Command-Line Interface (CLI) Execution ---


async def main():
    """Parses command-line arguments and runs the OLT data retrieval."""
    parser = argparse.ArgumentParser(description="SNMP OLT Information Retriever")
    parser.add_argument("-i", required=True, help="Target OLT IP address or hostname")
    parser.add_argument("-c", required=True, help="SNMP community string")
    parser.add_argument("-p", type=int, default=161, help="SNMP port (default: 161)")
    parser.add_argument(
        "-bc", choices=list(branches.keys()), help="OID branch to query"
    )
    parser.add_argument(
        "-bd", required=True, choices=list(supported_brands.keys()), help="Brand name"
    )
    parser.add_argument(
        "-v",
        type=int,
        default=0,
        choices=[0, 1],
        help="SNMP version (0 for v1, 1 for v2c; default: 0)",
    )
    parser.add_argument("-r", type=int, default=3, help="SNMP retries (default: 3)")
    parser.add_argument(
        "-t", type=int, default=3, help="SNMP timeout in seconds (default: 3)"
    )
    parser.add_argument(
        "-idx", type=str, default=None, help="Specific interface index string to query"
    )
    parser.add_argument(
        "-s", type=str, default=None, help="Specify filename to store output"
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Parse data but do not insert into database",
    )
    parser.add_argument(
        "-all", action="store_true", help="If set, all OIDs will be queried"
    )

    args = parser.parse_args()

    try:
        # Call the core, reusable function with arguments from the command line
        final_data, success = await retrieve_olt_data(
            target_ip=args.i,
            community_string=args.c,
            brand=args.bd,
            port=args.p,
            version=args.v,
            retries=args.r,
            timeout=args.t,
            branch=args.bc,
            onu_index_str=args.idx,
            all_oid=args.all,
            dry_run=args.dry_run,
        )

        if success is not None:
            if success:
                print("Data successfully inserted into the database.")
            else:
                print("Data insertion failed or no data to insert.")

        # Custom serializer for datetime objects
        def custom_serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()  # Convert datetime to ISO format string
            raise TypeError(f"Type {type(obj)} not serializable")

        # Handle the output based on CLI flags
        output_json = json.dumps(final_data, indent=4, default=custom_serializer)

        if args.s:
            try:
                with open(args.s, "w") as f:
                    f.write(output_json)
                print(f"Output successfully stored in {args.s}")
            except IOError as e:
                print(f"Error writing to file {args.s}: {e}")
        else:
            print("\n--- Parsed ONU Data ---")
            if not final_data:
                print("No ONU entries found.")
            else:
                print(output_json)

    except (ValueError, TypeError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
