from converters.index_decoders import decode_cdata_epon, decode_cdata_gpon
from ..enums import CDATA_EPON, CDATA_GPON, HEX_STRING, GAUGE, INTEGER, STRING, COUNTER, NULL, SLOT_ID, PON_ID, ONU_ID, EPON_LOWER, GPON_LOWER, CDATA, VSOL, UP_SINCE, VENDOR, POWER, VSOL_GPON
from datetime import datetime, timedelta
from ..utils import format_mac
from dictionaries.oid_name_dict import oid_name_dictionary

def process_snmp_data(snmp_output_lines, brand):
    """
    Processes SNMP output lines to extract and structure data based on the OLT brand and type.

    Args:
        snmp_output_lines (list): A list of strings, where each string is an SNMP output line.
                                  Example format: "MIB-NAME::objectName.index... = ValueType: ValueString"
        brand (str): The brand and type of OLT, e.g., "CDATA-EPON", "CDATA-GPON", "VSOL-GPON".

    Returns:
        list: An array of objects (list of dictionaries).
              Example: [{ "onuMacAddress": { "logical_id1": "mac_val1", ... } },
                        { "onuReceivedOpticalPower": { "logical_id2": power_val2, ... } }]
    """
    processed_data_map = {}

    try:
        vendor_name, olt_technology = brand.split('-', 1)
        olt_tech_lower = olt_technology.lower()
    except ValueError:
        print(f"Warning: Invalid brand format '{brand}'. Expected format 'VENDOR-TECHNOLOGY'.")
        return []

    for line in snmp_output_lines:
        try:
            parts = line.split(" = ", 1)
            if len(parts) != 2:
                print(f"Warning: Skipping malformed line (no ' = ' separator): {line}")
                continue
            
            oid_full_str, value_full_str = parts
            oid_components = oid_full_str.split('.')
            if not oid_components:
                print(f"Warning: Skipping line with invalid OID format (empty components after split by '.'): {line}")
                continue

            oid_key_full_name = oid_components[0]
            oid_key = oid_key_full_name
            if "::" in oid_key_full_name:
                oid_key = oid_key_full_name.split("::", 1)[1]

            value_type_indicator = None
            raw_value_str = value_full_str

            if ": " in value_full_str:
                value_parts = value_full_str.split(": ", 1)
                if len(value_parts) == 2:
                    value_type_indicator = value_parts[0].strip()
                    raw_value_str = value_parts[1].strip()
                else:
                    print(f"Warning: Malformed value string part in line: {line}. Treating as raw.")
                    value_type_indicator = STRING
                    raw_value_str = value_full_str.strip()
            elif value_full_str == "":
                value_type_indicator = NULL
                raw_value_str = ""
            else:
                value_type_indicator = STRING
                raw_value_str = value_full_str.strip()


            onu_string = None
            if vendor_name.upper() == CDATA:
                if len(oid_components) < 2 or not oid_components[1].isdigit():
                    print(f"Warning: Could not extract valid numeric device ID for CDATA from OID '{oid_full_str}' in line: {line}")
                    continue
                device_id_full = '.'.join(oid_components[1:])
                device_id_str = oid_components[1]
                device_id_int = int(device_id_str)
                
                decoded_indices = None
                if olt_tech_lower == EPON_LOWER:
                    decoded_indices = decode_cdata_epon(device_id_int)
                elif olt_tech_lower == GPON_LOWER:
                    decoded_indices = decode_cdata_gpon(device_id_int)
                else:
                    print(f"Warning: Unknown OLT technology '{olt_tech_lower}' for CDATA brand in line: {line}")
                    continue
                
                slot_id = decoded_indices[SLOT_ID]
                pon_id = decoded_indices[PON_ID]
                onu_id = decoded_indices[ONU_ID]
                onu_string = f"{slot_id}.{pon_id}.{onu_id}->{device_id_full}"

            elif vendor_name.upper() == VSOL:
                onu_string = '.'.join(oid_components[1:])
                if not onu_string:
                    print(f"Warning: Could not extract valid device ID for VSOL from OID '{oid_full_str}' in line: {line}")
                    continue
            else:
                print(f"Warning: Unknown vendor '{vendor_name}' in brand '{brand}'. Skipping line: {line}")
                continue

            parsed_value = None
            if vendor_name.upper() == CDATA:
                if oid_name_dictionary[POWER][CDATA_EPON] in oid_key:
                    try:
                        parsed_value = float(raw_value_str) / 100.0
                    except ValueError:
                        print(f"Warning: CDATA - Could not parse power value '{raw_value_str}' as float for line: {line}")
                        parsed_value = raw_value_str
                elif oid_name_dictionary[UP_SINCE][CDATA_EPON] in oid_key:
                    try:
                        current_time = datetime.now()
                        parsed_value = (current_time - timedelta(seconds=int(raw_value_str))).replace(microsecond=0)
                    except ValueError:
                        print(f"Warning: CDATA - Could not parse time value '{raw_value_str}' as int for line: {line}")
                        parsed_value = raw_value_str
                elif oid_name_dictionary[VENDOR][CDATA_EPON] in oid_key or oid_name_dictionary[VENDOR][CDATA_GPON] in oid_key:
                    cleaned = raw_value_str.strip().strip('"')

                    if " " in cleaned and ":" not in cleaned:
                        cleaned = cleaned.replace(" ", ":")

                    if not cleaned or all(part == "00" for part in cleaned.split(":")):
                        parsed_value = "N/A"

                    elif ":" not in cleaned:
                        parsed_value = cleaned

                    else:
                        try:
                            hex_clean = cleaned.replace(":", "")
                            byte_data = bytes.fromhex(hex_clean)
                            decoded = byte_data.decode("ascii", errors="ignore").strip("\x00").strip()
                            parsed_value = decoded if decoded else "N/A"
                        except Exception:
                            parsed_value = "N/A"

            elif vendor_name.upper() == VSOL:
                if oid_name_dictionary[POWER][VSOL_GPON] in oid_key:
                    try:
                        parsed_value = float(raw_value_str.strip('"'))
                    except ValueError:
                        print(f"Warning: VSOL - Could not parse power value '{raw_value_str}' as float for line: {line}")
                        parsed_value = raw_value_str
                elif oid_name_dictionary[UP_SINCE][VSOL_GPON] in oid_key:
                    try:
                        current_time = datetime.now()
                        cleaned_value = raw_value_str.strip('"')
                        if cleaned_value.upper() == "N/A":
                            parsed_value = None
                        else:
                            time_part = cleaned_value.split(' ')[0]
                            seconds = int(time_part)
                            parsed_value = (current_time - timedelta(seconds=seconds)).replace(microsecond=0)
                    except (ValueError, IndexError) as e:
                        print(f"Warning: VSOL - Could not parse time value '{raw_value_str}' for line: {line} (Error: {e})")
                        parsed_value = raw_value_str
            
            if parsed_value is None:
                if value_type_indicator == HEX_STRING:
                    parsed_value = format_mac(raw_value_str)
                elif value_type_indicator and (value_type_indicator.startswith(INTEGER) or \
                                              value_type_indicator.startswith(GAUGE) or \
                                              value_type_indicator.startswith(COUNTER)):
                    try:
                        parsed_value = int(raw_value_str)
                    except ValueError:
                        parsed_value = raw_value_str
                elif value_type_indicator == STRING:
                    parsed_value = raw_value_str.strip('"')
                elif value_type_indicator == NULL:
                    parsed_value = None
                else:
                    parsed_value = raw_value_str.strip('"')

            if oid_key not in processed_data_map:
                processed_data_map[oid_key] = {}
            if onu_string:
                processed_data_map[oid_key][onu_string] = parsed_value

        except ValueError as ve:
            print(f"Warning: ValueError processing line '{line}': {ve}")
        except Exception as e:
            print(f"Warning: Generic error processing line '{line}': {e}")

    result_array = []
    for key, value_map in processed_data_map.items():
        result_array.append({key: value_map})
        
    return result_array