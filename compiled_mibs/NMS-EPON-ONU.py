# SNMP MIB module (NMS-EPON-ONU) expressed in pysnmp data model.
#
# This Python module is designed to be imported and executed by the
# pysnmp library.
#
# See https://www.pysnmp.com/pysnmp for further information.
#
# Notes
# -----
# ASN.1 source file://app/mibs/NMS-EPON-ONU
# Produced by pysmi-1.6.1 at Wed Jul  2 15:33:46 2025
# On host user-HP platform Linux version 6.11.0-28-generic by user user
# Using Python version 3.12.3 (main, Jun 18 2025, 17:59:45) [GCC 13.3.0]

if 'mibBuilder' not in globals():
    import sys

    sys.stderr.write(__doc__)
    sys.exit(1)

# Import base ASN.1 objects even if this MIB does not use it

(Integer,
 OctetString,
 ObjectIdentifier) = mibBuilder.importSymbols(
    "ASN1",
    "Integer",
    "OctetString",
    "ObjectIdentifier")

(NamedValues,) = mibBuilder.importSymbols(
    "ASN1-ENUMERATION",
    "NamedValues")
(ConstraintsIntersection,
 ConstraintsUnion,
 SingleValueConstraint,
 ValueRangeConstraint,
 ValueSizeConstraint) = mibBuilder.importSymbols(
    "ASN1-REFINEMENT",
    "ConstraintsIntersection",
    "ConstraintsUnion",
    "SingleValueConstraint",
    "ValueRangeConstraint",
    "ValueSizeConstraint")

# Import SMI symbols from the MIBs this MIB depends on

(InetAddressIPv6,) = mibBuilder.importSymbols(
    "INET-ADDRESS-MIB",
    "InetAddressIPv6")

(llidIfIndex,) = mibBuilder.importSymbols(
    "NMS-EPON-LLID",
    "llidIfIndex")

(nmsEPONGroup,) = mibBuilder.importSymbols(
    "NMS-SMI",
    "nmsEPONGroup")

(ModuleCompliance,
 NotificationGroup) = mibBuilder.importSymbols(
    "SNMPv2-CONF",
    "ModuleCompliance",
    "NotificationGroup")

(Bits,
 Bits,
 Counter32,
 Counter64,
 Gauge32,
 Integer32,
 IpAddress,
 ModuleIdentity,
 MibIdentifier,
 NotificationType,
 ObjectIdentity,
 MibScalar,
 MibTable,
 MibTableRow,
 MibTableColumn,
 TimeTicks,
 Unsigned32,
 iso) = mibBuilder.importSymbols(
    "SNMPv2-SMI",
    "Bits",
    "Bits",
    "Counter32",
    "Counter64",
    "Gauge32",
    "Integer32",
    "IpAddress",
    "ModuleIdentity",
    "MibIdentifier",
    "NotificationType",
    "ObjectIdentity",
    "MibScalar",
    "MibTable",
    "MibTableRow",
    "MibTableColumn",
    "TimeTicks",
    "Unsigned32",
    "iso")

(DisplayString,
 MacAddress,
 PhysAddress,
 RowStatus,
 TextualConvention,
 TruthValue) = mibBuilder.importSymbols(
    "SNMPv2-TC",
    "DisplayString",
    "MacAddress",
    "PhysAddress",
    "RowStatus",
    "TextualConvention",
    "TruthValue")


# MODULE-IDENTITY


# Types definitions


# TEXTUAL-CONVENTIONS



# MIB Managed Objects in the order of their OIDs

_NmsEponOnu_ObjectIdentity = ObjectIdentity
nmsEponOnu = _NmsEponOnu_ObjectIdentity(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10)
)
_NmsepononuTable_Object = MibTable
nmsepononuTable = _NmsepononuTable_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1)
)
if mibBuilder.loadTexts:
    nmsepononuTable.setStatus("mandatory")
_NmsEponOnuEntry_Object = MibTableRow
nmsEponOnuEntry = _NmsEponOnuEntry_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1)
)
nmsEponOnuEntry.setIndexNames(
    (0, "NMS-EPON-LLID", "llidIfIndex"),
)
if mibBuilder.loadTexts:
    nmsEponOnuEntry.setStatus("mandatory")
_OnuVendorID_Type = DisplayString
_OnuVendorID_Object = MibTableColumn
onuVendorID = _OnuVendorID_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 1),
    _OnuVendorID_Type()
)
onuVendorID.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuVendorID.setStatus("mandatory")
_OnuModuleID_Type = DisplayString
_OnuModuleID_Object = MibTableColumn
onuModuleID = _OnuModuleID_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 2),
    _OnuModuleID_Type()
)
onuModuleID.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuModuleID.setStatus("mandatory")
_OnuID_Type = PhysAddress
_OnuID_Object = MibTableColumn
onuID = _OnuID_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 3),
    _OnuID_Type()
)
onuID.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuID.setStatus("mandatory")
_OnuHardwareVersion_Type = DisplayString
_OnuHardwareVersion_Object = MibTableColumn
onuHardwareVersion = _OnuHardwareVersion_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 4),
    _OnuHardwareVersion_Type()
)
onuHardwareVersion.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuHardwareVersion.setStatus("mandatory")
_OnuSoftwareVersion_Type = DisplayString
_OnuSoftwareVersion_Object = MibTableColumn
onuSoftwareVersion = _OnuSoftwareVersion_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 5),
    _OnuSoftwareVersion_Type()
)
onuSoftwareVersion.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuSoftwareVersion.setStatus("mandatory")
_OnuFirmwareVersion_Type = DisplayString
_OnuFirmwareVersion_Object = MibTableColumn
onuFirmwareVersion = _OnuFirmwareVersion_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 6),
    _OnuFirmwareVersion_Type()
)
onuFirmwareVersion.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuFirmwareVersion.setStatus("mandatory")
_OnuChipVendorID_Type = DisplayString
_OnuChipVendorID_Object = MibTableColumn
onuChipVendorID = _OnuChipVendorID_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 7),
    _OnuChipVendorID_Type()
)
onuChipVendorID.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuChipVendorID.setStatus("mandatory")
_OnuChipModuleID_Type = DisplayString
_OnuChipModuleID_Object = MibTableColumn
onuChipModuleID = _OnuChipModuleID_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 8),
    _OnuChipModuleID_Type()
)
onuChipModuleID.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuChipModuleID.setStatus("mandatory")
_OnuChipRevision_Type = DisplayString
_OnuChipRevision_Object = MibTableColumn
onuChipRevision = _OnuChipRevision_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 9),
    _OnuChipRevision_Type()
)
onuChipRevision.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuChipRevision.setStatus("mandatory")
_OnuIcVersion_Type = DisplayString
_OnuIcVersion_Object = MibTableColumn
onuIcVersion = _OnuIcVersion_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 10),
    _OnuIcVersion_Type()
)
onuIcVersion.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuIcVersion.setStatus("mandatory")
_OnuGePortCount_Type = Integer32
_OnuGePortCount_Object = MibTableColumn
onuGePortCount = _OnuGePortCount_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 12),
    _OnuGePortCount_Type()
)
onuGePortCount.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuGePortCount.setStatus("mandatory")


class _OnuGePortDistributing_Type(Bits):
    """Custom type onuGePortDistributing based on Bits"""
    namedValues = NamedValues(
        *(("gePort1", 0),
          ("gePort2", 1),
          ("gePort3", 2),
          ("gePort4", 3),
          ("gePort5", 4),
          ("gePort6", 5),
          ("gePort7", 6),
          ("gePort8", 7))
    )

_OnuGePortDistributing_Type.__name__ = "Bits"
_OnuGePortDistributing_Object = MibTableColumn
onuGePortDistributing = _OnuGePortDistributing_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 13),
    _OnuGePortDistributing_Type()
)
onuGePortDistributing.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuGePortDistributing.setStatus("mandatory")
_OnuFePortCount_Type = Integer32
_OnuFePortCount_Object = MibTableColumn
onuFePortCount = _OnuFePortCount_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 14),
    _OnuFePortCount_Type()
)
onuFePortCount.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuFePortCount.setStatus("mandatory")


class _OnuFePortDistributing_Type(Bits):
    """Custom type onuFePortDistributing based on Bits"""
    namedValues = NamedValues(
        *(("fePort1", 0),
          ("fePort2", 1),
          ("fePort3", 2),
          ("fePort4", 3),
          ("fePort5", 4),
          ("fePort6", 5),
          ("fePort7", 6),
          ("fePort8", 7))
    )

