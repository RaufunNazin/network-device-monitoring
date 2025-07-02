from enums import (
    BDCOM_EPON,
    BDCOM_GPON,
    CDATA_EPON,
    CDATA_GPON,
    OPERATION_STATUS_DB,
    VSOL_EPON,
    VSOL_GPON,
)
import re
from datetime import datetime, timedelta


def _parse_mac(raw_value: str, brand: str) -> str | None:
    """
    Parses a MAC address string, formatting it with colons.

    It handles two cases:
    1. For VSOL_EPON, it assumes the MAC is already formatted.
    2. For other brands, it formats a raw hex string (e.g., "AA BB CC 11 22 33")
       into a standard format (e.g., "AA:BB:CC:11:22:33").

    Args:
        raw_value: The raw MAC address string.
        brand: The device brand to determine parsing logic.

    Returns:
        A formatted, uppercase MAC address string, or None if input is invalid.
    """
    if not isinstance(raw_value, str) or not raw_value.strip():
        return None

    try:
        if brand == VSOL_EPON:
            # Assumes EPON provides a pre-formatted or simple MAC string
            parsed_value = raw_value.strip()
        elif brand == CDATA_EPON:
            # Handles CDATA format like "A2 4F 04 20 05 B0"
            # Just replace spaces with colons
            parsed_value = raw_value.strip().replace(" ", ":")
        elif brand == CDATA_GPON:
            parsed_value = ":".join(raw_value.replace(":", " ").split()[:6]).upper()
        elif brand == BDCOM_EPON:
            parsed_value = raw_value.strip().upper()
        else:
            # For other brands, format a raw hex string
            clean_mac = raw_value.replace(":", "").replace(" ", "").strip()
            # Validate that the cleaned string is a 12-character hex value
            if len(clean_mac) != 12 or not all(
                c in "0123456789abcdefABCDEF" for c in clean_mac
            ):
                return None
            # Insert colons
            parsed_value = ":".join(clean_mac[i : i + 2] for i in range(0, 12, 2))

        return parsed_value.upper()

    except (TypeError, AttributeError):
        # Catch any unexpected errors during string manipulation
        return None


def _parse_power(raw_value: str, brand: str) -> float | None:
    """
    Parses an optical power level from a raw string value based on the device brand.

    - For VSOL_EPON: Extracts dBm value from a string like "0.03 mW (-15.87 dBm)".
    - For VSOL_GPON: Converts the raw string directly to a float (value in dBm).
    - For other brands: Converts the raw string to a float and divides by 100
      (assuming the raw value is in hundredths of a dBm).

    Args:
        raw_value: The raw string containing the power level.
        brand: The device brand which determines the parsing logic.

    Returns:
        The power level as a float, or None if parsing fails for any reason.
    """
    # Fail fast: Ensure input is a usable string before proceeding.
    # if not isinstance(raw_value, str) or not raw_value.strip():
    #     return None

    try:
        if brand == VSOL_EPON:
            match = re.search(r"\((.*?)\s*dBm\)", raw_value)
            # Check if the pattern was found before trying to access the group
            if match:
                return float(match.group(1))
            else:
                # Return None if the expected pattern isn't in the string
                return None

        elif brand == VSOL_GPON:
            # Assumes the raw value is a direct float representation of dBm
            return float(raw_value.strip())

        elif brand in [BDCOM_EPON, BDCOM_GPON]:
            return (
                float(raw_value.strip()) / 10.0
            )  # BDCOM EPON and GPON values are in tenths of dBm

        else:
            # For other brands, convert to float THEN divide.
            # Using 100.0 ensures the result is always a float.
            return float(raw_value.strip()) / 100.0

    except (ValueError, TypeError, AttributeError):
        # This single block gracefully handles all potential errors:
        # - ValueError: If float() conversion fails.
        # - TypeError: If an operation is on the wrong type (less likely now).
        # - AttributeError: If re.search returns None and we try to access .group.
        return None


def _parse_up_since(raw_value: str | int, brand: str) -> str | None:
    """
    Parses an uptime value based on the device brand and formats it
    to Oracle-compatible datetime: 'YYYY-MM-DD HH:MM:SS'.

    Args:
        raw_value: The raw uptime string from the device.
        brand: The device brand (e.g., VSOL_EPON, CDATA_EPON, etc.)

    Returns:
        str: Formatted datetime string or None on failure.
    """
    if raw_value in [None, "", "N/A"]:
        return None

    try:
        if brand == VSOL_EPON:
            # Format: '2025/06/24 17:45:21'
            source_datetime = datetime.strptime(raw_value.strip(), "%Y/%m/%d %H:%M:%S")
            return source_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # Handle seconds input like "303751 s" or just "303751"
        seconds = int(str(raw_value).split()[0])
        if seconds == 0:
            return None
        up_since_datetime = datetime.now() - timedelta(seconds=seconds)
        return up_since_datetime.strftime("%Y-%m-%d %H:%M:%S")

    except (ValueError, TypeError):
        return None

    except (ValueError, TypeError):
        # If raw_value is not a valid number or has an unexpected format,
        # return None to indicate a parsing failure.
        return None


