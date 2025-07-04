# SNMP MIB module (SNMPv2-MIB) expressed in pysnmp data model.
#
# This Python module is designed to be imported and executed by the
# pysnmp library.
#
# See https://www.pysnmp.com/pysnmp for further information.
#
# Notes
# -----
# ASN.1 source file://app/mibs/SNMPv2-MIB
# Produced by pysmi-1.6.1 at Wed Jul  2 15:34:07 2025
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

(ModuleCompliance,
 NotificationGroup,
 ObjectGroup) = mibBuilder.importSymbols(
    "SNMPv2-CONF",
    "ModuleCompliance",
    "NotificationGroup",
    "ObjectGroup")

(Bits,
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
 iso,
 mib_2,
 snmpModules) = mibBuilder.importSymbols(
    "SNMPv2-SMI",
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
    "iso",
    "mib-2",
    "snmpModules")

(DisplayString,
 PhysAddress,
 TextualConvention,
 TestAndIncr,
 TimeStamp) = mibBuilder.importSymbols(
    "SNMPv2-TC",
    "DisplayString",
    "PhysAddress",
    "TextualConvention",
    "TestAndIncr",
    "TimeStamp")


# MODULE-IDENTITY

snmpMIB = ModuleIdentity(
    (1, 3, 6, 1, 6, 3, 1)
)
if mibBuilder.loadTexts:
    snmpMIB.setRevisions(
        ("2002-10-16 00:00",
         "1995-11-09 00:00",
         "1993-04-01 00:00")
    )


# Types definitions


# TEXTUAL-CONVENTIONS



# MIB Managed Objects in the order of their OIDs

_System_ObjectIdentity = ObjectIdentity
system = _System_ObjectIdentity(
    (1, 3, 6, 1, 2, 1, 1)
)


class _SysDescr_Type(DisplayString):
    """Custom type sysDescr based on DisplayString"""
    subtypeSpec = DisplayString.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueSizeConstraint(0, 255),
    )


_SysDescr_Type.__name__ = "DisplayString"
_SysDescr_Object = MibScalar
sysDescr = _SysDescr_Object(
    (1, 3, 6, 1, 2, 1, 1, 1),
    _SysDescr_Type()
)
sysDescr.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    sysDescr.setStatus("current")
_SysObjectID_Type = ObjectIdentifier
_SysObjectID_Object = MibScalar
sysObjectID = _SysObjectID_Object(
    (1, 3, 6, 1, 2, 1, 1, 2),
    _SysObjectID_Type()
)
sysObjectID.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    sysObjectID.setStatus("current")
_SysUpTime_Type = TimeTicks
_SysUpTime_Object = MibScalar
sysUpTime = _SysUpTime_Object(
    (1, 3, 6, 1, 2, 1, 1, 3),
    _SysUpTime_Type()
)
sysUpTime.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    sysUpTime.setStatus("current")


class _SysContact_Type(DisplayString):
    """Custom type sysContact based on DisplayString"""
    subtypeSpec = DisplayString.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueSizeConstraint(0, 255),
    )


_SysContact_Type.__name__ = "DisplayString"
_SysContact_Object = MibScalar
sysContact = _SysContact_Object(
    (1, 3, 6, 1, 2, 1, 1, 4),
    _SysContact_Type()
)
sysContact.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    sysContact.setStatus("current")


class _SysName_Type(DisplayString):
    """Custom type sysName based on DisplayString"""
    subtypeSpec = DisplayString.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueSizeConstraint(0, 255),
    )


_SysName_Type.__name__ = "DisplayString"
_SysName_Object = MibScalar
sysName = _SysName_Object(
    (1, 3, 6, 1, 2, 1, 1, 5),
    _SysName_Type()
)
sysName.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    sysName.setStatus("current")


class _SysLocation_Type(DisplayString):
    """Custom type sysLocation based on DisplayString"""
    subtypeSpec = DisplayString.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueSizeConstraint(0, 255),
    )


_SysLocation_Type.__name__ = "DisplayString"
_SysLocation_Object = MibScalar
sysLocation = _SysLocation_Object(
    (1, 3, 6, 1, 2, 1, 1, 6),
    _SysLocation_Type()
)
sysLocation.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    sysLocation.setStatus("current")