_OnuFePortDistributing_Type.__name__ = "Bits"
_OnuFePortDistributing_Object = MibTableColumn
onuFePortDistributing = _OnuFePortDistributing_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 15),
    _OnuFePortDistributing_Type()
)
onuFePortDistributing.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuFePortDistributing.setStatus("mandatory")
_OnuPotsPortCount_Type = Integer32
_OnuPotsPortCount_Object = MibTableColumn
onuPotsPortCount = _OnuPotsPortCount_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 16),
    _OnuPotsPortCount_Type()
)
onuPotsPortCount.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuPotsPortCount.setStatus("mandatory")
_OnuE1PortCount_Type = Integer32
_OnuE1PortCount_Object = MibTableColumn
onuE1PortCount = _OnuE1PortCount_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 17),
    _OnuE1PortCount_Type()
)
onuE1PortCount.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuE1PortCount.setStatus("mandatory")
_OnuUsQueueCount_Type = Integer32
_OnuUsQueueCount_Object = MibTableColumn
onuUsQueueCount = _OnuUsQueueCount_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 18),
    _OnuUsQueueCount_Type()
)
onuUsQueueCount.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuUsQueueCount.setStatus("mandatory")
_OnuUsQueueMaxCount_Type = Integer32
_OnuUsQueueMaxCount_Object = MibTableColumn
onuUsQueueMaxCount = _OnuUsQueueMaxCount_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 19),
    _OnuUsQueueMaxCount_Type()
)
onuUsQueueMaxCount.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuUsQueueMaxCount.setStatus("mandatory")
_OnuDsQueueCount_Type = Integer32
_OnuDsQueueCount_Object = MibTableColumn
onuDsQueueCount = _OnuDsQueueCount_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 20),
    _OnuDsQueueCount_Type()
)
onuDsQueueCount.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuDsQueueCount.setStatus("mandatory")
_OnuDsQueueMaxCount_Type = Integer32
_OnuDsQueueMaxCount_Object = MibTableColumn
onuDsQueueMaxCount = _OnuDsQueueMaxCount_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 21),
    _OnuDsQueueMaxCount_Type()
)
onuDsQueueMaxCount.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuDsQueueMaxCount.setStatus("mandatory")


class _OnuIsBakupBattery_Type(Integer32):
    """Custom type onuIsBakupBattery based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(0,
              1)
        )
    )
    namedValues = NamedValues(
        *(("yes", 0),
          ("no", 1))
    )


_OnuIsBakupBattery_Type.__name__ = "Integer32"
_OnuIsBakupBattery_Object = MibTableColumn
onuIsBakupBattery = _OnuIsBakupBattery_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 22),
    _OnuIsBakupBattery_Type()
)
onuIsBakupBattery.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuIsBakupBattery.setStatus("mandatory")
_OnuADSL2PlusPortCount_Type = Integer32
_OnuADSL2PlusPortCount_Object = MibTableColumn
onuADSL2PlusPortCount = _OnuADSL2PlusPortCount_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 23),
    _OnuADSL2PlusPortCount_Type()
)
onuADSL2PlusPortCount.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuADSL2PlusPortCount.setStatus("mandatory")
_OnuVDSL2PortCount_Type = Integer32
_OnuVDSL2PortCount_Object = MibTableColumn
onuVDSL2PortCount = _OnuVDSL2PortCount_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 24),
    _OnuVDSL2PortCount_Type()
)
onuVDSL2PortCount.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuVDSL2PortCount.setStatus("mandatory")
_OnuLLIDCount_Type = Integer32
_OnuLLIDCount_Object = MibTableColumn
onuLLIDCount = _OnuLLIDCount_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 25),
    _OnuLLIDCount_Type()
)
onuLLIDCount.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuLLIDCount.setStatus("mandatory")


class _OnuStatus_Type(Integer32):
    """Custom type onuStatus based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(0,
              1,
              2,
              3,
              4,
              5)
        )
    )
    namedValues = NamedValues(
        *(("authenticated", 0),
          ("registered", 1),
          ("deregistered", 2),
          ("auto-config", 3),
          ("lost", 4),
          ("standby", 5))
    )


_OnuStatus_Type.__name__ = "Integer32"
_OnuStatus_Object = MibTableColumn
onuStatus = _OnuStatus_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 26),
    _OnuStatus_Type()
)
onuStatus.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuStatus.setStatus("mandatory")
_OnuDistance_Type = Integer32
_OnuDistance_Object = MibTableColumn
onuDistance = _OnuDistance_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 27),
    _OnuDistance_Type()
)
onuDistance.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuDistance.setStatus("mandatory")


class _OnuBindStatus_Type(Integer32):
    """Custom type onuBindStatus based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(0,
              1)
        )
    )
    namedValues = NamedValues(
        *(("static", 0),
          ("dynamic", 1))
    )


_OnuBindStatus_Type.__name__ = "Integer32"
_OnuBindStatus_Object = MibTableColumn
onuBindStatus = _OnuBindStatus_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 28),
    _OnuBindStatus_Type()
)
onuBindStatus.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuBindStatus.setStatus("mandatory")


class _OnuReset_Type(Integer32):
    """Custom type onuReset based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(0,
              1)
        )
    )
    namedValues = NamedValues(
        *(("reset", 0),
          ("no-reset", 1))
    )


_OnuReset_Type.__name__ = "Integer32"
_OnuReset_Object = MibTableColumn
onuReset = _OnuReset_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 29),
    _OnuReset_Type()
)
onuReset.setMaxAccess("write-only")
if mibBuilder.loadTexts:
    onuReset.setStatus("mandatory")
_OnuUpdateImage_Type = OctetString
_OnuUpdateImage_Object = MibTableColumn
onuUpdateImage = _OnuUpdateImage_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 30),
    _OnuUpdateImage_Type()
)
onuUpdateImage.setMaxAccess("write-only")
if mibBuilder.loadTexts:
    onuUpdateImage.setStatus("mandatory")
_OnuUpdateEepromImage_Type = OctetString
_OnuUpdateEepromImage_Object = MibTableColumn
onuUpdateEepromImage = _OnuUpdateEepromImage_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 31),
    _OnuUpdateEepromImage_Type()
)
onuUpdateEepromImage.setMaxAccess("write-only")
if mibBuilder.loadTexts:
    onuUpdateEepromImage.setStatus("mandatory")
_OnuEncryptionStatus_Type = TruthValue
_OnuEncryptionStatus_Object = MibTableColumn
onuEncryptionStatus = _OnuEncryptionStatus_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 32),
    _OnuEncryptionStatus_Type()
)
onuEncryptionStatus.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuEncryptionStatus.setStatus("mandatory")


class _OnuEncryptionMode_Type(Integer32):
    """Custom type onuEncryptionMode based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            2
        )
    )
    namedValues = NamedValues(
        ("ctc-churning", 2)
    )


_OnuEncryptionMode_Type.__name__ = "Integer32"
_OnuEncryptionMode_Object = MibTableColumn
onuEncryptionMode = _OnuEncryptionMode_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 33),
    _OnuEncryptionMode_Type()
)
onuEncryptionMode.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuEncryptionMode.setStatus("mandatory")
_OnuIgmpSnoopingStatus_Type = TruthValue
_OnuIgmpSnoopingStatus_Object = MibTableColumn
onuIgmpSnoopingStatus = _OnuIgmpSnoopingStatus_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 34),
    _OnuIgmpSnoopingStatus_Type()
)
onuIgmpSnoopingStatus.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuIgmpSnoopingStatus.setStatus("mandatory")


class _OnuMcstMode_Type(Integer32):
    """Custom type onuMcstMode based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(0,
              1)
        )
    )
    namedValues = NamedValues(
        *(("igmp-snooping", 0),
          ("dynamic-controllable", 1))
    )


_OnuMcstMode_Type.__name__ = "Integer32"
_OnuMcstMode_Object = MibTableColumn
onuMcstMode = _OnuMcstMode_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 35),
    _OnuMcstMode_Type()
)
onuMcstMode.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuMcstMode.setStatus("mandatory")


class _OnuAFastLeaveAbility_Type(Integer32):
    """Custom type onuAFastLeaveAbility based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(0,
              1,
              2,
              3)
        )
    )
    namedValues = NamedValues(
        *(("multicast-non-fast-leave", 0),
          ("igmp-snooping-fast-leave", 1),
          ("controlable-multicast-non-fast-leave", 2),
          ("controlable-multicast-fast-leave", 3))
    )


_OnuAFastLeaveAbility_Type.__name__ = "Integer32"
_OnuAFastLeaveAbility_Object = MibTableColumn
onuAFastLeaveAbility = _OnuAFastLeaveAbility_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 36),
    _OnuAFastLeaveAbility_Type()
)
onuAFastLeaveAbility.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuAFastLeaveAbility.setStatus("mandatory")


class _OnuAcFastLeaveAdminControl_Type(Integer32):
    """Custom type onuAcFastLeaveAdminControl based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(1,
              2)
        )
    )
    namedValues = NamedValues(
        *(("deactivate-Fast-Leave-Function", 1),
          ("activate-Fast-Leave-Function", 2))
    )


_OnuAcFastLeaveAdminControl_Type.__name__ = "Integer32"
_OnuAcFastLeaveAdminControl_Object = MibTableColumn
onuAcFastLeaveAdminControl = _OnuAcFastLeaveAdminControl_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 37),
    _OnuAcFastLeaveAdminControl_Type()
)
onuAcFastLeaveAdminControl.setMaxAccess("write-only")
if mibBuilder.loadTexts:
    onuAcFastLeaveAdminControl.setStatus("mandatory")


class _OnuAFastLeaveAdminState_Type(Integer32):
    """Custom type onuAFastLeaveAdminState based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(1,
              2)
        )
    )
    namedValues = NamedValues(
        *(("disable", 1),
          ("enable", 2))
    )


_OnuAFastLeaveAdminState_Type.__name__ = "Integer32"
_OnuAFastLeaveAdminState_Object = MibTableColumn
onuAFastLeaveAdminState = _OnuAFastLeaveAdminState_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 38),
    _OnuAFastLeaveAdminState_Type()
)
onuAFastLeaveAdminState.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuAFastLeaveAdminState.setStatus("mandatory")
_OnuInFecStatus_Type = TruthValue
_OnuInFecStatus_Object = MibTableColumn
onuInFecStatus = _OnuInFecStatus_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 39),
    _OnuInFecStatus_Type()
)
onuInFecStatus.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuInFecStatus.setStatus("mandatory")
_OnuOutFecStatus_Type = TruthValue
_OnuOutFecStatus_Object = MibTableColumn
onuOutFecStatus = _OnuOutFecStatus_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 40),
    _OnuOutFecStatus_Type()
)
onuOutFecStatus.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuOutFecStatus.setStatus("mandatory")
_OnuIfProtectedStatus_Type = TruthValue
_OnuIfProtectedStatus_Object = MibTableColumn
onuIfProtectedStatus = _OnuIfProtectedStatus_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 41),
    _OnuIfProtectedStatus_Type()
)
onuIfProtectedStatus.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuIfProtectedStatus.setStatus("mandatory")


class _OnuSehedulePolicy_Type(Integer32):
    """Custom type onuSehedulePolicy based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(1,
              2)
        )
    )
    namedValues = NamedValues(
        *(("sp", 1),
          ("wrr", 2))
    )


