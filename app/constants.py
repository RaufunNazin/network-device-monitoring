from ..enums import MAC, OPERATION_STATUS, ADMIN_STATUS, DISTANCE, UP_SINCE, VENDOR, MODEL, SERIAL_NO, POWER, DESC, CDATA_EPON, CDATA_GPON, VSOL_EPON, VSOL_GPON, BDCOM_EPON, BDCOM_GPON

supported_brands = {
    "CDATA-EPON": CDATA_EPON,
    "CDATA-GPON": CDATA_GPON,
    "VSOL-EPON": VSOL_EPON,
    "VSOL-GPON": VSOL_GPON,
}

branches = {
  "MAC": MAC,
  "OPERATION_STATUS": OPERATION_STATUS,
  "ADMIN_STATUS": ADMIN_STATUS,
  "DISTANCE": DISTANCE,
  "UP_SINCE": UP_SINCE,
  "VENDOR": VENDOR,
  "MODEL": MODEL,
  "SERIAL_NO": SERIAL_NO,
  "POWER": POWER,
  "DESC": DESC,
}

mib_map = {
  'DEFAULT': ['IF-MIB', 'SNMPv2-MIB', 'NMS-SMI', 'RFC1155-SMI', 'RFC1213-MIB'],
  CDATA_EPON: ['NSCRTV-FTTX-EPON-MIB'],
  CDATA_GPON: ['NSCRTV-FTTX-GPON-MIB'],
  VSOL_EPON: ['V1600D'],
  VSOL_GPON: ['V1600G'],
  BDCOM_EPON: ['NMS-SMI', 'RFC1155-SMI', 'RFC1213-MIB', 'NMS-EPON-ONU', 'NMS-EPON-LLID'],
  BDCOM_GPON: ['NMS-SMI', 'RFC1155-SMI', 'RFC1213-MIB', 'NMS-GPON-MIB'],
}

telnet_commands = {
  CDATA_GPON: {
    "enable": "enable",
    "config": "config",
    "show_mac": "show mac-address all",
    "pagination_text": "--More ( Press 'Q' to quit )--"
  },
  VSOL_EPON: {
    "enable": "enable",
    "config": "config",
    "show_mac": "show mac-address all",
    "pagination_text": "--More--"
  },
  VSOL_GPON: {
    "enable": "enable",
    "config": "configure terminal",
    "show_mac": "show mac address-table pon",
    "pagination_text": "--More--"
  }
}