class _SysServices_Type(Integer32):
    """Custom type sysServices based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueRangeConstraint(0, 127),
    )


_SysServices_Type.__name__ = "Integer32"
_SysServices_Object = MibScalar
sysServices = _SysServices_Object(
    (1, 3, 6, 1, 2, 1, 1, 7),
    _SysServices_Type()
)
sysServices.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    sysServices.setStatus("current")
_SysORLastChange_Type = TimeStamp
_SysORLastChange_Object = MibScalar
sysORLastChange = _SysORLastChange_Object(
    (1, 3, 6, 1, 2, 1, 1, 8),
    _SysORLastChange_Type()
)
sysORLastChange.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    sysORLastChange.setStatus("current")
_SysORTable_Object = MibTable
sysORTable = _SysORTable_Object(
    (1, 3, 6, 1, 2, 1, 1, 9)
)
if mibBuilder.loadTexts:
    sysORTable.setStatus("current")
_SysOREntry_Object = MibTableRow
sysOREntry = _SysOREntry_Object(
    (1, 3, 6, 1, 2, 1, 1, 9, 1)
)
sysOREntry.setIndexNames(
    (0, "SNMPv2-MIB", "sysORIndex"),
)
if mibBuilder.loadTexts:
    sysOREntry.setStatus("current")


class _SysORIndex_Type(Integer32):
    """Custom type sysORIndex based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueRangeConstraint(1, 2147483647),
    )


_SysORIndex_Type.__name__ = "Integer32"
_SysORIndex_Object = MibTableColumn
sysORIndex = _SysORIndex_Object(
    (1, 3, 6, 1, 2, 1, 1, 9, 1, 1),
    _SysORIndex_Type()
)
sysORIndex.setMaxAccess("not-accessible")
if mibBuilder.loadTexts:
    sysORIndex.setStatus("current")