_OnuSehedulePolicy_Type.__name__ = "Integer32"
_OnuSehedulePolicy_Object = MibTableColumn
onuSehedulePolicy = _OnuSehedulePolicy_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 42),
    _OnuSehedulePolicy_Type()
)
onuSehedulePolicy.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuSehedulePolicy.setStatus("mandatory")


class _OnuDynamicMacLearningStatus_Type(Integer32):
    """Custom type onuDynamicMacLearningStatus based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(1,
              2)
        )
    )
    namedValues = NamedValues(
        *(("off", 1),
          ("on", 2))
    )


_OnuDynamicMacLearningStatus_Type.__name__ = "Integer32"
_OnuDynamicMacLearningStatus_Object = MibTableColumn
onuDynamicMacLearningStatus = _OnuDynamicMacLearningStatus_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 43),
    _OnuDynamicMacLearningStatus_Type()
)
onuDynamicMacLearningStatus.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuDynamicMacLearningStatus.setStatus("mandatory")


class _OnuDynamicMacAgingTime_Type(Integer32):
    """Custom type onuDynamicMacAgingTime based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueRangeConstraint(0, 3825),
    )


_OnuDynamicMacAgingTime_Type.__name__ = "Integer32"
_OnuDynamicMacAgingTime_Object = MibTableColumn
onuDynamicMacAgingTime = _OnuDynamicMacAgingTime_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 44),
    _OnuDynamicMacAgingTime_Type()
)
onuDynamicMacAgingTime.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuDynamicMacAgingTime.setStatus("mandatory")
_OnuStaticMacAddress_Type = MacAddress
_OnuStaticMacAddress_Object = MibTableColumn
onuStaticMacAddress = _OnuStaticMacAddress_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 45),
    _OnuStaticMacAddress_Type()
)
onuStaticMacAddress.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuStaticMacAddress.setStatus("mandatory")


class _OnuStaticMacAddressPortBitmap_Type(Bits):
    """Custom type onuStaticMacAddressPortBitmap based on Bits"""
    namedValues = NamedValues(
        *(("port1", 0),
          ("port2", 1),
          ("port3", 2),
          ("port4", 3),
          ("port5", 4),
          ("port6", 5),
          ("port7", 6),
          ("port8", 7))
    )

_OnuStaticMacAddressPortBitmap_Type.__name__ = "Bits"
_OnuStaticMacAddressPortBitmap_Object = MibTableColumn
onuStaticMacAddressPortBitmap = _OnuStaticMacAddressPortBitmap_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 46),
    _OnuStaticMacAddressPortBitmap_Type()
)
onuStaticMacAddressPortBitmap.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuStaticMacAddressPortBitmap.setStatus("mandatory")
_OnuStaticMacAddressConfigRowStatus_Type = RowStatus
_OnuStaticMacAddressConfigRowStatus_Object = MibTableColumn
onuStaticMacAddressConfigRowStatus = _OnuStaticMacAddressConfigRowStatus_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 47),
    _OnuStaticMacAddressConfigRowStatus_Type()
)
onuStaticMacAddressConfigRowStatus.setMaxAccess("read-create")
if mibBuilder.loadTexts:
    onuStaticMacAddressConfigRowStatus.setStatus("mandatory")
_OnuClearDynamicMacAddressByMac_Type = MacAddress
_OnuClearDynamicMacAddressByMac_Object = MibTableColumn
onuClearDynamicMacAddressByMac = _OnuClearDynamicMacAddressByMac_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 48),
    _OnuClearDynamicMacAddressByMac_Type()
)
onuClearDynamicMacAddressByMac.setMaxAccess("write-only")
if mibBuilder.loadTexts:
    onuClearDynamicMacAddressByMac.setStatus("mandatory")
_OnuClearDynamicMacAddressByPort_Type = Integer32
_OnuClearDynamicMacAddressByPort_Object = MibTableColumn
onuClearDynamicMacAddressByPort = _OnuClearDynamicMacAddressByPort_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 49),
    _OnuClearDynamicMacAddressByPort_Type()
)
onuClearDynamicMacAddressByPort.setMaxAccess("write-only")
if mibBuilder.loadTexts:
    onuClearDynamicMacAddressByPort.setStatus("mandatory")
_OnuPriorityQueueMapping_Type = OctetString
_OnuPriorityQueueMapping_Object = MibTableColumn
onuPriorityQueueMapping = _OnuPriorityQueueMapping_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 50),
    _OnuPriorityQueueMapping_Type()
)
onuPriorityQueueMapping.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuPriorityQueueMapping.setStatus("mandatory")


class _OnuVlanMode_Type(Integer32):
    """Custom type onuVlanMode based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(0,
              1,
              2,
              3,
              254)
        )
    )
    namedValues = NamedValues(
        *(("transparent-mode", 0),
          ("tag-mode", 1),
          ("translation-mode", 2),
          ("stacking-mode", 3),
          ("none", 254))
    )


_OnuVlanMode_Type.__name__ = "Integer32"
_OnuVlanMode_Object = MibTableColumn
onuVlanMode = _OnuVlanMode_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 51),
    _OnuVlanMode_Type()
)
onuVlanMode.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuVlanMode.setStatus("mandatory")


class _OnuIpAddressMode_Type(Integer32):
    """Custom type onuIpAddressMode based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(1,
              2)
        )
    )
    namedValues = NamedValues(
        *(("dhcp", 1),
          ("static", 2))
    )


_OnuIpAddressMode_Type.__name__ = "Integer32"
_OnuIpAddressMode_Object = MibTableColumn
onuIpAddressMode = _OnuIpAddressMode_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 52),
    _OnuIpAddressMode_Type()
)
onuIpAddressMode.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuIpAddressMode.setStatus("mandatory")
_OnuStaticIpAddress_Type = IpAddress
_OnuStaticIpAddress_Object = MibTableColumn
onuStaticIpAddress = _OnuStaticIpAddress_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 53),
    _OnuStaticIpAddress_Type()
)
onuStaticIpAddress.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuStaticIpAddress.setStatus("mandatory")
_OnuStaticIpMask_Type = IpAddress
_OnuStaticIpMask_Object = MibTableColumn
onuStaticIpMask = _OnuStaticIpMask_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 54),
    _OnuStaticIpMask_Type()
)
onuStaticIpMask.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuStaticIpMask.setStatus("mandatory")
_OnuStaticIpGateway_Type = IpAddress
_OnuStaticIpGateway_Object = MibTableColumn
onuStaticIpGateway = _OnuStaticIpGateway_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 55),
    _OnuStaticIpGateway_Type()
)
onuStaticIpGateway.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuStaticIpGateway.setStatus("mandatory")


class _OnuMgmtVlan_Type(Integer32):
    """Custom type onuMgmtVlan based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueRangeConstraint(1, 4094),
    )


_OnuMgmtVlan_Type.__name__ = "Integer32"
_OnuMgmtVlan_Object = MibTableColumn
onuMgmtVlan = _OnuMgmtVlan_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 56),
    _OnuMgmtVlan_Type()
)
onuMgmtVlan.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuMgmtVlan.setStatus("mandatory")
_OnuStaticIpAddressRowStatus_Type = RowStatus
_OnuStaticIpAddressRowStatus_Object = MibTableColumn
onuStaticIpAddressRowStatus = _OnuStaticIpAddressRowStatus_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 57),
    _OnuStaticIpAddressRowStatus_Type()
)
onuStaticIpAddressRowStatus.setMaxAccess("read-create")
if mibBuilder.loadTexts:
    onuStaticIpAddressRowStatus.setStatus("mandatory")


class _OnuCIR_Type(Integer32):
    """Custom type onuCIR based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueRangeConstraint(0, 16777215),
    )


_OnuCIR_Type.__name__ = "Integer32"
_OnuCIR_Object = MibTableColumn
onuCIR = _OnuCIR_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 58),
    _OnuCIR_Type()
)
onuCIR.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuCIR.setStatus("mandatory")


class _OnuCBS_Type(Integer32):
    """Custom type onuCBS based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueRangeConstraint(0, 65535),
    )


_OnuCBS_Type.__name__ = "Integer32"
_OnuCBS_Object = MibTableColumn
onuCBS = _OnuCBS_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 59),
    _OnuCBS_Type()
)
onuCBS.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuCBS.setStatus("mandatory")


class _OnuEBS_Type(Integer32):
    """Custom type onuEBS based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueRangeConstraint(0, 65535),
    )


