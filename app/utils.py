from passlib.context import CryptContext
from pysnmp.hlapi.v3arch.asyncio import *
from pysnmp.smi import builder, view
import time
import os
from .enums import COMPILED_MIBS
from constants import mib_map
from snmp_session import get_snmp_session
from dictionaries.oid_dict import oid_dictionary
from parsers.raw_value_parser import format_raw_values
import cx_Oracle
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


_mib_cache = None


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def format_mac(hex_mac):
    clean_mac = hex_mac.replace(" ", "")
    formatted_mac = ":".join(
        [clean_mac[i : i + 2] for i in range(0, len(clean_mac), 2)]
    )
    return formatted_mac


def load_mibs(brand):
    """Load and cache MIBs based on brand; always load DEFAULT MIBs as well."""
    global _mib_cache
    if _mib_cache:
        return _mib_cache

    print("Loading MIBs...")
    start_time = time.time()

    mib_builder = builder.MibBuilder()

    compiled_mib_dir = COMPILED_MIBS
    if os.path.exists(compiled_mib_dir):
        mib_builder.add_mib_sources(builder.DirMibSource(compiled_mib_dir))
    else:
        raise FileNotFoundError(f"Compiled MIB path not found: {compiled_mib_dir}")

    source_mib_dir = "mibs"
    if os.path.exists(source_mib_dir):
        mib_builder.add_mib_sources(builder.DirMibSource(source_mib_dir))

    mibs_to_load = mib_map.get("DEFAULT", [])
    brand_mibs = mib_map.get(brand, [])
    mibs_to_load += brand_mibs

    for mib in mibs_to_load:
        t0 = time.time()
        try:
            mib_builder.load_modules(mib)
            print(f"Loaded {mib} in {time.time() - t0:.2f}s")
        except Exception as e:
            print(f"Warning: Could not load MIB {mib}: {e}")

    _mib_cache = mib_builder

    print(f"MIB Load complete in {time.time() - start_time:.2f} seconds.")
    return mib_builder


def resolve_oid(oid, mib_view):
    try:
        oid_obj = ObjectIdentity(oid)
        oid_obj.resolve_with_mib(mib_view)
        return oid_obj.prettyPrint()
    except Exception:
        try:
            mib_node = mib_view.get_node_name(oid)
            module_name = mib_node[0]
            obj_name = mib_node[1]
            indices = list(oid[len(mib_view.get_node_oid(mib_node)) :])
            index_str = "." + ".".join(map(str, indices)) if indices else ""
            return f"{module_name}::{obj_name}{index_str}"
        except Exception:
            return oid.prettyPrint()