_SysORID_Type = ObjectIdentifier
_SysORID_Object = MibTableColumn
sysORID = _SysORID_Object(
    (1, 3, 6, 1, 2, 1, 1, 9, 1, 2),
    _SysORID_Type()
)
sysORID.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    sysORID.setStatus("current")
_SysORDescr_Type = DisplayString
_SysORDescr_Object = MibTableColumn
sysORDescr = _SysORDescr_Object(
    (1, 3, 6, 1, 2, 1, 1, 9, 1, 3),
    _SysORDescr_Type()
)
sysORDescr.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    sysORDescr.setStatus("current")
_SysORUpTime_Type = TimeStamp
_SysORUpTime_Object = MibTableColumn
sysORUpTime = _SysORUpTime_Object(
    (1, 3, 6, 1, 2, 1, 1, 9, 1, 4),
    _SysORUpTime_Type()
)
sysORUpTime.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    sysORUpTime.setStatus("current")
_Snmp_ObjectIdentity = ObjectIdentity
snmp = _Snmp_ObjectIdentity(
    (1, 3, 6, 1, 2, 1, 11)
)
_SnmpInPkts_Type = Counter32
_SnmpInPkts_Object = MibScalar
snmpInPkts = _SnmpInPkts_Object(
    (1, 3, 6, 1, 2, 1, 11, 1),
    _SnmpInPkts_Type()
)
snmpInPkts.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpInPkts.setStatus("current")
_SnmpOutPkts_Type = Counter32
_SnmpOutPkts_Object = MibScalar
snmpOutPkts = _SnmpOutPkts_Object(
    (1, 3, 6, 1, 2, 1, 11, 2),
    _SnmpOutPkts_Type()
)
snmpOutPkts.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpOutPkts.setStatus("obsolete")
_SnmpInBadVersions_Type = Counter32
_SnmpInBadVersions_Object = MibScalar
snmpInBadVersions = _SnmpInBadVersions_Object(
    (1, 3, 6, 1, 2, 1, 11, 3),
    _SnmpInBadVersions_Type()
)
snmpInBadVersions.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpInBadVersions.setStatus("current")
_SnmpInBadCommunityNames_Type = Counter32
_SnmpInBadCommunityNames_Object = MibScalar
snmpInBadCommunityNames = _SnmpInBadCommunityNames_Object(
    (1, 3, 6, 1, 2, 1, 11, 4),
    _SnmpInBadCommunityNames_Type()
)
snmpInBadCommunityNames.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpInBadCommunityNames.setStatus("current")
_SnmpInBadCommunityUses_Type = Counter32
_SnmpInBadCommunityUses_Object = MibScalar
snmpInBadCommunityUses = _SnmpInBadCommunityUses_Object(
    (1, 3, 6, 1, 2, 1, 11, 5),
    _SnmpInBadCommunityUses_Type()
)
snmpInBadCommunityUses.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpInBadCommunityUses.setStatus("current")
_SnmpInASNParseErrs_Type = Counter32
_SnmpInASNParseErrs_Object = MibScalar
snmpInASNParseErrs = _SnmpInASNParseErrs_Object(
    (1, 3, 6, 1, 2, 1, 11, 6),
    _SnmpInASNParseErrs_Type()
)
snmpInASNParseErrs.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpInASNParseErrs.setStatus("current")
_SnmpInTooBigs_Type = Counter32
_SnmpInTooBigs_Object = MibScalar
snmpInTooBigs = _SnmpInTooBigs_Object(
    (1, 3, 6, 1, 2, 1, 11, 8),
    _SnmpInTooBigs_Type()
)
snmpInTooBigs.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpInTooBigs.setStatus("obsolete")
_SnmpInNoSuchNames_Type = Counter32
_SnmpInNoSuchNames_Object = MibScalar
snmpInNoSuchNames = _SnmpInNoSuchNames_Object(
    (1, 3, 6, 1, 2, 1, 11, 9),
    _SnmpInNoSuchNames_Type()
)
snmpInNoSuchNames.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpInNoSuchNames.setStatus("obsolete")
_SnmpInBadValues_Type = Counter32
_SnmpInBadValues_Object = MibScalar
snmpInBadValues = _SnmpInBadValues_Object(
    (1, 3, 6, 1, 2, 1, 11, 10),
    _SnmpInBadValues_Type()
)
snmpInBadValues.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpInBadValues.setStatus("obsolete")
_SnmpInReadOnlys_Type = Counter32
_SnmpInReadOnlys_Object = MibScalar
snmpInReadOnlys = _SnmpInReadOnlys_Object(
    (1, 3, 6, 1, 2, 1, 11, 11),
    _SnmpInReadOnlys_Type()
)
snmpInReadOnlys.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpInReadOnlys.setStatus("obsolete")
_SnmpInGenErrs_Type = Counter32
_SnmpInGenErrs_Object = MibScalar
snmpInGenErrs = _SnmpInGenErrs_Object(
    (1, 3, 6, 1, 2, 1, 11, 12),
    _SnmpInGenErrs_Type()
)
snmpInGenErrs.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpInGenErrs.setStatus("obsolete")
_SnmpInTotalReqVars_Type = Counter32
_SnmpInTotalReqVars_Object = MibScalar
snmpInTotalReqVars = _SnmpInTotalReqVars_Object(
    (1, 3, 6, 1, 2, 1, 11, 13),
    _SnmpInTotalReqVars_Type()
)
snmpInTotalReqVars.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpInTotalReqVars.setStatus("obsolete")
_SnmpInTotalSetVars_Type = Counter32
_SnmpInTotalSetVars_Object = MibScalar
snmpInTotalSetVars = _SnmpInTotalSetVars_Object(
    (1, 3, 6, 1, 2, 1, 11, 14),
    _SnmpInTotalSetVars_Type()
)
snmpInTotalSetVars.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpInTotalSetVars.setStatus("obsolete")
_SnmpInGetRequests_Type = Counter32
_SnmpInGetRequests_Object = MibScalar
snmpInGetRequests = _SnmpInGetRequests_Object(
    (1, 3, 6, 1, 2, 1, 11, 15),
    _SnmpInGetRequests_Type()
)
snmpInGetRequests.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpInGetRequests.setStatus("obsolete")
_SnmpInGetNexts_Type = Counter32
_SnmpInGetNexts_Object = MibScalar
snmpInGetNexts = _SnmpInGetNexts_Object(
    (1, 3, 6, 1, 2, 1, 11, 16),
    _SnmpInGetNexts_Type()
)
snmpInGetNexts.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpInGetNexts.setStatus("obsolete")
_SnmpInSetRequests_Type = Counter32
_SnmpInSetRequests_Object = MibScalar
snmpInSetRequests = _SnmpInSetRequests_Object(
    (1, 3, 6, 1, 2, 1, 11, 17),
    _SnmpInSetRequests_Type()
)
snmpInSetRequests.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpInSetRequests.setStatus("obsolete")
_SnmpInGetResponses_Type = Counter32
_SnmpInGetResponses_Object = MibScalar
snmpInGetResponses = _SnmpInGetResponses_Object(
    (1, 3, 6, 1, 2, 1, 11, 18),
    _SnmpInGetResponses_Type()
)
snmpInGetResponses.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpInGetResponses.setStatus("obsolete")
_SnmpInTraps_Type = Counter32
_SnmpInTraps_Object = MibScalar
snmpInTraps = _SnmpInTraps_Object(
    (1, 3, 6, 1, 2, 1, 11, 19),
    _SnmpInTraps_Type()
)
snmpInTraps.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpInTraps.setStatus("obsolete")
_SnmpOutTooBigs_Type = Counter32
_SnmpOutTooBigs_Object = MibScalar
snmpOutTooBigs = _SnmpOutTooBigs_Object(
    (1, 3, 6, 1, 2, 1, 11, 20),
    _SnmpOutTooBigs_Type()
)
snmpOutTooBigs.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpOutTooBigs.setStatus("obsolete")
_SnmpOutNoSuchNames_Type = Counter32
_SnmpOutNoSuchNames_Object = MibScalar
snmpOutNoSuchNames = _SnmpOutNoSuchNames_Object(
    (1, 3, 6, 1, 2, 1, 11, 21),
    _SnmpOutNoSuchNames_Type()
)
snmpOutNoSuchNames.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpOutNoSuchNames.setStatus("obsolete")
_SnmpOutBadValues_Type = Counter32
_SnmpOutBadValues_Object = MibScalar
snmpOutBadValues = _SnmpOutBadValues_Object(
    (1, 3, 6, 1, 2, 1, 11, 22),
    _SnmpOutBadValues_Type()
)
snmpOutBadValues.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpOutBadValues.setStatus("obsolete")
_SnmpOutGenErrs_Type = Counter32
_SnmpOutGenErrs_Object = MibScalar
snmpOutGenErrs = _SnmpOutGenErrs_Object(
    (1, 3, 6, 1, 2, 1, 11, 24),
    _SnmpOutGenErrs_Type()
)
snmpOutGenErrs.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpOutGenErrs.setStatus("obsolete")
_SnmpOutGetRequests_Type = Counter32
_SnmpOutGetRequests_Object = MibScalar
snmpOutGetRequests = _SnmpOutGetRequests_Object(
    (1, 3, 6, 1, 2, 1, 11, 25),
    _SnmpOutGetRequests_Type()
)
snmpOutGetRequests.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpOutGetRequests.setStatus("obsolete")
_SnmpOutGetNexts_Type = Counter32
_SnmpOutGetNexts_Object = MibScalar
snmpOutGetNexts = _SnmpOutGetNexts_Object(
    (1, 3, 6, 1, 2, 1, 11, 26),
    _SnmpOutGetNexts_Type()
)
snmpOutGetNexts.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpOutGetNexts.setStatus("obsolete")
_SnmpOutSetRequests_Type = Counter32
_SnmpOutSetRequests_Object = MibScalar
snmpOutSetRequests = _SnmpOutSetRequests_Object(
    (1, 3, 6, 1, 2, 1, 11, 27),
    _SnmpOutSetRequests_Type()
)
snmpOutSetRequests.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpOutSetRequests.setStatus("obsolete")
_SnmpOutGetResponses_Type = Counter32
_SnmpOutGetResponses_Object = MibScalar
snmpOutGetResponses = _SnmpOutGetResponses_Object(
    (1, 3, 6, 1, 2, 1, 11, 28),
    _SnmpOutGetResponses_Type()
)
snmpOutGetResponses.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpOutGetResponses.setStatus("obsolete")
_SnmpOutTraps_Type = Counter32
_SnmpOutTraps_Object = MibScalar
snmpOutTraps = _SnmpOutTraps_Object(
    (1, 3, 6, 1, 2, 1, 11, 29),
    _SnmpOutTraps_Type()
)
snmpOutTraps.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpOutTraps.setStatus("obsolete")