_OnuEBS_Type.__name__ = "Integer32"
_OnuEBS_Object = MibTableColumn
onuEBS = _OnuEBS_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 60),
    _OnuEBS_Type()
)
onuEBS.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuEBS.setStatus("mandatory")
_OnuIfMacACL_Type = DisplayString
_OnuIfMacACL_Object = MibTableColumn
onuIfMacACL = _OnuIfMacACL_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 61),
    _OnuIfMacACL_Type()
)
onuIfMacACL.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuIfMacACL.setStatus("mandatory")
_OnuIfIpACL_Type = DisplayString
_OnuIfIpACL_Object = MibTableColumn
onuIfIpACL = _OnuIfIpACL_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 62),
    _OnuIfIpACL_Type()
)
onuIfIpACL.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuIfIpACL.setStatus("mandatory")


class _OnuVlans_Type(Bits):
    """Custom type onuVlans based on Bits"""
    namedValues = NamedValues(
        *(("vlan1", 0),
          ("vlan2", 1),
          ("vlan3", 2),
          ("vlan4", 3),
          ("vlan5", 4),
          ("vlan6", 5),
          ("vlan7", 6),
          ("vlan8", 7))
    )

_OnuVlans_Type.__name__ = "Bits"
_OnuVlans_Object = MibTableColumn
onuVlans = _OnuVlans_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 63),
    _OnuVlans_Type()
)
onuVlans.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuVlans.setStatus("mandatory")
_OnuActivePonDiid_Type = Integer32
_OnuActivePonDiid_Object = MibTableColumn
onuActivePonDiid = _OnuActivePonDiid_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 64),
    _OnuActivePonDiid_Type()
)
onuActivePonDiid.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuActivePonDiid.setStatus("mandatory")
_OnuPonPortCount_Type = Integer32
_OnuPonPortCount_Object = MibTableColumn
onuPonPortCount = _OnuPonPortCount_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 65),
    _OnuPonPortCount_Type()
)
onuPonPortCount.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuPonPortCount.setStatus("mandatory")
_OnuActivePonPortIndex_Type = Integer32
_OnuActivePonPortIndex_Object = MibTableColumn
onuActivePonPortIndex = _OnuActivePonPortIndex_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 66),
    _OnuActivePonPortIndex_Type()
)
onuActivePonPortIndex.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuActivePonPortIndex.setStatus("mandatory")


class _OnuSerialPortWorkMode_Type(Integer32):
    """Custom type onuSerialPortWorkMode based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(0,
              1,
              2,
              3)
        )
    )
    namedValues = NamedValues(
        *(("none", 0),
          ("tcp-server", 1),
          ("udp", 2),
          ("tcp-client", 3))
    )


_OnuSerialPortWorkMode_Type.__name__ = "Integer32"
_OnuSerialPortWorkMode_Object = MibTableColumn
onuSerialPortWorkMode = _OnuSerialPortWorkMode_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 67),
    _OnuSerialPortWorkMode_Type()
)
onuSerialPortWorkMode.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuSerialPortWorkMode.setStatus("mandatory")


class _OnuSerialPortWorkPort_Type(Integer32):
    """Custom type onuSerialPortWorkPort based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueRangeConstraint(5000, 30000),
    )


_OnuSerialPortWorkPort_Type.__name__ = "Integer32"
_OnuSerialPortWorkPort_Object = MibTableColumn
onuSerialPortWorkPort = _OnuSerialPortWorkPort_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 68),
    _OnuSerialPortWorkPort_Type()
)
onuSerialPortWorkPort.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuSerialPortWorkPort.setStatus("mandatory")
_OnuSerialWorkModeRowStatus_Type = RowStatus
_OnuSerialWorkModeRowStatus_Object = MibTableColumn
onuSerialWorkModeRowStatus = _OnuSerialWorkModeRowStatus_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 69),
    _OnuSerialWorkModeRowStatus_Type()
)
onuSerialWorkModeRowStatus.setMaxAccess("read-create")
if mibBuilder.loadTexts:
    onuSerialWorkModeRowStatus.setStatus("mandatory")


class _OnuRemoteServerIpAddrIndex_Type(Integer32):
    """Custom type onuRemoteServerIpAddrIndex based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueRangeConstraint(0, 1000),
    )


_OnuRemoteServerIpAddrIndex_Type.__name__ = "Integer32"
_OnuRemoteServerIpAddrIndex_Object = MibTableColumn
onuRemoteServerIpAddrIndex = _OnuRemoteServerIpAddrIndex_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 70),
    _OnuRemoteServerIpAddrIndex_Type()
)
onuRemoteServerIpAddrIndex.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuRemoteServerIpAddrIndex.setStatus("mandatory")
_OnuPeerOLTIpAddr_Type = IpAddress
_OnuPeerOLTIpAddr_Object = MibTableColumn
onuPeerOLTIpAddr = _OnuPeerOLTIpAddr_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 71),
    _OnuPeerOLTIpAddr_Type()
)
onuPeerOLTIpAddr.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuPeerOLTIpAddr.setStatus("mandatory")
_OnuPeerPONIndex_Type = Integer32
_OnuPeerPONIndex_Object = MibTableColumn
onuPeerPONIndex = _OnuPeerPONIndex_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 72),
    _OnuPeerPONIndex_Type()
)
onuPeerPONIndex.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuPeerPONIndex.setStatus("mandatory")
_OnuSerialPortCount_Type = Integer32
_OnuSerialPortCount_Object = MibTableColumn
onuSerialPortCount = _OnuSerialPortCount_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 73),
    _OnuSerialPortCount_Type()
)
onuSerialPortCount.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuSerialPortCount.setStatus("mandatory")


class _OnuBakupPonStatus_Type(Integer32):
    """Custom type onuBakupPonStatus based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(0,
              1)
        )
    )
    namedValues = NamedValues(
        *(("passive", 0),
          ("active", 1))
    )


_OnuBakupPonStatus_Type.__name__ = "Integer32"
_OnuBakupPonStatus_Object = MibTableColumn
onuBakupPonStatus = _OnuBakupPonStatus_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 74),
    _OnuBakupPonStatus_Type()
)
onuBakupPonStatus.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuBakupPonStatus.setStatus("mandatory")


class _OnuCurrentPONInUse_Type(Integer32):
    """Custom type onuCurrentPONInUse based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(1,
              2)
        )
    )
    namedValues = NamedValues(
        *(("in-use", 1),
          ("not-in-use", 2))
    )


_OnuCurrentPONInUse_Type.__name__ = "Integer32"
_OnuCurrentPONInUse_Object = MibTableColumn
onuCurrentPONInUse = _OnuCurrentPONInUse_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 75),
    _OnuCurrentPONInUse_Type()
)
onuCurrentPONInUse.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuCurrentPONInUse.setStatus("mandatory")
_OnuCurrentPONMAC_Type = PhysAddress
_OnuCurrentPONMAC_Object = MibTableColumn
onuCurrentPONMAC = _OnuCurrentPONMAC_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 76),
    _OnuCurrentPONMAC_Type()
)
onuCurrentPONMAC.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuCurrentPONMAC.setStatus("mandatory")
_OnuPeerPONDiid_Type = Integer32
_OnuPeerPONDiid_Object = MibTableColumn
onuPeerPONDiid = _OnuPeerPONDiid_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 77),
    _OnuPeerPONDiid_Type()
)
onuPeerPONDiid.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuPeerPONDiid.setStatus("mandatory")
_OnuPeerPONMAC_Type = PhysAddress
_OnuPeerPONMAC_Object = MibTableColumn
onuPeerPONMAC = _OnuPeerPONMAC_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 78),
    _OnuPeerPONMAC_Type()
)
onuPeerPONMAC.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuPeerPONMAC.setStatus("mandatory")
_OnuConfigurablePortDiid_Type = Integer32
_OnuConfigurablePortDiid_Object = MibTableColumn
onuConfigurablePortDiid = _OnuConfigurablePortDiid_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 79),
    _OnuConfigurablePortDiid_Type()
)
onuConfigurablePortDiid.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuConfigurablePortDiid.setStatus("mandatory")
_OnuAliveTime_Type = Integer32
_OnuAliveTime_Object = MibScalar
onuAliveTime = _OnuAliveTime_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 1, 1, 80),
    _OnuAliveTime_Type()
)
onuAliveTime.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuAliveTime.setStatus("mandatory")
_NmsepononuPonSwitchTable_Object = MibTable
nmsepononuPonSwitchTable = _NmsepononuPonSwitchTable_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 2)
)
if mibBuilder.loadTexts:
    nmsepononuPonSwitchTable.setStatus("mandatory")
_NmsEponOnuPonSwitchEntry_Object = MibTableRow
nmsEponOnuPonSwitchEntry = _NmsEponOnuPonSwitchEntry_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 2, 1)
)
nmsEponOnuPonSwitchEntry.setIndexNames(
    (0, "NMS-EPON-ONU", "ifIndex"),
)
if mibBuilder.loadTexts:
    nmsEponOnuPonSwitchEntry.setStatus("mandatory")
_IfIndex_Type = Integer32
_IfIndex_Object = MibTableColumn
ifIndex = _IfIndex_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 2, 1, 1),
    _IfIndex_Type()
)
ifIndex.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    ifIndex.setStatus("mandatory")


class _OperType_Type(Integer32):
    """Custom type operType based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(0,
              1)
        )
    )
    namedValues = NamedValues(
        *(("switchBack", 0),
          ("switchToAnother", 1))
    )


_OperType_Type.__name__ = "Integer32"
_OperType_Object = MibTableColumn
operType = _OperType_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 2, 1, 2),
    _OperType_Type()
)
operType.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    operType.setStatus("mandatory")
_Nmsepononucap2Table_Object = MibTable
nmsepononucap2Table = _Nmsepononucap2Table_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 3)
)
if mibBuilder.loadTexts:
    nmsepononucap2Table.setStatus("mandatory")