def _parse_status(raw_value: int | str, status_type: str) -> int | None:
    """
    Parses a raw status value into a standardized integer code.

    It maps different raw status codes to a consistent internal format based
    on whether it is an operational or administrative status.

    Args:
        raw_value: The raw status code from the device (e.g., 1, 2).
        status_type: The type of status, e.g., OPERATION_STATUS_DB for
                     operational status or another type for admin status.

    Returns:
        The standardized integer status code, or None on failure.
    """
    try:
        status_val = int(raw_value)

        if status_type == OPERATION_STATUS_DB:
            # For operational status: 1 -> 1 (online), others -> 2 (offline)
            parsed_value = 1 if status_val == 1 else 2
        else:
            # For admin status: 2 or 0 -> 3 (disabled), others are passed through
            parsed_value = 3 if status_val in (2, 0) else status_val

        return parsed_value

    except (ValueError, TypeError):
        # Handles cases where raw_value cannot be converted to an integer
        return None


def _parse_descr(pon: int, onu: int, brand: str, slot_id: int | None = None) -> str:
    """
    Generates a description string for an ONU using its location details.

    The final format is "TYPE<frame_id>/<pon_id>:<onu_id>", for example: "GPON0/1:32".

    Args:
        pon: The PON port ID (e.g., 1).
        onu: The ONU ID on the PON port (e.g., 32).
        brand: The device brand string, used to determine the technology type.
        frame_id: The OLT frame or chassis ID. Defaults to 0.

    Returns:
        A formatted description string.
    """
    # Use a case-insensitive check for robustness and provide a default value.
    type_str = "EPON"  # Default if brand is not recognized
    normalized_brand = brand.upper()
    frame_id = 0

    if "GPON" in normalized_brand:
        type_str = "GPON"

    if brand == CDATA_EPON or brand == CDATA_GPON:
        # For CDATA EPON, frame_id is not used in the description
        return f"{type_str}{frame_id}/{slot_id}/{pon}:{onu}"
    # The f-string formatting is already a great choice.
    return f"{type_str}{frame_id}/{pon}:{onu}"


def _parse_hex_string(hex_str: str, mode: str = "ascii") -> str | None:
    """
    Decodes or cleans a hex string based on the required mode.

    Args:
        hex_str: The raw hex string (e.g., "0x...", "ONU(0x...)", or "A24F...").
        mode (str): 'ascii' to decode to text, 'serial' to clean for a serial number.

    Returns:
        A formatted string, or None if parsing fails.
    """
    if not hex_str or not isinstance(hex_str, str):
        return None

    clean_hex = hex_str.strip()
    try:
        # Clean the string to get only the hex part
        if clean_hex.lower().startswith("0x"):
            clean_hex = clean_hex[2:]
        elif "(0x" in clean_hex:
            match = re.search(r"\(0x([a-fA-F0-9]+)\)", clean_hex)
            clean_hex = match.group(1) if match else ""

        if mode == "serial":
            return clean_hex.upper()

        elif mode == "ascii":
            # Ensure hex string has an even number of characters for decoding
            if len(clean_hex) % 2 != 0:
                clean_hex = "0" + clean_hex
            decoded_bytes = bytes.fromhex(clean_hex)
            readable_str = (
                decoded_bytes.rstrip(b"\x00").decode("ascii", errors="replace").strip()
            )
            return readable_str if readable_str else None

    except (ValueError, TypeError):
        return None  # Return None if hex decoding fails

    return None  # Default return


def _parse_hex_to_ascii(input_string: str) -> str | None:
    """
    Converts various string formats (including hex) to a clean ASCII string.

    Handles three primary formats:
    1. A hex string prefixed with '0x' (e.g., "0x4f4e5500" -> "ONU").
    2. A mixed string with a hex part in parentheses (e.g., " ONU(0x204f4e55)" -> "ONU").
    3. A standard hex string with optional colons (e.g., "48:57:41..." -> "HWA...").

    If the input does not match these formats, it's returned as is (e.g., "Huawei").

    Args:
        input_string: The string to process.

    Returns:
        The decoded ASCII string, or the original input if not a recognized hex format.
    """
    if not isinstance(input_string, str):
        return input_string  # Return non-strings as is

    clean_str = input_string.strip()

    # Case 1: Handle mixed string like " ONU(0x204f4e55)"
    # This specifically looks for a hex value inside parentheses.
    if "(0x" in clean_str and clean_str.endswith(")"):
        # Split at the parenthesis and return the part before it, stripped of whitespace.
        return clean_str.split("(0x")[0].strip()

    # Prepare the string for hex decoding
    hex_part = clean_str

    # Case 2: Handle '0x' prefix
    if hex_part.lower().startswith("0x"):
        hex_part = hex_part[2:]  # Remove the '0x'

    # Case 3: Handle colons (original logic)
    if ":" in hex_part:
        hex_part = hex_part.replace(":", "")

    # Now, try to decode the cleaned hex part
    try:
        # Ensure the hex string has an even number of characters for decoding
        if len(hex_part) % 2 != 0:
            raise ValueError("Hex string has an odd length")

        decoded_bytes = bytes.fromhex(hex_part)

        # Decode to text, removing any trailing null bytes and replacing errors
        return decoded_bytes.rstrip(b"\x00").decode("utf-8", errors="replace").strip()

    except ValueError:
        # If decoding fails, it's not a valid hex string. Return the original input.
        return input_string
