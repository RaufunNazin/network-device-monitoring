from enums import MAC, OPERATION_STATUS, ADMIN_STATUS, DISTANCE, UP_SINCE, VENDOR, MODEL, SERIAL_NO, POWER, DESC, PON, ONU, CDATA_EPON, CDATA_GPON, VSOL_EPON, VSOL_GPON, BDCOM_EPON, BDCOM_GPON

oid_name_dictionary = {
  MAC: {
    CDATA_EPON: 'onuMacAddress',
    CDATA_GPON: 'onuMacAddress',
    VSOL_EPON: 'onuMacAddr',
    VSOL_GPON: '1.3.6.1.4.1.37950.1.1.5.10.3.2.1.3',
    BDCOM_EPON: 'onuMacAddr',
    BDCOM_GPON: ''
  },
  SERIAL_NO: {
    CDATA_EPON: 'onuSn',
    CDATA_GPON: 'onuSn',
    VSOL_EPON: 'onuID',
    VSOL_GPON: 'gOnuDetailInfoSn',
    BDCOM_EPON: 'onuID',
    BDCOM_GPON: ''
  },
  OPERATION_STATUS: {
    CDATA_EPON: 'onuOperationStatus',
    CDATA_GPON: 'onuOperationStatus',
    VSOL_EPON: 'onuPortBasicLinkStatus',
    VSOL_GPON: 'gOnuDetailInfoOpSta',
    BDCOM_EPON: '',
    BDCOM_GPON: ''
  },
  ADMIN_STATUS: {
    CDATA_EPON: 'onuAdminStatus',
    CDATA_GPON: 'onuAdminStatus',
    VSOL_EPON: 'onuPortBasicAdminStatus',
    VSOL_GPON: 'gOnuStaInfoAdminSta',
    BDCOM_EPON: '',
    BDCOM_GPON: ''
  },
  DISTANCE: {
    CDATA_EPON: 'onuTestDistance',
    CDATA_GPON: 'onuTestDistance',
    VSOL_EPON: 'onuAuthInfoDistance2',
    VSOL_GPON: 'gOnuRttDistance',
    BDCOM_EPON: 'onuDistance',
    BDCOM_GPON: ''
  },
  UP_SINCE: {
    CDATA_EPON: 'onuTimeSinceLastRegister',
    CDATA_GPON: 'onuTimeSinceLastRegister',
    VSOL_EPON: 'onuAuthInfoLastRegTime',
    VSOL_GPON: 'gOnuDetailInfoSysUpTime',
    BDCOM_EPON: 'onuAliveTime',
    BDCOM_GPON: ''
  },
  VENDOR: {
    CDATA_EPON: 'onuVendorId',
    CDATA_GPON: 'onuVendorID',
    VSOL_EPON: 'onuVendorId',
    VSOL_GPON: 'gOnuDetailInfoVendorId',
    BDCOM_EPON: 'onuVendorID',
    BDCOM_GPON: ''
  },
  MODEL: {
    CDATA_EPON: 'onuModelId',
    CDATA_GPON: 'onuModelId',
    VSOL_EPON: 'onuModel',
    VSOL_GPON: 'gOnuModel',
    BDCOM_EPON: '',
    BDCOM_GPON: ''
  },
  POWER: {
    CDATA_EPON: 'onuReceivedOpticalPower',
    CDATA_GPON: 'onuReceivedOpticalPower',
    VSOL_EPON: 'onuRecievepower',
    VSOL_GPON: 'gOnuOpticalInfoRxPwr',
    BDCOM_EPON: 'opModuleRxPower',
    BDCOM_GPON: ''
  },
  DESC: {
    CDATA_EPON: '',
    CDATA_GPON: '',
    VSOL_GPON: 'gOnuDetailInfoOnuDesc',
    BDCOM_EPON: '',
    BDCOM_GPON: ''
  },
  PON: {
    CDATA_EPON: '',
    CDATA_GPON: '',
    VSOL_EPON: '',
    VSOL_GPON: 'gOnuRttPon',
    BDCOM_EPON: '',
    BDCOM_GPON: ''
  },
  ONU: {
    CDATA_EPON: '',
    CDATA_GPON: '',
    VSOL_EPON: '',
    VSOL_GPON: 'gOnuRttOnu',
    BDCOM_EPON: '',
    BDCOM_GPON: ''
  }
}