_NmsEponOnuCap2Entry_Object = MibTableRow
nmsEponOnuCap2Entry = _NmsEponOnuCap2Entry_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 3, 1)
)
nmsEponOnuCap2Entry.setIndexNames(
    (0, "NMS-EPON-LLID", "llidIfIndex"),
)
if mibBuilder.loadTexts:
    nmsEponOnuCap2Entry.setStatus("mandatory")


class _Cap2OnuType_Type(Integer32):
    """Custom type cap2OnuType based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(0,
              1,
              2,
              3,
              4,
              5,
              6,
              7,
              8)
        )
    )
    namedValues = NamedValues(
        *(("sfu", 0),
          ("hgu", 1),
          ("sbu", 2),
          ("mdu-3", 3),
          ("mdu-4", 4),
          ("mdu-5", 5),
          ("mdu-6", 6),
          ("mdu-7", 7),
          ("mtu", 8))
    )


_Cap2OnuType_Type.__name__ = "Integer32"
_Cap2OnuType_Object = MibTableColumn
cap2OnuType = _Cap2OnuType_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 3, 1, 1),
    _Cap2OnuType_Type()
)
cap2OnuType.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    cap2OnuType.setStatus("mandatory")


class _Cap2Multillid_Type(Integer32):
    """Custom type cap2Multillid based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(0,
              1)
        )
    )
    namedValues = NamedValues(
        *(("yes", 0),
          ("no", 1))
    )


_Cap2Multillid_Type.__name__ = "Integer32"
_Cap2Multillid_Object = MibTableColumn
cap2Multillid = _Cap2Multillid_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 3, 1, 2),
    _Cap2Multillid_Type()
)
cap2Multillid.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    cap2Multillid.setStatus("mandatory")


class _Cap2ProtectionType_Type(Integer32):
    """Custom type cap2ProtectionType based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(0,
              1,
              2)
        )
    )
    namedValues = NamedValues(
        *(("notsupported", 0),
          ("supportc-psg", 1),
          ("supportd-psg", 2))
    )


_Cap2ProtectionType_Type.__name__ = "Integer32"
_Cap2ProtectionType_Object = MibTableColumn
cap2ProtectionType = _Cap2ProtectionType_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 3, 1, 3),
    _Cap2ProtectionType_Type()
)
cap2ProtectionType.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    cap2ProtectionType.setStatus("mandatory")
_Cap2NumPONIf_Type = Integer32
_Cap2NumPONIf_Object = MibTableColumn
cap2NumPONIf = _Cap2NumPONIf_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 3, 1, 4),
    _Cap2NumPONIf_Type()
)
cap2NumPONIf.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    cap2NumPONIf.setStatus("mandatory")
_Cap2NumSlot_Type = Integer32
_Cap2NumSlot_Object = MibTableColumn
cap2NumSlot = _Cap2NumSlot_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 3, 1, 5),
    _Cap2NumSlot_Type()
)
cap2NumSlot.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    cap2NumSlot.setStatus("mandatory")
_Cap2NumIfType_Type = Integer32
_Cap2NumIfType_Object = MibTableColumn
cap2NumIfType = _Cap2NumIfType_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 3, 1, 6),
    _Cap2NumIfType_Type()
)
cap2NumIfType.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    cap2NumIfType.setStatus("mandatory")
_Cap2NumGEPorts_Type = Integer32
_Cap2NumGEPorts_Object = MibTableColumn
cap2NumGEPorts = _Cap2NumGEPorts_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 3, 1, 7),
    _Cap2NumGEPorts_Type()
)
cap2NumGEPorts.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    cap2NumGEPorts.setStatus("mandatory")
_Cap2NumFEPorts_Type = Integer32
_Cap2NumFEPorts_Object = MibTableColumn
cap2NumFEPorts = _Cap2NumFEPorts_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 3, 1, 8),
    _Cap2NumFEPorts_Type()
)
cap2NumFEPorts.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    cap2NumFEPorts.setStatus("mandatory")
_Cap2NumVoIPPorts_Type = Integer32
_Cap2NumVoIPPorts_Object = MibTableColumn
cap2NumVoIPPorts = _Cap2NumVoIPPorts_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 3, 1, 9),
    _Cap2NumVoIPPorts_Type()
)
cap2NumVoIPPorts.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    cap2NumVoIPPorts.setStatus("mandatory")
_Cap2NumTDMPorts_Type = Integer32
_Cap2NumTDMPorts_Object = MibTableColumn
cap2NumTDMPorts = _Cap2NumTDMPorts_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 3, 1, 10),
    _Cap2NumTDMPorts_Type()
)
cap2NumTDMPorts.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    cap2NumTDMPorts.setStatus("mandatory")
_Cap2NumADSL2Ports_Type = Integer32
_Cap2NumADSL2Ports_Object = MibTableColumn
cap2NumADSL2Ports = _Cap2NumADSL2Ports_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 3, 1, 11),
    _Cap2NumADSL2Ports_Type()
)
cap2NumADSL2Ports.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    cap2NumADSL2Ports.setStatus("mandatory")
_Cap2NumVDSL2Ports_Type = Integer32
_Cap2NumVDSL2Ports_Object = MibTableColumn
cap2NumVDSL2Ports = _Cap2NumVDSL2Ports_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 3, 1, 12),
    _Cap2NumVDSL2Ports_Type()
)
cap2NumVDSL2Ports.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    cap2NumVDSL2Ports.setStatus("mandatory")
_Cap2NumWLANPorts_Type = Integer32
_Cap2NumWLANPorts_Object = MibTableColumn
cap2NumWLANPorts = _Cap2NumWLANPorts_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 3, 1, 13),
    _Cap2NumWLANPorts_Type()
)
cap2NumWLANPorts.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    cap2NumWLANPorts.setStatus("mandatory")
_Cap2NumUSBPorts_Type = Integer32
_Cap2NumUSBPorts_Object = MibTableColumn
cap2NumUSBPorts = _Cap2NumUSBPorts_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 3, 1, 14),
    _Cap2NumUSBPorts_Type()
)
cap2NumUSBPorts.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    cap2NumUSBPorts.setStatus("mandatory")
_Cap2NumCATVRFPorts_Type = Integer32
_Cap2NumCATVRFPorts_Object = MibTableColumn
cap2NumCATVRFPorts = _Cap2NumCATVRFPorts_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 3, 1, 15),
    _Cap2NumCATVRFPorts_Type()
)
cap2NumCATVRFPorts.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    cap2NumCATVRFPorts.setStatus("mandatory")
_Cap2NumSerialPorts_Type = Integer32
_Cap2NumSerialPorts_Object = MibTableColumn
cap2NumSerialPorts = _Cap2NumSerialPorts_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 3, 1, 16),
    _Cap2NumSerialPorts_Type()
)
cap2NumSerialPorts.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    cap2NumSerialPorts.setStatus("mandatory")


class _Cap2BatteryBackup_Type(Integer32):
    """Custom type cap2BatteryBackup based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(0,
              1)
        )
    )
    namedValues = NamedValues(
        *(("no", 0),
          ("yes", 1))
    )


_Cap2BatteryBackup_Type.__name__ = "Integer32"
_Cap2BatteryBackup_Object = MibTableColumn
cap2BatteryBackup = _Cap2BatteryBackup_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 3, 1, 17),
    _Cap2BatteryBackup_Type()
)
cap2BatteryBackup.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    cap2BatteryBackup.setStatus("mandatory")
_NmsepononusnmpTable_Object = MibTable
nmsepononusnmpTable = _NmsepononusnmpTable_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 4)
)
if mibBuilder.loadTexts:
    nmsepononusnmpTable.setStatus("mandatory")
_NmsEponOnuSnmpEntry_Object = MibTableRow
nmsEponOnuSnmpEntry = _NmsEponOnuSnmpEntry_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 4, 1)
)
nmsEponOnuSnmpEntry.setIndexNames(
    (0, "NMS-EPON-LLID", "llidIfIndex"),
)
if mibBuilder.loadTexts:
    nmsEponOnuSnmpEntry.setStatus("mandatory")
_OnuMacAddr_Type = PhysAddress
_OnuMacAddr_Object = MibTableColumn
onuMacAddr = _OnuMacAddr_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 4, 1, 1),
    _OnuMacAddr_Type()
)
onuMacAddr.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuMacAddr.setStatus("mandatory")
_OnuIpAddr_Type = IpAddress
_OnuIpAddr_Object = MibTableColumn
onuIpAddr = _OnuIpAddr_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 4, 1, 2),
    _OnuIpAddr_Type()
)
onuIpAddr.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuIpAddr.setStatus("mandatory")
_OnuCommRo_Type = DisplayString
_OnuCommRo_Object = MibTableColumn
onuCommRo = _OnuCommRo_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 4, 1, 3),
    _OnuCommRo_Type()
)
onuCommRo.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuCommRo.setStatus("mandatory")
_OnuCommRw_Type = DisplayString
_OnuCommRw_Object = MibTableColumn
onuCommRw = _OnuCommRw_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 4, 1, 4),
    _OnuCommRw_Type()
)
onuCommRw.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuCommRw.setStatus("mandatory")


class _OnuSnmpPort_Type(Integer32):
    """Custom type onuSnmpPort based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueRangeConstraint(1, 65535),
    )


_OnuSnmpPort_Type.__name__ = "Integer32"
_OnuSnmpPort_Object = MibTableColumn
onuSnmpPort = _OnuSnmpPort_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 4, 1, 5),
    _OnuSnmpPort_Type()
)
onuSnmpPort.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuSnmpPort.setStatus("mandatory")


class _OnuSnmpTrapPort_Type(Integer32):
    """Custom type onuSnmpTrapPort based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueRangeConstraint(1, 65535),
    )


