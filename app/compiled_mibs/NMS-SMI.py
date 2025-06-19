# SNMP MIB module (NMS-SMI) expressed in pysnmp data model.
#
# This Python module is designed to be imported and executed by the
# pysnmp library.
#
# See https://www.pysnmp.com/pysnmp for further information.
#
# Notes
# -----
# ASN.1 source file://app/mibs/NMS-SMI
# Produced by pysmi-1.6.1 at Thu Jun 19 14:04:18 2025
# On host user-HP platform Linux version 6.11.0-26-generic by user user
# Using Python version 3.12.3 (main, May 26 2025, 18:50:19) [GCC 13.3.0]

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
 NotificationGroup) = mibBuilder.importSymbols(
    "SNMPv2-CONF",
    "ModuleCompliance",
    "NotificationGroup")

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
 enterprises,
 iso) = mibBuilder.importSymbols(
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
    "enterprises",
    "iso")

(DisplayString,
 PhysAddress,
 TextualConvention) = mibBuilder.importSymbols(
    "SNMPv2-TC",
    "DisplayString",
    "PhysAddress",
    "TextualConvention")


# MODULE-IDENTITY

nms = ModuleIdentity(
    (1, 3, 6, 1, 4, 1, 3320)
)


# Types definitions


# TEXTUAL-CONVENTIONS



# MIB Managed Objects in the order of their OIDs

_NmsProducts_ObjectIdentity = ObjectIdentity
nmsProducts = _NmsProducts_ObjectIdentity(
    (1, 3, 6, 1, 4, 1, 3320, 1)
)
if mibBuilder.loadTexts:
    nmsProducts.setStatus("current")
_Nmslocal_ObjectIdentity = ObjectIdentity
nmslocal = _Nmslocal_ObjectIdentity(
    (1, 3, 6, 1, 4, 1, 3320, 2)
)
if mibBuilder.loadTexts:
    nmslocal.setStatus("current")
_Nmstemporary_ObjectIdentity = ObjectIdentity
nmstemporary = _Nmstemporary_ObjectIdentity(
    (1, 3, 6, 1, 4, 1, 3320, 3)
)
if mibBuilder.loadTexts:
    nmstemporary.setStatus("current")
_NmsMgmt_ObjectIdentity = ObjectIdentity
nmsMgmt = _NmsMgmt_ObjectIdentity(
    (1, 3, 6, 1, 4, 1, 3320, 9)
)
if mibBuilder.loadTexts:
    nmsMgmt.setStatus("current")
_NmsModules_ObjectIdentity = ObjectIdentity
nmsModules = _NmsModules_ObjectIdentity(
    (1, 3, 6, 1, 4, 1, 3320, 12)
)
if mibBuilder.loadTexts:
    nmsModules.setStatus("current")
_NmsPolicyAuto_ObjectIdentity = ObjectIdentity
nmsPolicyAuto = _NmsPolicyAuto_ObjectIdentity(
    (1, 3, 6, 1, 4, 1, 3320, 18)
)
if mibBuilder.loadTexts:
    nmsPolicyAuto.setStatus("current")
_NmsPibToMib_ObjectIdentity = ObjectIdentity
nmsPibToMib = _NmsPibToMib_ObjectIdentity(
    (1, 3, 6, 1, 4, 1, 3320, 18, 2)
)
if mibBuilder.loadTexts:
    nmsPibToMib.setStatus("current")
_NmsWorkGroup_ObjectIdentity = ObjectIdentity
nmsWorkGroup = _NmsWorkGroup_ObjectIdentity(
    (1, 3, 6, 1, 4, 1, 3320, 20)
)
if mibBuilder.loadTexts:
    nmsWorkGroup.setStatus("current")
_NmsEPONGroup_ObjectIdentity = ObjectIdentity
nmsEPONGroup = _NmsEPONGroup_ObjectIdentity(
    (1, 3, 6, 1, 4, 1, 3320, 101)
)
if mibBuilder.loadTexts:
    nmsEPONGroup.setStatus("current")
_NmsPTNGroup_ObjectIdentity = ObjectIdentity
nmsPTNGroup = _NmsPTNGroup_ObjectIdentity(
    (1, 3, 6, 1, 4, 1, 3320, 102)
)
if mibBuilder.loadTexts:
    nmsPTNGroup.setStatus("current")

# Managed Objects groups


# Notification objects


# Notifications groups


# Agent capabilities


# Module compliance


# Export all MIB objects to the MIB builder

mibBuilder.exportSymbols(
    "NMS-SMI",
    **{"nms": nms,
       "nmsProducts": nmsProducts,
       "nmslocal": nmslocal,
       "nmstemporary": nmstemporary,
       "nmsMgmt": nmsMgmt,
       "nmsModules": nmsModules,
       "nmsPolicyAuto": nmsPolicyAuto,
       "nmsPibToMib": nmsPibToMib,
       "nmsWorkGroup": nmsWorkGroup,
       "nmsEPONGroup": nmsEPONGroup,
       "nmsPTNGroup": nmsPTNGroup}
)