async def get_olt_information(
    target_ip,
    community_string,
    port,
    version,
    retries,
    timeout,
    branch,
    brand,
    onu_index_str,
    all_oid,
):
    """
    Perform an SNMP walk or get operation to retrieve OLT information.
    Returns all resolved OIDs and values as strings.
    """
    result = []
    start_time = time.time()

    mib_builder = load_mibs(brand)
    mib_view = view.MibViewController(mib_builder)

    snmp_engine, community, transport, context = await get_snmp_session(
        target_ip, port, community_string, version, timeout, retries
    )

    action_description = ""

    if onu_index_str:
        if all_oid:
            action_description = (
                f"bulk GET for all branches (index: {onu_index_str}, brand: {brand})"
            )
            print(f"Starting {action_description}")

            object_types_to_fetch = []
            for current_branch_key, brand_map in oid_dictionary.items():
                if brand in brand_map:
                    base_oid_for_branch = brand_map[brand]
                    oid_to_query_for_branch = f"{base_oid_for_branch}.{onu_index_str}"
                    object_types_to_fetch.append(
                        ObjectType(ObjectIdentity(oid_to_query_for_branch))
                    )
                else:
                    msg = f"Info: OID for branch '{current_branch_key}' with brand '{brand}' not found in dictionary. Skipping for index {onu_index_str}."
                    result.append(msg)

            if not object_types_to_fetch:
                if not any(item.startswith("Info:") for item in result):
                    result.append(
                        f"Error: No OIDs found to query for brand '{brand}' and index '{onu_index_str}' with all_oid=True."
                    )
            else:
                errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
                    snmp_engine, community, transport, context, *object_types_to_fetch
                )

                if errorIndication:
                    result.append(f"Error during bulk SNMP GET: {errorIndication}")
                elif errorStatus:
                    failed_oid_str = "?"
                    if errorIndex is not None and 0 < int(errorIndex) <= len(
                        object_types_to_fetch
                    ):
                        failed_oid_object = object_types_to_fetch[int(errorIndex) - 1]
                        failed_oid_str = str(failed_oid_object[0])

                    result.append(
                        f"SNMP Error during bulk GET: {errorStatus.prettyPrint()} (at OID like {failed_oid_str}, errorIndex: {errorIndex})"
                    )
                    for oid_val, value_val in varBinds:
                        symbolic_oid = resolve_oid(oid_val, mib_view)
                        formatted_value = format_raw_values(
                            value_val, type(value_val).__name__.upper()
                        )
                        result.append(f"{symbolic_oid} = {formatted_value}")
                else:
                    for oid_val, value_val in varBinds:
                        symbolic_oid = resolve_oid(oid_val, mib_view)
                        formatted_value = format_raw_values(
                            value_val, type(value_val).__name__.upper()
                        )
                        result.append(f"{symbolic_oid} = {formatted_value}")

        else:
            action_description = (
                f"GET for branch '{branch}' (index: {onu_index_str}, brand: {brand})"
            )
            if branch not in oid_dictionary or brand not in oid_dictionary[branch]:
                error_msg = f"Error: OID for specified branch '{branch}' and brand '{brand}' not found in dictionary."
                print(f"{action_description} - {error_msg}")
                result.append(error_msg)
            else:
                oid_to_query = f"{oid_dictionary[branch][brand]}.{onu_index_str}"
                print(f"Starting {action_description}, OID: {oid_to_query}")

                errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
                    snmp_engine,
                    community,
                    transport,
                    context,
                    ObjectType(ObjectIdentity(oid_to_query)),
                )

                if errorIndication:
                    return [f"Error: {errorIndication}"]
                elif errorStatus:
                    return [
                        f"SNMP Error: {errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or '?'}"
                    ]
                for oid, value in varBinds:
                    symbolic_oid = resolve_oid(oid, mib_view)
                    formatted_value = format_raw_values(
                        value, type(value).__name__.upper()
                    )
                    result.append(f"{symbolic_oid} = {formatted_value}")

    else:
        if all_oid:
            print(
                f"Warning: 'all_oid=True' is currently ignored for SNMP WALK operations (when no ONU index is provided). Performing standard walk for branch '{branch}'."
            )

        action_description = f"WALK for branch '{branch}' (brand: {brand})"
        if branch not in oid_dictionary or brand not in oid_dictionary[branch]:
            error_msg = f"Error: OID for branch '{branch}' and brand '{brand}' not found in dictionary for walk."
            print(f"{action_description} - {error_msg}")
            result.append(error_msg)
        else:
            oid_to_walk = oid_dictionary[branch][brand]
            print(f"Starting {action_description}, Base OID: {oid_to_walk}")

            objects_to_walk = walk_cmd(
                snmp_engine,
                community,
                transport,
                context,
                ObjectType(ObjectIdentity(oid_to_walk)),
                lexicographicMode=False,
            )

            async for (
                errorIndication,
                errorStatus,
                errorIndex,
                varBinds,
            ) in objects_to_walk:
                if errorIndication:
                    return [f"Error: {errorIndication}"]
                elif errorStatus:
                    return [
                        f"SNMP Error: {errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or '?'}"
                    ]
                else:
                    for oid, value in varBinds:
                        symbolic_oid = resolve_oid(oid, mib_view)
                        formatted_value = format_raw_values(
                            value, type(value).__name__.upper()
                        )
                        result.append(f"{symbolic_oid} = {formatted_value}")

    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time:.2f} seconds")
    print(f"SNMP {action_description} completed. Processed {len(result)} entries.")
    return result