_OnuSnmpTrapPort_Type.__name__ = "Integer32"
_OnuSnmpTrapPort_Object = MibTableColumn
onuSnmpTrapPort = _OnuSnmpTrapPort_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 4, 1, 6),
    _OnuSnmpTrapPort_Type()
)
onuSnmpTrapPort.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuSnmpTrapPort.setStatus("mandatory")


class _OnuSnmpVersion_Type(Integer32):
    """Custom type onuSnmpVersion based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(1,
              2)
        )
    )
    namedValues = NamedValues(
        *(("v1", 1),
          ("v2c", 2))
    )


_OnuSnmpVersion_Type.__name__ = "Integer32"
_OnuSnmpVersion_Object = MibTableColumn
onuSnmpVersion = _OnuSnmpVersion_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 4, 1, 7),
    _OnuSnmpVersion_Type()
)
onuSnmpVersion.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuSnmpVersion.setStatus("mandatory")


class _OnuSnmpTrapVersion_Type(Integer32):
    """Custom type onuSnmpTrapVersion based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(1,
              2)
        )
    )
    namedValues = NamedValues(
        *(("v1", 1),
          ("v2c", 2))
    )


_OnuSnmpTrapVersion_Type.__name__ = "Integer32"
_OnuSnmpTrapVersion_Object = MibTableColumn
onuSnmpTrapVersion = _OnuSnmpTrapVersion_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 4, 1, 8),
    _OnuSnmpTrapVersion_Type()
)
onuSnmpTrapVersion.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuSnmpTrapVersion.setStatus("mandatory")
_OnuSnmpTrapHost_Type = IpAddress
_OnuSnmpTrapHost_Object = MibTableColumn
onuSnmpTrapHost = _OnuSnmpTrapHost_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 4, 1, 9),
    _OnuSnmpTrapHost_Type()
)
onuSnmpTrapHost.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuSnmpTrapHost.setStatus("mandatory")
_NmsepononuopticalportTable_Object = MibTable
nmsepononuopticalportTable = _NmsepononuopticalportTable_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 5)
)
if mibBuilder.loadTexts:
    nmsepononuopticalportTable.setStatus("mandatory")
_NmsEponOnuOpticalPortEntry_Object = MibTableRow
nmsEponOnuOpticalPortEntry = _NmsEponOnuOpticalPortEntry_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 5, 1)
)
nmsEponOnuOpticalPortEntry.setIndexNames(
    (0, "NMS-EPON-ONU", "opIfIndex"),
)
if mibBuilder.loadTexts:
    nmsEponOnuOpticalPortEntry.setStatus("mandatory")
_OpIfIndex_Type = Integer32
_OpIfIndex_Object = MibTableColumn
opIfIndex = _OpIfIndex_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 5, 1, 1),
    _OpIfIndex_Type()
)
opIfIndex.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    opIfIndex.setStatus("mandatory")
_OpModuleTemp_Type = Integer32
_OpModuleTemp_Object = MibTableColumn
opModuleTemp = _OpModuleTemp_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 5, 1, 2),
    _OpModuleTemp_Type()
)
opModuleTemp.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    opModuleTemp.setStatus("mandatory")
_OpModuleVolt_Type = Integer32
_OpModuleVolt_Object = MibTableColumn
opModuleVolt = _OpModuleVolt_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 5, 1, 3),
    _OpModuleVolt_Type()
)
opModuleVolt.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    opModuleVolt.setStatus("mandatory")
_OpModuleCurrent_Type = Integer32
_OpModuleCurrent_Object = MibTableColumn
opModuleCurrent = _OpModuleCurrent_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 5, 1, 4),
    _OpModuleCurrent_Type()
)
opModuleCurrent.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    opModuleCurrent.setStatus("mandatory")
_OpModuleRxPower_Type = Integer32
_OpModuleRxPower_Object = MibTableColumn
opModuleRxPower = _OpModuleRxPower_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 5, 1, 5),
    _OpModuleRxPower_Type()
)
opModuleRxPower.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    opModuleRxPower.setStatus("mandatory")
_OpModuleTxPower_Type = Integer32
_OpModuleTxPower_Object = MibTableColumn
opModuleTxPower = _OpModuleTxPower_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 5, 1, 6),
    _OpModuleTxPower_Type()
)
opModuleTxPower.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    opModuleTxPower.setStatus("mandatory")
_OnuIPParamGetTable_Object = MibTable
onuIPParamGetTable = _OnuIPParamGetTable_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 7)
)
if mibBuilder.loadTexts:
    onuIPParamGetTable.setStatus("mandatory")
_OnuIPParamGetEntry_Object = MibTableRow
onuIPParamGetEntry = _OnuIPParamGetEntry_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 7, 1)
)
onuIPParamGetEntry.setIndexNames(
    (0, "NMS-EPON-ONU", "onuIfIndex"),
)
if mibBuilder.loadTexts:
    onuIPParamGetEntry.setStatus("mandatory")
_OnuIfIndex_Type = Integer32
_OnuIfIndex_Object = MibTableColumn
onuIfIndex = _OnuIfIndex_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 7, 1, 1),
    _OnuIfIndex_Type()
)
onuIfIndex.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuIfIndex.setStatus("mandatory")


class _IpVersion_Type(Integer32):
    """Custom type ipVersion based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(1,
              2)
        )
    )
    namedValues = NamedValues(
        *(("ipv4", 1),
          ("ipv6", 2))
    )


_IpVersion_Type.__name__ = "Integer32"
_IpVersion_Object = MibTableColumn
ipVersion = _IpVersion_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 7, 1, 2),
    _IpVersion_Type()
)
ipVersion.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    ipVersion.setStatus("mandatory")
_Ipv4Address_Type = IpAddress
_Ipv4Address_Object = MibTableColumn
ipv4Address = _Ipv4Address_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 7, 1, 3),
    _Ipv4Address_Type()
)
ipv4Address.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    ipv4Address.setStatus("mandatory")
_Ipv4Mask_Type = IpAddress
_Ipv4Mask_Object = MibTableColumn
ipv4Mask = _Ipv4Mask_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 7, 1, 4),
    _Ipv4Mask_Type()
)
ipv4Mask.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    ipv4Mask.setStatus("mandatory")
_Ipv4GateWay_Type = IpAddress
_Ipv4GateWay_Object = MibTableColumn
ipv4GateWay = _Ipv4GateWay_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 7, 1, 5),
    _Ipv4GateWay_Type()
)
ipv4GateWay.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    ipv4GateWay.setStatus("mandatory")
_Ipv6Address_Type = InetAddressIPv6
_Ipv6Address_Object = MibTableColumn
ipv6Address = _Ipv6Address_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 7, 1, 6),
    _Ipv6Address_Type()
)
ipv6Address.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    ipv6Address.setStatus("mandatory")
_Ipv6Prefix_Type = Integer32
_Ipv6Prefix_Object = MibTableColumn
ipv6Prefix = _Ipv6Prefix_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 7, 1, 7),
    _Ipv6Prefix_Type()
)
ipv6Prefix.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    ipv6Prefix.setStatus("mandatory")
_Ipv6GateWay_Type = InetAddressIPv6
_Ipv6GateWay_Object = MibTableColumn
ipv6GateWay = _Ipv6GateWay_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 7, 1, 8),
    _Ipv6GateWay_Type()
)
ipv6GateWay.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    ipv6GateWay.setStatus("mandatory")


class _Cvlan_Type(Integer32):
    """Custom type cvlan based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueRangeConstraint(1, 4094),
    )


_Cvlan_Type.__name__ = "Integer32"
_Cvlan_Object = MibTableColumn
cvlan = _Cvlan_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 7, 1, 9),
    _Cvlan_Type()
)
cvlan.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    cvlan.setStatus("mandatory")


class _Svlan_Type(Integer32):
    """Custom type svlan based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueRangeConstraint(0, 4094),
    )


_Svlan_Type.__name__ = "Integer32"
_Svlan_Object = MibTableColumn
svlan = _Svlan_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 7, 1, 10),
    _Svlan_Type()
)
svlan.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    svlan.setStatus("mandatory")


class _Priority_Type(Integer32):
    """Custom type priority based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueRangeConstraint(0, 7),
    )


_Priority_Type.__name__ = "Integer32"
_Priority_Object = MibTableColumn
priority = _Priority_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 7, 1, 11),
    _Priority_Type()
)
priority.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    priority.setStatus("mandatory")
_OnuCTCIPParamConfigTable_Object = MibTable
onuCTCIPParamConfigTable = _OnuCTCIPParamConfigTable_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 29)
)
if mibBuilder.loadTexts:
    onuCTCIPParamConfigTable.setStatus("current")
_OnuCTCIPParamConfigEntry_Object = MibTableRow
onuCTCIPParamConfigEntry = _OnuCTCIPParamConfigEntry_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 29, 1)
)
onuCTCIPParamConfigEntry.setIndexNames(
    (0, "NMS-EPON-ONU", "onuCTCIPParamConfigIfIndex"),
)
if mibBuilder.loadTexts:
    onuCTCIPParamConfigEntry.setStatus("current")
