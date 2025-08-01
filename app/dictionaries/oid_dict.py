from ..enums import (
    HUAWEI_EPON,
    HUAWEI_GPON,
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
    PON,
    ONU,
    CDATA_EPON,
    CDATA_GPON,
    VSOL_EPON,
    VSOL_GPON,
    BDCOM_EPON,
    BDCOM_GPON,
)

oid_dictionary = {
    MAC: {
        CDATA_EPON: "1.3.6.1.4.1.17409.2.3.4.1.1.7",
        CDATA_GPON: "1.3.6.1.4.1.17409.2.8.4.6.1.1.2",
        VSOL_EPON: "1.3.6.1.4.1.37950.1.1.5.12.1.25.1.5",
        VSOL_GPON: "1.3.6.1.4.1.37950.1.1.5.10.3.5.1",
        BDCOM_EPON: "1.3.6.1.4.1.3320.101.10.4.1.1",
        BDCOM_GPON: "",
        HUAWEI_EPON: "",
        HUAWEI_GPON: "",
    },
    SERIAL_NO: {
        CDATA_EPON: "1.3.6.1.4.1.17409.2.3.4.1.1.28",
        CDATA_GPON: "1.3.6.1.4.1.17409.2.8.4.1.1.3",
        VSOL_EPON: "1.3.6.1.4.1.37950.1.1.5.12.2.1.2.1.5",
        VSOL_GPON: "1.3.6.1.4.1.37950.1.1.6.1.1.4.1.5",
        BDCOM_EPON: "1.3.6.1.4.1.3320.101.10.1.1.3",
        BDCOM_GPON: "1.3.6.1.4.1.3320.10.3.1.1.4",
        HUAWEI_EPON: "",
        HUAWEI_GPON: "1.3.6.1.4.1.2011.6.128.1.1.2.46.1.30",
    },
    OPERATION_STATUS: {
        CDATA_EPON: "1.3.6.1.4.1.17409.2.3.4.1.1.8",
        CDATA_GPON: "1.3.6.1.4.1.17409.2.8.4.1.1.7",
        VSOL_EPON: "1.3.6.1.4.1.37950.1.1.5.12.1.25.1.4",
        VSOL_GPON: "1.3.6.1.4.1.37950.1.1.6.1.1.4.1.13",
        BDCOM_EPON: "1.3.6.1.2.1.2.2.1.8",
        BDCOM_GPON: "1.3.6.1.4.1.3320.10.3.1.1.8",
        HUAWEI_EPON: "",
        HUAWEI_GPON: "1.3.6.1.4.1.2011.6.128.1.1.2.46.1.15",
    },
    ADMIN_STATUS: {
        CDATA_EPON: "1.3.6.1.4.1.17409.2.3.4.1.1.9",
        CDATA_GPON: "1.3.6.1.4.1.17409.2.8.4.1.1.8",
        VSOL_EPON: "",
        VSOL_GPON: "1.3.6.1.4.1.37950.1.1.6.1.1.1.1.3",
        BDCOM_EPON: "1.3.6.1.2.1.2.2.1.7",
        BDCOM_GPON: "1.3.6.1.2.1.2.2.1.7",
        HUAWEI_EPON: "",
        HUAWEI_GPON: "",
    },
    DISTANCE: {
        CDATA_EPON: "1.3.6.1.4.1.17409.2.3.4.1.1.15",
        CDATA_GPON: "1.3.6.1.4.1.17409.2.8.4.1.1.9",
        VSOL_EPON: "1.3.6.1.4.1.37950.1.1.5.12.1.25.1.17",
        VSOL_GPON: "1.3.6.1.4.1.37950.1.1.6.1.1.12.1.3",
        BDCOM_EPON: "1.3.6.1.4.1.3320.101.10.1.1.27",
        BDCOM_GPON: "1.3.6.1.4.1.3320.10.3.1.1.33",
        HUAWEI_EPON: "",
        HUAWEI_GPON: "",
    },
    UP_SINCE: {
        CDATA_EPON: "1.3.6.1.4.1.17409.2.3.4.1.1.18",
        CDATA_GPON: "1.3.6.1.4.1.17409.2.8.4.1.1.12",
        VSOL_EPON: "1.3.6.1.4.1.37950.1.1.5.12.1.25.1.18",
        VSOL_GPON: "1.3.6.1.4.1.37950.1.1.6.1.1.4.1.20",
        BDCOM_EPON: "1.3.6.1.4.1.3320.101.10.1.1.80",
        BDCOM_GPON: "1.3.6.1.4.1.3320.10.3.1.1.19",
        HUAWEI_EPON: "",
        HUAWEI_GPON: "",
    },
    VENDOR: {
        CDATA_EPON: "1.3.6.1.4.1.17409.2.3.4.1.1.25",
        CDATA_GPON: "1.3.6.1.4.1.17409.2.8.4.1.1.5",
        VSOL_EPON: "1.3.6.1.4.1.37950.1.1.5.12.2.1.2.1.3",
        VSOL_GPON: "1.3.6.1.4.1.37950.1.1.6.1.1.4.1.3",
        BDCOM_EPON: "1.3.6.1.4.1.3320.101.10.1.1.1",
        BDCOM_GPON: "1.3.6.1.4.1.3320.10.3.1.1.2",
        HUAWEI_EPON: "",
        HUAWEI_GPON: "",
    },
    MODEL: {
        CDATA_EPON: "1.3.6.1.4.1.17409.2.3.4.1.1.26",
        CDATA_GPON: "1.3.6.1.4.1.17409.2.8.4.1.1.6",
        VSOL_EPON: "1.3.6.1.4.1.37950.1.1.5.12.2.1.2.1.4",
        VSOL_GPON: "1.3.6.1.4.1.37950.1.1.6.1.1.2.1.6",
        BDCOM_EPON: "1.3.6.1.4.1.3320.101.10.1.1.2",
        BDCOM_GPON: "1.3.6.1.4.1.3320.10.3.1.1.9",
        HUAWEI_EPON: "",
        HUAWEI_GPON: "",
    },
    POWER: {
        CDATA_EPON: "1.3.6.1.4.1.17409.2.3.4.2.1.4",
        CDATA_GPON: "1.3.6.1.4.1.17409.2.8.4.4.1.4",
        VSOL_EPON: "1.3.6.1.4.1.37950.1.1.5.12.2.1.8.1.7",
        VSOL_GPON: "1.3.6.1.4.1.37950.1.1.6.1.1.3.1.7",
        BDCOM_EPON: "1.3.6.1.4.1.3320.101.10.5.1.5",
        BDCOM_GPON: "1.3.6.1.4.1.3320.10.3.4.1.2",
        HUAWEI_EPON: "",
        HUAWEI_GPON: "1.3.6.1.4.1.2011.6.128.1.1.2.51.1.4",
    },
    DESC: {
        CDATA_EPON: "",
        CDATA_GPON: "",
        # VSOL_EPON: '1.3.6.1.4.1.37950.1.1.5.12.2.1.14.1.2',
        VSOL_EPON: "",
        VSOL_GPON: "1.3.6.1.4.1.37950.1.1.6.1.1.4.1.24",
        BDCOM_EPON: "1.3.6.1.2.1.31.1.1.1.1",
        BDCOM_GPON: "1.3.6.1.2.1.2.2.1.2",
        HUAWEI_EPON: "",
        HUAWEI_GPON: "",
    },
    PON: {
        CDATA_EPON: "",
        CDATA_GPON: "",
        VSOL_EPON: "1.3.6.1.4.1.37950.1.1.5.12.1.25.1.1",
        VSOL_GPON: "1.3.6.1.4.1.37950.1.1.6.1.1.12.1.1",
        BDCOM_EPON: "",
        BDCOM_GPON: "",
        HUAWEI_EPON: "",
        HUAWEI_GPON: "",
    },
    ONU: {
        CDATA_EPON: "",
        CDATA_GPON: "",
        VSOL_EPON: "1.3.6.1.4.1.37950.1.1.5.12.1.25.1.2",
        VSOL_GPON: "1.3.6.1.4.1.37950.1.1.6.1.1.12.1.2",
        BDCOM_EPON: "",
        BDCOM_GPON: "",
        HUAWEI_EPON: "",
        HUAWEI_GPON: "",
    },
}

IFDESCR = "1.3.6.1.2.1.2.2.1.2"