def insert_into_db(onu_data, ip, db_host, db_port, db_user, db_pass, db_sid):
    """
    Insert ONU data into the Oracle database.

    Args:
        onu_data (dict): Dictionary containing ONU data with keys like 'MAC', 'SLNO', 'STATUS', etc.
        ip (str): IP address of the switch to retrieve the switch ID.
        db_host (str): Database host.
        db_port (int): Database port.
        db_user (str): Database username.
        db_pass (str): Database password.
        db_sid (str): Database SID.

    Returns:
        bool: True if insertion was successful, False otherwise.
    """
    dsn_tns = cx_Oracle.makedsn(db_host, db_port, sid=db_sid)

    try:
        connection = cx_Oracle.connect(db_user, db_pass, dsn_tns)
        cursor = connection.cursor()

        print(f"Connected to Oracle Database.")

        try:
            cursor.execute("SELECT ID FROM SWITCHES WHERE IP = :ip", {"ip": ip})
            result = cursor.fetchone()
            sw_id = result[0] if result else None
            if sw_id:
                print(f"Retrieved switch ID {sw_id} from SWITCHES table for IP {ip}")
            else:
                print(
                    f"Warning: No switch found with IP {ip} in SWITCHES table. SW_ID will be set to NULL."
                )
        except cx_Oracle.DatabaseError as e:
            (error,) = e.args
            print(f"Error retrieving switch ID from SWITCHES table: {error.message}")
            sw_id = None

        for index, data in onu_data.items():
            data["SW_ID"] = sw_id

        current_time = datetime.now()

        for index, data in onu_data.items():
            cursor.execute("SELECT SWITCH_SNMP_ONU_PORTS_sq.nextval FROM DUAL")
            _id = cursor.fetchone()[0]
            data.setdefault("MAC", None)
            data.setdefault("POWER", None)
            data.setdefault("STATUS", None)
            data.setdefault("IFDESCR", None)
            data.setdefault("PORTNO", None)
            data.setdefault("IFINDEX", None)
            data.setdefault("PARENT_ID", None)
            data.setdefault("SLNO", None)
            data.setdefault("DISTANCE", None)
            data.setdefault("UP_SINCE", None)
            data.setdefault("ONU_MODEL", None)
            data.setdefault("ONU_VENDOR", None)
            data.setdefault("IFINDEX2", None)

            cursor.execute(
                """
            INSERT INTO SWITCH_SNMP_ONU_PORTS 
            (ID, PORT_ID, MAC, POWER, STATUS, IFDESCR, PORTNO, SW_ID, IFINDEX, 
            UDATE, PARENT_ID, SLNO, DISTANCE, UP_SINCE, ONU_MODEL, ONU_VENDOR, IFINDEX2)
            VALUES 
            (:id, :port_id, :mac, :power, :status, :ifdescr, :portno, :sw_id, :ifindex,
            :udate, :parent_id, :slno, :distance, :up_since, :onu_model, :onu_vendor, :ifindex2)
            """,
                {
                    "id": _id,
                    "port_id": None,
                    "mac": data["MAC"],
                    "power": data["POWER"],
                    "status": data["STATUS"],
                    "ifdescr": data["IFDESCR"],
                    "portno": data["PORTNO"],
                    "sw_id": sw_id,
                    "ifindex": data["IFINDEX"],
                    "udate": current_time,
                    "parent_id": data["PARENT_ID"],
                    "slno": data["SLNO"],
                    "distance": data["DISTANCE"],
                    "up_since": data["UP_SINCE"],
                    "onu_model": data["ONU_MODEL"],
                    "onu_vendor": data["ONU_VENDOR"],
                    "ifindex2": data["IFINDEX2"],
                },
            )

            connection.commit()
            print(f"Inserted record for ONU {index} with ID {_id} with {sw_id}")

        print(f"Successfully inserted {len(onu_data)} ONU records into the database.")

    except cx_Oracle.DatabaseError as e:
        (error,) = e.args
        print(f"Database error: {error.message}")
        return False
    finally:
        if "connection" in locals():
            connection.close()

    return True


def insert_into_db_olt_customer_mac(
    onu_data, ip, db_host, db_port, db_user, db_pass, db_sid
):
    dsn_tns = cx_Oracle.makedsn(db_host, db_port, sid=db_sid)

    try:
        connection = cx_Oracle.connect(db_user, db_pass, dsn_tns)
        cursor = connection.cursor()

        print(f"Connected to Oracle Database.")

        try:
            cursor.execute("SELECT ID FROM SWITCHES WHERE IP = :ip", {"ip": ip})
            result = cursor.fetchone()
            olt_id = result[0] if result else None
            if olt_id:
                print(f"Retrieved OLT ID {olt_id} from SWITCHES table for IP {ip}")
            else:
                print(
                    f"Warning: No OLT found with IP {ip} in SWITCHES table. SW_ID will be set to NULL."
                )
        except cx_Oracle.DatabaseError as e:
            (error,) = e.args
            print(f"Error retrieving OLT ID from SWITCHES table: {error.message}")
            olt_id = None

        for index, data in enumerate(onu_data):
            data["OLT_ID"] = olt_id

        current_time = datetime.now()

        for index, data in enumerate(onu_data):
            cursor.execute("SELECT OLT_CUSTOMER_MAC_sq.nextval FROM DUAL")
            _id = cursor.fetchone()[0]
            data.setdefault("OLT_ID", None)
            data.setdefault("VLAN", None)
            data.setdefault("Port", None)
            data.setdefault("MAC", None)
            data.setdefault("udate", None)

            cursor.execute(
                """
            INSERT INTO OLT_CUSTOMER_MAC 
            (ID, OLT_ID, VLAN, PORT, MAC, UDATE)
            VALUES 
            (:id, :olt_id, :vlan, :port, :mac, :udate)
            """,
                {
                    "id": _id,
                    "olt_id": data["OLT_ID"],
                    "vlan": data["VLAN"],
                    "port": data["Port"],
                    "mac": data["MAC"],
                    "udate": current_time,
                },
            )

            connection.commit()
            print(f"Inserted record for ONU {index} with ID {_id} with {olt_id}")

        print(f"Successfully inserted {len(onu_data)} ONU records into the database.")

    except cx_Oracle.DatabaseError as e:
        (error,) = e.args
        print(f"Database error: {error.message}")
        return False
    finally:
        if "connection" in locals():
            connection.close()
    return True