_OnuCTCIPParamConfigIfIndex_Type = Integer32
_OnuCTCIPParamConfigIfIndex_Object = MibTableColumn
onuCTCIPParamConfigIfIndex = _OnuCTCIPParamConfigIfIndex_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 29, 1, 1),
    _OnuCTCIPParamConfigIfIndex_Type()
)
onuCTCIPParamConfigIfIndex.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    onuCTCIPParamConfigIfIndex.setStatus("current")


class _OnuCTCIPParamConfigIpVersion_Type(Integer32):
    """Custom type onuCTCIPParamConfigIpVersion based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(1,
              2)
        )
    )
    namedValues = NamedValues(
        *(("ipv4", 1),
          ("ipv6", 2))
    )


_OnuCTCIPParamConfigIpVersion_Type.__name__ = "Integer32"
_OnuCTCIPParamConfigIpVersion_Object = MibTableColumn
onuCTCIPParamConfigIpVersion = _OnuCTCIPParamConfigIpVersion_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 29, 1, 2),
    _OnuCTCIPParamConfigIpVersion_Type()
)
onuCTCIPParamConfigIpVersion.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuCTCIPParamConfigIpVersion.setStatus("current")
_OnuCTCIPParamConfigIpv4Address_Type = IpAddress
_OnuCTCIPParamConfigIpv4Address_Object = MibTableColumn
onuCTCIPParamConfigIpv4Address = _OnuCTCIPParamConfigIpv4Address_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 29, 1, 3),
    _OnuCTCIPParamConfigIpv4Address_Type()
)
onuCTCIPParamConfigIpv4Address.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuCTCIPParamConfigIpv4Address.setStatus("current")
_OnuCTCIPParamConfigIpv4Mask_Type = IpAddress
_OnuCTCIPParamConfigIpv4Mask_Object = MibTableColumn
onuCTCIPParamConfigIpv4Mask = _OnuCTCIPParamConfigIpv4Mask_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 29, 1, 4),
    _OnuCTCIPParamConfigIpv4Mask_Type()
)
onuCTCIPParamConfigIpv4Mask.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuCTCIPParamConfigIpv4Mask.setStatus("current")
_OnuCTCIPParamConfigIpv4GateWay_Type = IpAddress
_OnuCTCIPParamConfigIpv4GateWay_Object = MibTableColumn
onuCTCIPParamConfigIpv4GateWay = _OnuCTCIPParamConfigIpv4GateWay_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 29, 1, 5),
    _OnuCTCIPParamConfigIpv4GateWay_Type()
)
onuCTCIPParamConfigIpv4GateWay.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuCTCIPParamConfigIpv4GateWay.setStatus("current")
_OnuCTCIPParamConfigIpv6Address_Type = InetAddressIPv6
_OnuCTCIPParamConfigIpv6Address_Object = MibTableColumn
onuCTCIPParamConfigIpv6Address = _OnuCTCIPParamConfigIpv6Address_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 29, 1, 6),
    _OnuCTCIPParamConfigIpv6Address_Type()
)
onuCTCIPParamConfigIpv6Address.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuCTCIPParamConfigIpv6Address.setStatus("current")
_OnuCTCIPParamConfigIpv6Prefix_Type = Integer32
_OnuCTCIPParamConfigIpv6Prefix_Object = MibTableColumn
onuCTCIPParamConfigIpv6Prefix = _OnuCTCIPParamConfigIpv6Prefix_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 29, 1, 7),
    _OnuCTCIPParamConfigIpv6Prefix_Type()
)
onuCTCIPParamConfigIpv6Prefix.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuCTCIPParamConfigIpv6Prefix.setStatus("current")
_OnuCTCIPParamConfigIpv6GateWay_Type = InetAddressIPv6
_OnuCTCIPParamConfigIpv6GateWay_Object = MibTableColumn
onuCTCIPParamConfigIpv6GateWay = _OnuCTCIPParamConfigIpv6GateWay_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 29, 1, 8),
    _OnuCTCIPParamConfigIpv6GateWay_Type()
)
onuCTCIPParamConfigIpv6GateWay.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuCTCIPParamConfigIpv6GateWay.setStatus("current")


class _OnuCTCIPParamConfigCVLAN_Type(Integer32):
    """Custom type onuCTCIPParamConfigCVLAN based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueRangeConstraint(1, 4094),
    )


_OnuCTCIPParamConfigCVLAN_Type.__name__ = "Integer32"
_OnuCTCIPParamConfigCVLAN_Object = MibTableColumn
onuCTCIPParamConfigCVLAN = _OnuCTCIPParamConfigCVLAN_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 29, 1, 9),
    _OnuCTCIPParamConfigCVLAN_Type()
)
onuCTCIPParamConfigCVLAN.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuCTCIPParamConfigCVLAN.setStatus("current")


class _OnuCTCIPParamConfigSVLAN_Type(Integer32):
    """Custom type onuCTCIPParamConfigSVLAN based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueRangeConstraint(0, 4094),
    )


_OnuCTCIPParamConfigSVLAN_Type.__name__ = "Integer32"
_OnuCTCIPParamConfigSVLAN_Object = MibTableColumn
onuCTCIPParamConfigSVLAN = _OnuCTCIPParamConfigSVLAN_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 29, 1, 10),
    _OnuCTCIPParamConfigSVLAN_Type()
)
onuCTCIPParamConfigSVLAN.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuCTCIPParamConfigSVLAN.setStatus("current")


class _OnuCTCIPParamConfigPriority_Type(Integer32):
    """Custom type onuCTCIPParamConfigPriority based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueRangeConstraint(0, 7),
    )


_OnuCTCIPParamConfigPriority_Type.__name__ = "Integer32"
_OnuCTCIPParamConfigPriority_Object = MibTableColumn
onuCTCIPParamConfigPriority = _OnuCTCIPParamConfigPriority_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 29, 1, 11),
    _OnuCTCIPParamConfigPriority_Type()
)
onuCTCIPParamConfigPriority.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuCTCIPParamConfigPriority.setStatus("current")
_OnuCTCIPParamConfigRowStatus_Type = RowStatus
_OnuCTCIPParamConfigRowStatus_Object = MibTableColumn
onuCTCIPParamConfigRowStatus = _OnuCTCIPParamConfigRowStatus_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 29, 1, 12),
    _OnuCTCIPParamConfigRowStatus_Type()
)
onuCTCIPParamConfigRowStatus.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    onuCTCIPParamConfigRowStatus.setStatus("current")
_OnuCATVConfigTable_Object = MibTable
onuCATVConfigTable = _OnuCATVConfigTable_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 30)
)
if mibBuilder.loadTexts:
    onuCATVConfigTable.setStatus("current")
_OnuCATVConfigEntry_Object = MibTableRow
onuCATVConfigEntry = _OnuCATVConfigEntry_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 30, 1)
)
onuCATVConfigEntry.setIndexNames(
    (0, "NMS-EPON-ONU", "ifCATVIndex"),
)
if mibBuilder.loadTexts:
    onuCATVConfigEntry.setStatus("current")
_IfCATVIndex_Type = Integer32
_IfCATVIndex_Object = MibTableColumn
ifCATVIndex = _IfCATVIndex_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 30, 1, 1),
    _IfCATVIndex_Type()
)
ifCATVIndex.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    ifCATVIndex.setStatus("current")