class _SnmpEnableAuthenTraps_Type(Integer32):
    """Custom type snmpEnableAuthenTraps based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(1,
              2)
        )
    )
    namedValues = NamedValues(
        *(("enabled", 1),
          ("disabled", 2))
    )


_SnmpEnableAuthenTraps_Type.__name__ = "Integer32"
_SnmpEnableAuthenTraps_Object = MibScalar
snmpEnableAuthenTraps = _SnmpEnableAuthenTraps_Object(
    (1, 3, 6, 1, 2, 1, 11, 30),
    _SnmpEnableAuthenTraps_Type()
)
snmpEnableAuthenTraps.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    snmpEnableAuthenTraps.setStatus("current")
_SnmpSilentDrops_Type = Counter32
_SnmpSilentDrops_Object = MibScalar
snmpSilentDrops = _SnmpSilentDrops_Object(
    (1, 3, 6, 1, 2, 1, 11, 31),
    _SnmpSilentDrops_Type()
)
snmpSilentDrops.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpSilentDrops.setStatus("current")
_SnmpProxyDrops_Type = Counter32
_SnmpProxyDrops_Object = MibScalar
snmpProxyDrops = _SnmpProxyDrops_Object(
    (1, 3, 6, 1, 2, 1, 11, 32),
    _SnmpProxyDrops_Type()
)
snmpProxyDrops.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    snmpProxyDrops.setStatus("current")
_SnmpMIBObjects_ObjectIdentity = ObjectIdentity
snmpMIBObjects = _SnmpMIBObjects_ObjectIdentity(
    (1, 3, 6, 1, 6, 3, 1, 1)
)
_SnmpTrap_ObjectIdentity = ObjectIdentity
snmpTrap = _SnmpTrap_ObjectIdentity(
    (1, 3, 6, 1, 6, 3, 1, 1, 4)
)
_SnmpTrapOID_Type = ObjectIdentifier
_SnmpTrapOID_Object = MibScalar
snmpTrapOID = _SnmpTrapOID_Object(
    (1, 3, 6, 1, 6, 3, 1, 1, 4, 1),
    _SnmpTrapOID_Type()
)
snmpTrapOID.setMaxAccess("accessible-for-notify")
if mibBuilder.loadTexts:
    snmpTrapOID.setStatus("current")
_SnmpTrapEnterprise_Type = ObjectIdentifier
_SnmpTrapEnterprise_Object = MibScalar
snmpTrapEnterprise = _SnmpTrapEnterprise_Object(
    (1, 3, 6, 1, 6, 3, 1, 1, 4, 3),
    _SnmpTrapEnterprise_Type()
)
snmpTrapEnterprise.setMaxAccess("accessible-for-notify")
if mibBuilder.loadTexts:
    snmpTrapEnterprise.setStatus("current")
_SnmpTraps_ObjectIdentity = ObjectIdentity
snmpTraps = _SnmpTraps_ObjectIdentity(
    (1, 3, 6, 1, 6, 3, 1, 1, 5)
)
_SnmpSet_ObjectIdentity = ObjectIdentity
snmpSet = _SnmpSet_ObjectIdentity(
    (1, 3, 6, 1, 6, 3, 1, 1, 6)
)
_SnmpSetSerialNo_Type = TestAndIncr
_SnmpSetSerialNo_Object = MibScalar
snmpSetSerialNo = _SnmpSetSerialNo_Object(
    (1, 3, 6, 1, 6, 3, 1, 1, 6, 1),
    _SnmpSetSerialNo_Type()
)
snmpSetSerialNo.setMaxAccess("read-write")
if mibBuilder.loadTexts:
    snmpSetSerialNo.setStatus("current")
_SnmpMIBConformance_ObjectIdentity = ObjectIdentity
snmpMIBConformance = _SnmpMIBConformance_ObjectIdentity(
    (1, 3, 6, 1, 6, 3, 1, 2)
)
_SnmpMIBCompliances_ObjectIdentity = ObjectIdentity
snmpMIBCompliances = _SnmpMIBCompliances_ObjectIdentity(
    (1, 3, 6, 1, 6, 3, 1, 2, 1)
)
_SnmpMIBGroups_ObjectIdentity = ObjectIdentity
snmpMIBGroups = _SnmpMIBGroups_ObjectIdentity(
    (1, 3, 6, 1, 6, 3, 1, 2, 2)
)

# Managed Objects groups

snmpSetGroup = ObjectGroup(
    (1, 3, 6, 1, 6, 3, 1, 2, 2, 5)
)
snmpSetGroup.setObjects(
    ("SNMPv2-MIB", "snmpSetSerialNo")
)
if mibBuilder.loadTexts:
    snmpSetGroup.setStatus("current")

systemGroup = ObjectGroup(
    (1, 3, 6, 1, 6, 3, 1, 2, 2, 6)
)
systemGroup.setObjects(
      *(("SNMPv2-MIB", "sysDescr"),
        ("SNMPv2-MIB", "sysObjectID"),
        ("SNMPv2-MIB", "sysUpTime"),
        ("SNMPv2-MIB", "sysContact"),
        ("SNMPv2-MIB", "sysName"),
        ("SNMPv2-MIB", "sysLocation"),
        ("SNMPv2-MIB", "sysServices"),
        ("SNMPv2-MIB", "sysORLastChange"),
        ("SNMPv2-MIB", "sysORID"),
        ("SNMPv2-MIB", "sysORUpTime"),
        ("SNMPv2-MIB", "sysORDescr"))
)
if mibBuilder.loadTexts:
    systemGroup.setStatus("current")

snmpGroup = ObjectGroup(
    (1, 3, 6, 1, 6, 3, 1, 2, 2, 8)
)
snmpGroup.setObjects(
      *(("SNMPv2-MIB", "snmpInPkts"),
        ("SNMPv2-MIB", "snmpInBadVersions"),
        ("SNMPv2-MIB", "snmpInASNParseErrs"),
        ("SNMPv2-MIB", "snmpSilentDrops"),
        ("SNMPv2-MIB", "snmpProxyDrops"),
        ("SNMPv2-MIB", "snmpEnableAuthenTraps"))
)
if mibBuilder.loadTexts:
    snmpGroup.setStatus("current")

snmpCommunityGroup = ObjectGroup(
    (1, 3, 6, 1, 6, 3, 1, 2, 2, 9)
)
snmpCommunityGroup.setObjects(
      *(("SNMPv2-MIB", "snmpInBadCommunityNames"),
        ("SNMPv2-MIB", "snmpInBadCommunityUses"))
)
if mibBuilder.loadTexts:
    snmpCommunityGroup.setStatus("current")

snmpObsoleteGroup = ObjectGroup(
    (1, 3, 6, 1, 6, 3, 1, 2, 2, 10)
)
snmpObsoleteGroup.setObjects(
      *(("SNMPv2-MIB", "snmpOutPkts"),
        ("SNMPv2-MIB", "snmpInTooBigs"),
        ("SNMPv2-MIB", "snmpInNoSuchNames"),
        ("SNMPv2-MIB", "snmpInBadValues"),
        ("SNMPv2-MIB", "snmpInReadOnlys"),
        ("SNMPv2-MIB", "snmpInGenErrs"),
        ("SNMPv2-MIB", "snmpInTotalReqVars"),
        ("SNMPv2-MIB", "snmpInTotalSetVars"),
        ("SNMPv2-MIB", "snmpInGetRequests"),
        ("SNMPv2-MIB", "snmpInGetNexts"),
        ("SNMPv2-MIB", "snmpInSetRequests"),
        ("SNMPv2-MIB", "snmpInGetResponses"),
        ("SNMPv2-MIB", "snmpInTraps"),
        ("SNMPv2-MIB", "snmpOutTooBigs"),
        ("SNMPv2-MIB", "snmpOutNoSuchNames"),
        ("SNMPv2-MIB", "snmpOutBadValues"),
        ("SNMPv2-MIB", "snmpOutGenErrs"),
        ("SNMPv2-MIB", "snmpOutGetRequests"),
        ("SNMPv2-MIB", "snmpOutGetNexts"),
        ("SNMPv2-MIB", "snmpOutSetRequests"),
        ("SNMPv2-MIB", "snmpOutGetResponses"),
        ("SNMPv2-MIB", "snmpOutTraps"))
)
if mibBuilder.loadTexts:
    snmpObsoleteGroup.setStatus("obsolete")

snmpNotificationGroup = ObjectGroup(
    (1, 3, 6, 1, 6, 3, 1, 2, 2, 12)
)
snmpNotificationGroup.setObjects(
      *(("SNMPv2-MIB", "snmpTrapOID"),
        ("SNMPv2-MIB", "snmpTrapEnterprise"))
)
if mibBuilder.loadTexts:
    snmpNotificationGroup.setStatus("current")


# Notification objects

coldStart = NotificationType(
    (1, 3, 6, 1, 6, 3, 1, 1, 5, 1)
)
if mibBuilder.loadTexts:
    coldStart.setStatus(
        "current"
    )

warmStart = NotificationType(
    (1, 3, 6, 1, 6, 3, 1, 1, 5, 2)
)
if mibBuilder.loadTexts:
    warmStart.setStatus(
        "current"
    )

authenticationFailure = NotificationType(
    (1, 3, 6, 1, 6, 3, 1, 1, 5, 5)
)
if mibBuilder.loadTexts:
    authenticationFailure.setStatus(
        "current"
    )


# Notifications groups

snmpBasicNotificationsGroup = NotificationGroup(
    (1, 3, 6, 1, 6, 3, 1, 2, 2, 7)
)
snmpBasicNotificationsGroup.setObjects(
      *(("SNMPv2-MIB", "coldStart"),
        ("SNMPv2-MIB", "authenticationFailure"))
)
if mibBuilder.loadTexts:
    snmpBasicNotificationsGroup.setStatus(
        "current"
    )

snmpWarmStartNotificationGroup = NotificationGroup(
    (1, 3, 6, 1, 6, 3, 1, 2, 2, 11)
)
snmpWarmStartNotificationGroup.setObjects(
    ("SNMPv2-MIB", "warmStart")
)
if mibBuilder.loadTexts:
    snmpWarmStartNotificationGroup.setStatus(
        "current"
    )


# Agent capabilities


# Module compliance

snmpBasicCompliance = ModuleCompliance(
    (1, 3, 6, 1, 6, 3, 1, 2, 1, 2)
)
snmpBasicCompliance.setObjects(
      *(("SNMPv2-MIB", "snmpGroup"),
        ("SNMPv2-MIB", "snmpSetGroup"),
        ("SNMPv2-MIB", "systemGroup"),
        ("SNMPv2-MIB", "snmpBasicNotificationsGroup"),
        ("SNMPv2-MIB", "snmpCommunityGroup"))
)
if mibBuilder.loadTexts:
    snmpBasicCompliance.setStatus(
        "deprecated"
    )

snmpBasicComplianceRev2 = ModuleCompliance(
    (1, 3, 6, 1, 6, 3, 1, 2, 1, 3)
)
snmpBasicComplianceRev2.setObjects(
      *(("SNMPv2-MIB", "snmpGroup"),
        ("SNMPv2-MIB", "snmpSetGroup"),
        ("SNMPv2-MIB", "systemGroup"),
        ("SNMPv2-MIB", "snmpBasicNotificationsGroup"),
        ("SNMPv2-MIB", "snmpCommunityGroup"),
        ("SNMPv2-MIB", "snmpWarmStartNotificationGroup"))
)
if mibBuilder.loadTexts:
    snmpBasicComplianceRev2.setStatus(
        "current"
    )


# Export all MIB objects to the MIB builder

mibBuilder.exportSymbols(
    "SNMPv2-MIB",
    **{"system": system,
       "sysDescr": sysDescr,
       "sysObjectID": sysObjectID,
       "sysUpTime": sysUpTime,
       "sysContact": sysContact,
       "sysName": sysName,
       "sysLocation": sysLocation,
       "sysServices": sysServices,
       "sysORLastChange": sysORLastChange,
       "sysORTable": sysORTable,
       "sysOREntry": sysOREntry,
       "sysORIndex": sysORIndex,
       "sysORID": sysORID,
       "sysORDescr": sysORDescr,
       "sysORUpTime": sysORUpTime,
       "snmp": snmp,
       "snmpInPkts": snmpInPkts,
       "snmpOutPkts": snmpOutPkts,
       "snmpInBadVersions": snmpInBadVersions,
       "snmpInBadCommunityNames": snmpInBadCommunityNames,
       "snmpInBadCommunityUses": snmpInBadCommunityUses,
       "snmpInASNParseErrs": snmpInASNParseErrs,
       "snmpInTooBigs": snmpInTooBigs,
       "snmpInNoSuchNames": snmpInNoSuchNames,
       "snmpInBadValues": snmpInBadValues,
       "snmpInReadOnlys": snmpInReadOnlys,
       "snmpInGenErrs": snmpInGenErrs,
       "snmpInTotalReqVars": snmpInTotalReqVars,
       "snmpInTotalSetVars": snmpInTotalSetVars,
       "snmpInGetRequests": snmpInGetRequests,
       "snmpInGetNexts": snmpInGetNexts,
       "snmpInSetRequests": snmpInSetRequests,
       "snmpInGetResponses": snmpInGetResponses,
       "snmpInTraps": snmpInTraps,
       "snmpOutTooBigs": snmpOutTooBigs,
       "snmpOutNoSuchNames": snmpOutNoSuchNames,
       "snmpOutBadValues": snmpOutBadValues,
       "snmpOutGenErrs": snmpOutGenErrs,
       "snmpOutGetRequests": snmpOutGetRequests,
       "snmpOutGetNexts": snmpOutGetNexts,
       "snmpOutSetRequests": snmpOutSetRequests,
       "snmpOutGetResponses": snmpOutGetResponses,
       "snmpOutTraps": snmpOutTraps,
       "snmpEnableAuthenTraps": snmpEnableAuthenTraps,
       "snmpSilentDrops": snmpSilentDrops,
       "snmpProxyDrops": snmpProxyDrops,
       "snmpMIB": snmpMIB,
       "snmpMIBObjects": snmpMIBObjects,
       "snmpTrap": snmpTrap,
       "snmpTrapOID": snmpTrapOID,
       "snmpTrapEnterprise": snmpTrapEnterprise,
       "snmpTraps": snmpTraps,
       "coldStart": coldStart,
       "warmStart": warmStart,
       "authenticationFailure": authenticationFailure,
       "snmpSet": snmpSet,
       "snmpSetSerialNo": snmpSetSerialNo,
       "snmpMIBConformance": snmpMIBConformance,
       "snmpMIBCompliances": snmpMIBCompliances,
       "snmpBasicCompliance": snmpBasicCompliance,
       "snmpBasicComplianceRev2": snmpBasicComplianceRev2,
       "snmpMIBGroups": snmpMIBGroups,
       "snmpSetGroup": snmpSetGroup,
       "systemGroup": systemGroup,
       "snmpBasicNotificationsGroup": snmpBasicNotificationsGroup,
       "snmpGroup": snmpGroup,
       "snmpCommunityGroup": snmpCommunityGroup,
       "snmpObsoleteGroup": snmpObsoleteGroup,
       "snmpWarmStartNotificationGroup": snmpWarmStartNotificationGroup,
       "snmpNotificationGroup": snmpNotificationGroup}
)
