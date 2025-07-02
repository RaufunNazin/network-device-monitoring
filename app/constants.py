from .enums import (
    MAC,
    OPERATION_STATUS,
    ADMIN_STATUS,
    DISTANCE,
    UP_SINCE,
    VENDOR,
    MODEL,
    SERIAL_NO,
    POWER,
    DESC,
    CDATA_EPON,
    CDATA_GPON,
    VSOL_EPON,
    VSOL_GPON,
    BDCOM_EPON,
    BDCOM_GPON,
)

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
supported_brands = {
    CDATA_EPON: CDATA_EPON,
    CDATA_GPON: CDATA_GPON,
    VSOL_EPON: VSOL_EPON,
    VSOL_GPON: VSOL_GPON,
    BDCOM_EPON: BDCOM_EPON,
    BDCOM_GPON: BDCOM_GPON,
}

mib_map = {
    "DEFAULT": [
        "IF-MIB",
        "SNMPv2-MIB",
        "NMS-SMI",
        "RFC1155-SMI",
        "RFC1213-MIB",
        "SNMPv2-SMI",
    ],
    CDATA_EPON: ["NSCRTV-FTTX-EPON-MIB"],
    CDATA_GPON: ["NSCRTV-FTTX-GPON-MIB"],
    VSOL_EPON: ["V1600D"],
    VSOL_GPON: ["V1600G", "V1600D"],
    BDCOM_EPON: [
        "NMS-SMI",
        "RFC1155-SMI",
        "RFC1213-MIB",
        "NMS-EPON-ONU",
        "NMS-EPON-LLID",
    ],
    BDCOM_GPON: ["NMS-SMI", "RFC1155-SMI", "RFC1213-MIB", "NMS-GPON-MIB"],
}

telnet_commands = {
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