class _IfCATVAdminStatus_Type(Integer32):
    """Custom type ifCATVAdminStatus based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(1,
              2)
        )
    )
    namedValues = NamedValues(
        *(("up", 1),
          ("down", 2))
    )


_IfCATVAdminStatus_Type.__name__ = "Integer32"
_IfCATVAdminStatus_Object = MibTableColumn
ifCATVAdminStatus = _IfCATVAdminStatus_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 30, 1, 2),
    _IfCATVAdminStatus_Type()
)
ifCATVAdminStatus.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    ifCATVAdminStatus.setStatus("current")
_OnuCATVRxPowerTable_Object = MibTable
onuCATVRxPowerTable = _OnuCATVRxPowerTable_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 31)
)
if mibBuilder.loadTexts:
    onuCATVRxPowerTable.setStatus("current")
_OnuCATVRxPowerEntry_Object = MibTableRow
onuCATVRxPowerEntry = _OnuCATVRxPowerEntry_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 31, 1)
)
onuCATVRxPowerEntry.setIndexNames(
    (0, "NMS-EPON-ONU", "ifCATVRxIndex"),
)
if mibBuilder.loadTexts:
    onuCATVRxPowerEntry.setStatus("current")
_IfCATVRxIndex_Type = Integer32
_IfCATVRxIndex_Object = MibTableColumn
ifCATVRxIndex = _IfCATVRxIndex_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 31, 1, 1),
    _IfCATVRxIndex_Type()
)
ifCATVRxIndex.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    ifCATVRxIndex.setStatus("current")
_RxPower_Type = Integer32
_RxPower_Object = MibTableColumn
rxPower = _RxPower_Object(
    (1, 3, 6, 1, 4, 1, 3320, 101, 10, 31, 1, 2),
    _RxPower_Type()
)
rxPower.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    rxPower.setStatus("current")

# Managed Objects groups


# Notification objects


# Notifications groups


# Agent capabilities


# Module compliance


# Export all MIB objects to the MIB builder

mibBuilder.exportSymbols(
    "NMS-EPON-ONU",
    **{"nmsEponOnu": nmsEponOnu,
       "nmsepononuTable": nmsepononuTable,
       "nmsEponOnuEntry": nmsEponOnuEntry,
       "onuVendorID": onuVendorID,
       "onuModuleID": onuModuleID,
       "onuID": onuID,
       "onuHardwareVersion": onuHardwareVersion,
       "onuSoftwareVersion": onuSoftwareVersion,
       "onuFirmwareVersion": onuFirmwareVersion,
       "onuChipVendorID": onuChipVendorID,
       "onuChipModuleID": onuChipModuleID,
       "onuChipRevision": onuChipRevision,
       "onuIcVersion": onuIcVersion,
       "onuGePortCount": onuGePortCount,
       "onuGePortDistributing": onuGePortDistributing,
       "onuFePortCount": onuFePortCount,
       "onuFePortDistributing": onuFePortDistributing,
       "onuPotsPortCount": onuPotsPortCount,
       "onuE1PortCount": onuE1PortCount,
       "onuUsQueueCount": onuUsQueueCount,
       "onuUsQueueMaxCount": onuUsQueueMaxCount,
       "onuDsQueueCount": onuDsQueueCount,
       "onuDsQueueMaxCount": onuDsQueueMaxCount,
       "onuIsBakupBattery": onuIsBakupBattery,
       "onuADSL2PlusPortCount": onuADSL2PlusPortCount,
       "onuVDSL2PortCount": onuVDSL2PortCount,
       "onuLLIDCount": onuLLIDCount,
       "onuStatus": onuStatus,
       "onuDistance": onuDistance,
       "onuBindStatus": onuBindStatus,
       "onuReset": onuReset,
       "onuUpdateImage": onuUpdateImage,
       "onuUpdateEepromImage": onuUpdateEepromImage,
       "onuEncryptionStatus": onuEncryptionStatus,
       "onuEncryptionMode": onuEncryptionMode,
       "onuIgmpSnoopingStatus": onuIgmpSnoopingStatus,
       "onuMcstMode": onuMcstMode,
       "onuAFastLeaveAbility": onuAFastLeaveAbility,
       "onuAcFastLeaveAdminControl": onuAcFastLeaveAdminControl,
       "onuAFastLeaveAdminState": onuAFastLeaveAdminState,
       "onuInFecStatus": onuInFecStatus,
       "onuOutFecStatus": onuOutFecStatus,
       "onuIfProtectedStatus": onuIfProtectedStatus,
       "onuSehedulePolicy": onuSehedulePolicy,
       "onuDynamicMacLearningStatus": onuDynamicMacLearningStatus,
       "onuDynamicMacAgingTime": onuDynamicMacAgingTime,
       "onuStaticMacAddress": onuStaticMacAddress,
       "onuStaticMacAddressPortBitmap": onuStaticMacAddressPortBitmap,
       "onuStaticMacAddressConfigRowStatus": onuStaticMacAddressConfigRowStatus,
       "onuClearDynamicMacAddressByMac": onuClearDynamicMacAddressByMac,
       "onuClearDynamicMacAddressByPort": onuClearDynamicMacAddressByPort,
       "onuPriorityQueueMapping": onuPriorityQueueMapping,
       "onuVlanMode": onuVlanMode,
       "onuIpAddressMode": onuIpAddressMode,
       "onuStaticIpAddress": onuStaticIpAddress,
       "onuStaticIpMask": onuStaticIpMask,
       "onuStaticIpGateway": onuStaticIpGateway,
       "onuMgmtVlan": onuMgmtVlan,
       "onuStaticIpAddressRowStatus": onuStaticIpAddressRowStatus,
       "onuCIR": onuCIR,
       "onuCBS": onuCBS,
       "onuEBS": onuEBS,
       "onuIfMacACL": onuIfMacACL,
       "onuIfIpACL": onuIfIpACL,
       "onuVlans": onuVlans,
       "onuActivePonDiid": onuActivePonDiid,
       "onuPonPortCount": onuPonPortCount,
       "onuActivePonPortIndex": onuActivePonPortIndex,
       "onuSerialPortWorkMode": onuSerialPortWorkMode,
       "onuSerialPortWorkPort": onuSerialPortWorkPort,
       "onuSerialWorkModeRowStatus": onuSerialWorkModeRowStatus,
       "onuRemoteServerIpAddrIndex": onuRemoteServerIpAddrIndex,
       "onuPeerOLTIpAddr": onuPeerOLTIpAddr,
       "onuPeerPONIndex": onuPeerPONIndex,
       "onuSerialPortCount": onuSerialPortCount,
       "onuBakupPonStatus": onuBakupPonStatus,
       "onuCurrentPONInUse": onuCurrentPONInUse,
       "onuCurrentPONMAC": onuCurrentPONMAC,
       "onuPeerPONDiid": onuPeerPONDiid,
       "onuPeerPONMAC": onuPeerPONMAC,
       "onuConfigurablePortDiid": onuConfigurablePortDiid,
       "onuAliveTime": onuAliveTime,
       "nmsepononuPonSwitchTable": nmsepononuPonSwitchTable,
       "nmsEponOnuPonSwitchEntry": nmsEponOnuPonSwitchEntry,
       "ifIndex": ifIndex,
       "operType": operType,
       "nmsepononucap2Table": nmsepononucap2Table,
       "nmsEponOnuCap2Entry": nmsEponOnuCap2Entry,
       "cap2OnuType": cap2OnuType,
       "cap2Multillid": cap2Multillid,
       "cap2ProtectionType": cap2ProtectionType,
       "cap2NumPONIf": cap2NumPONIf,
       "cap2NumSlot": cap2NumSlot,
       "cap2NumIfType": cap2NumIfType,
       "cap2NumGEPorts": cap2NumGEPorts,
       "cap2NumFEPorts": cap2NumFEPorts,
       "cap2NumVoIPPorts": cap2NumVoIPPorts,
       "cap2NumTDMPorts": cap2NumTDMPorts,
       "cap2NumADSL2Ports": cap2NumADSL2Ports,
       "cap2NumVDSL2Ports": cap2NumVDSL2Ports,
       "cap2NumWLANPorts": cap2NumWLANPorts,
       "cap2NumUSBPorts": cap2NumUSBPorts,
       "cap2NumCATVRFPorts": cap2NumCATVRFPorts,
       "cap2NumSerialPorts": cap2NumSerialPorts,
       "cap2BatteryBackup": cap2BatteryBackup,
       "nmsepononusnmpTable": nmsepononusnmpTable,
       "nmsEponOnuSnmpEntry": nmsEponOnuSnmpEntry,
       "onuMacAddr": onuMacAddr,
       "onuIpAddr": onuIpAddr,
       "onuCommRo": onuCommRo,
       "onuCommRw": onuCommRw,
       "onuSnmpPort": onuSnmpPort,
       "onuSnmpTrapPort": onuSnmpTrapPort,
       "onuSnmpVersion": onuSnmpVersion,
       "onuSnmpTrapVersion": onuSnmpTrapVersion,
       "onuSnmpTrapHost": onuSnmpTrapHost,
       "nmsepononuopticalportTable": nmsepononuopticalportTable,
       "nmsEponOnuOpticalPortEntry": nmsEponOnuOpticalPortEntry,
       "opIfIndex": opIfIndex,
       "opModuleTemp": opModuleTemp,
       "opModuleVolt": opModuleVolt,
       "opModuleCurrent": opModuleCurrent,
       "opModuleRxPower": opModuleRxPower,
       "opModuleTxPower": opModuleTxPower,
       "onuIPParamGetTable": onuIPParamGetTable,
       "onuIPParamGetEntry": onuIPParamGetEntry,
       "onuIfIndex": onuIfIndex,
       "ipVersion": ipVersion,
       "ipv4Address": ipv4Address,
       "ipv4Mask": ipv4Mask,
       "ipv4GateWay": ipv4GateWay,
       "ipv6Address": ipv6Address,
       "ipv6Prefix": ipv6Prefix,
       "ipv6GateWay": ipv6GateWay,
       "cvlan": cvlan,
       "svlan": svlan,
       "priority": priority,
       "onuCTCIPParamConfigTable": onuCTCIPParamConfigTable,
       "onuCTCIPParamConfigEntry": onuCTCIPParamConfigEntry,
       "onuCTCIPParamConfigIfIndex": onuCTCIPParamConfigIfIndex,
       "onuCTCIPParamConfigIpVersion": onuCTCIPParamConfigIpVersion,
       "onuCTCIPParamConfigIpv4Address": onuCTCIPParamConfigIpv4Address,
       "onuCTCIPParamConfigIpv4Mask": onuCTCIPParamConfigIpv4Mask,
       "onuCTCIPParamConfigIpv4GateWay": onuCTCIPParamConfigIpv4GateWay,
       "onuCTCIPParamConfigIpv6Address": onuCTCIPParamConfigIpv6Address,
       "onuCTCIPParamConfigIpv6Prefix": onuCTCIPParamConfigIpv6Prefix,
       "onuCTCIPParamConfigIpv6GateWay": onuCTCIPParamConfigIpv6GateWay,
       "onuCTCIPParamConfigCVLAN": onuCTCIPParamConfigCVLAN,
       "onuCTCIPParamConfigSVLAN": onuCTCIPParamConfigSVLAN,
       "onuCTCIPParamConfigPriority": onuCTCIPParamConfigPriority,
       "onuCTCIPParamConfigRowStatus": onuCTCIPParamConfigRowStatus,
       "onuCATVConfigTable": onuCATVConfigTable,
       "onuCATVConfigEntry": onuCATVConfigEntry,
       "ifCATVIndex": ifCATVIndex,
       "ifCATVAdminStatus": ifCATVAdminStatus,
       "onuCATVRxPowerTable": onuCATVRxPowerTable,
       "onuCATVRxPowerEntry": onuCATVRxPowerEntry,
       "ifCATVRxIndex": ifCATVRxIndex,
       "rxPower": rxPower}
)
