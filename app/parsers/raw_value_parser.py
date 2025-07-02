from ..enums import OCTETSTRING, HEX_STRING, OID, OID_SHORT, GAUGE32, INTEGER, STRING, COUNTER32, COUNTER64, TIMETICKS, IPADDRESS, NULL

def format_raw_values(value, value_type):
    """
    Format the value based on its type
    Args:
        value: The value to format.
        value_type (str): The type of the value (e.g., OCTETSTRING, INTEGER).
    Returns:
        str: The formatted value as a string.
    """
    if value_type == OCTETSTRING:
        # Attempt to decode as a printable ASCII string first
        try:
            # Get raw bytes
            raw_bytes = bytes(value.asNumbers())
            # Check if all bytes are in the printable ASCII range
            if all(32 <= byte <= 126 for byte in raw_bytes):
                decoded_string = raw_bytes.decode("ascii")
                # If the string contains colons, convert it to uppercase
                if ":" in decoded_string:
                    processed_value = decoded_string.upper()
                else:
                    processed_value = decoded_string
                return f'{STRING}: "{processed_value}"'
        except (ValueError, UnicodeDecodeError):
            # This will catch errors if asNumbers() is empty or decoding fails
            pass

        # If it's not a printable string, format it as Hex
        hex_bytes = value.asNumbers()
        if not hex_bytes:
            return '""'

        # Format each byte as a two-digit uppercase hex number and join with colons
        formatted_hex = ":".join(f"{byte:02X}" for byte in hex_bytes)
        return f"{HEX_STRING}: {formatted_hex}"
    elif value_type == OID:
        return f"{OID_SHORT}: {value.prettyPrint()}"
    elif value_type == GAUGE32:
        return f"{GAUGE32}: {value}"
    elif value_type == COUNTER32:
        return f"{COUNTER32}: {value}"
    elif value_type == COUNTER64:
        return f"{Counter64}: {value}"
    elif value_type == TIMETICKS:
        raw_ticks = int(value)
        days = raw_ticks // (24 * 60 * 60 * 100)
        hours = (raw_ticks // (60 * 60 * 100)) % 24
        minutes = (raw_ticks // (60 * 100)) % 60
        seconds = (raw_ticks // 100) % 60
        milliseconds = raw_ticks % 100
        human_readable = (
            f"{days} days, {hours}:{minutes:02}:{seconds:02}.{milliseconds:02}"
        )
        return f"{TIMETICKS}: ({raw_ticks}) {human_readable}"
    elif value_type == IPADDRESS:
        return f"{IPADDRESS}: {value.prettyPrint()}"
    elif value_type == INTEGER:
        return f"{INTEGER}: {value}"
    elif value_type == NULL:
        return '""'
    else:
        return f"{value_type}: {value.prettyPrint()}"