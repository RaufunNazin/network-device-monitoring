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
    decoded_value = value.prettyPrint()
    if not decoded_value:  
      return '""'
    if not decoded_value.startswith("0x") and all(32 <= ord(char) <= 126 for char in decoded_value):
      return f'{STRING}: "{decoded_value}"'
    else:
      hex_value = " ".join([f"{byte:02X}" for byte in value.asNumbers()])
      return f'{HEX_STRING}: {hex_value}'
  elif value_type == OID:
    return f"{OID_SHORT}: {value.prettyPrint()}"
  elif value_type == GAUGE32:
    return f"{GAUGE32}: {value}"
  elif value_type == COUNTER32:
    return f"{COUNTER32}: {value}"
  elif value_type == COUNTER64:
    return f"{COUNTER64}: {value}"
  elif value_type == TIMETICKS:
    raw_ticks = int(value)
    days = raw_ticks // (24 * 60 * 60 * 100)
    hours = (raw_ticks // (60 * 60 * 100)) % 24
    minutes = (raw_ticks // (60 * 100)) % 60
    seconds = (raw_ticks // 100) % 60
    milliseconds = raw_ticks % 100
    human_readable = f"{days} days, {hours}:{minutes:02}:{seconds:02}.{milliseconds:02}"
    return f"{TIMETICKS}: ({raw_ticks}) {human_readable}"
  elif value_type == IPADDRESS:
    return f"{IPADDRESS}: {value.prettyPrint()}"
  elif value_type == INTEGER:
    return f"{INTEGER}: {value}"
  elif value_type == NULL:
    return '""'
  else:
    return f"{value_type}: {value.prettyPrint()}"