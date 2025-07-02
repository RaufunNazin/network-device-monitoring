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
    Upsert ONU data into the Oracle database using the MERGE statement.
    If a record with the same SW_ID and IFDESCR exists, it's updated.
    Otherwise, a new record is inserted.

    Args:
        onu_data (dict): Dictionary containing ONU data with keys like 'MAC', 'SLNO', 'STATUS', etc.
        ip (str): IP address of the switch to retrieve the switch ID.
        db_host (str): Database host.
        db_port (int): Database port.
        db_user (str): Database username.
        db_pass (str): Database password.
        db_sid (str): Database SID.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    dsn_tns = cx_Oracle.makedsn(db_host, db_port, sid=db_sid)
    connection = None  # Initialize connection to None for robust error handling

    try:
        connection = cx_Oracle.connect(db_user, db_pass, dsn_tns)
        cursor = connection.cursor()

        print("Connected to Oracle Database.")

        sw_id = None
        try:
            cursor.execute("SELECT ID FROM SWITCHES WHERE IP = :ip", {"ip": ip})
            result = cursor.fetchone()
            if result:
                sw_id = result[0]
                print(f"Retrieved switch ID {sw_id} from SWITCHES table for IP {ip}")
            else:
                print(
                    f"Warning: No switch found with IP {ip} in SWITCHES table. SW_ID will be set to NULL."
                )
        except cx_Oracle.DatabaseError as e:
            (error,) = e.args
            print(f"Error retrieving switch ID from SWITCHES table: {error.message}")

        # --- The MERGE statement is the key to the new logic ---
        merge_sql = """
        MERGE INTO SWITCH_SNMP_ONU_PORTS T
        USING (
            SELECT :sw_id AS SW_ID, :ifdescr AS IFDESCR FROM DUAL
        ) S
        ON (T.SW_ID = S.SW_ID AND T.IFDESCR = S.IFDESCR)
        WHEN MATCHED THEN
            UPDATE SET
                T.MAC = :mac,
                T.POWER = :power,
                T.STATUS = :status,
                T.PORTNO = :portno,
                T.IFINDEX = :ifindex,
                T.UDATE = :udate,
                T.SLNO = :slno,
                T.DISTANCE = :distance,
                T.UP_SINCE = :up_since,
                T.ONU_MODEL = :onu_model,
                T.ONU_VENDOR = :onu_vendor,
                T.IFINDEX2 = :ifindex2
        WHEN NOT MATCHED THEN
            INSERT (
                ID, PORT_ID, MAC, POWER, STATUS, IFDESCR, PORTNO, SW_ID, IFINDEX,
                UDATE, PARENT_ID, SLNO, DISTANCE, UP_SINCE, ONU_MODEL, ONU_VENDOR, IFINDEX2
            )
            VALUES (
                SWITCH_SNMP_ONU_PORTS_sq.nextval, :port_id, :mac, :power, :status,
                :ifdescr, :portno, :sw_id, :ifindex, :udate, :parent_id, :slno,
                :distance, :up_since, :onu_model, :onu_vendor, :ifindex2
            )
        """

        # --- A single, consolidated loop for processing ---
        for index, data in onu_data.items():
            try:
                # Prepare the dictionary of parameters for the MERGE statement.
                # .get() is safer than [], as it returns None if a key is missing.
                params = {
                    "port_id": None,  # As per your original code
                    "mac": data.get("MAC"),
                    "power": data.get("POWER"),
                    "status": data.get("STATUS"),
                    "ifdescr": data.get("IFDESCR"),
                    "portno": (
                        data.get("ONU_PORT")
                        if data.get("ONU_PORT") is not None
                        else (
                            data.get("IFDESCR").split(":")[1]
                            if ":" in data.get("IFDESCR", "")
                            else None
                        )
                    ),
                    "sw_id": sw_id,
                    "ifindex": data.get("IFINDEX"),
                    "udate": datetime.now(),
                    "parent_id": data.get("PARENT_ID"),
                    "slno": data.get("SLNO"),
                    "distance": data.get("DISTANCE"),
                    "up_since": (
                        datetime.strptime(data["UP_SINCE"], "%Y-%m-%d %H:%M:%S")
                        if data.get("UP_SINCE")
                        else None
                    ),
                    "onu_model": data.get("ONU_MODEL"),
                    "onu_vendor": data.get("ONU_VENDOR"),
                    "ifindex2": data.get("IFINDEX2"),
                }

                cursor.execute(merge_sql, params)
                print(f"Upserted record for ONU {index} on switch {sw_id}")

            except cx_Oracle.DatabaseError as e:
                (error,) = e.args
                print(f"Error processing record for ONU {index}: {error.message}")
                # Decide if you want to stop or continue. Continuing here.
                continue

        connection.commit()
        print(f"Successfully processed {len(onu_data)} ONU records.")

    except cx_Oracle.DatabaseError as e:
        (error,) = e.args
        print(f"Database error: {error.message}")
        if connection:
            connection.rollback()
        return False
    finally:
        if connection:
            connection.close()
            print("Database connection closed.")

    return True


def insert_into_db_olt_customer_mac(
    onu_data, ip, db_host, db_port, db_user, db_pass, db_sid
):
    """
    Inserts or updates ONU data into the OLT_CUSTOMER_MAC table.

    For each record, it checks if a record with the same MAC, PORT, and OLT_ID
    already exists. If it does, only the VLAN and UDATE are updated.
    If not, a new record is inserted.

    Args:
        onu_data (list): A list of dictionaries, each representing an ONU.
        ip (str): The IP address of the OLT to find its ID in the SWITCHES table.
        db_host, db_port, db_user, db_pass, db_sid: Oracle DB connection details.

    Returns:
        bool: True if the operation completed, False if a connection error occurred.
    """
    cleaned_onu_data = [
        item for item in onu_data if item and item.get("MAC") and item.get("PORT")
    ]
    if not cleaned_onu_data:
        print("No valid ONU data with both MAC and PORT to process.")
        return True

    dsn_tns = cx_Oracle.makedsn(db_host, db_port, sid=db_sid)
    connection = None

    try:
        connection = cx_Oracle.connect(db_user, db_pass, dsn_tns)
        cursor = connection.cursor()
        print("Connected to Oracle Database.")

        # --- STEP 1: Retrieve the OLT ID once at the beginning ---
        olt_id = None
        try:
            cursor.execute("SELECT ID FROM SWITCHES WHERE IP = :ip", {"ip": ip})
            result = cursor.fetchone()
            if result:
                olt_id = result[0]
                print(f"Retrieved OLT ID: {olt_id} for IP: {ip}")
            else:
                print(
                    f"Warning: No OLT found with IP {ip}. Records cannot be processed without an OLT_ID."
                )
                # If olt_id is essential, we should stop here.
                return True
        except cx_Oracle.DatabaseError as e:
            print(f"Error retrieving OLT ID from SWITCHES table: {e}")
            return False  # Cannot proceed without OLT ID

        current_time = datetime.now()
        inserted_count = 0
        updated_count = 0

        # --- STEP 2: Loop through data and perform the new UPSERT logic ---
        for data in cleaned_onu_data:
            try:
                mac_address = data["MAC"]
                port = data["PORT"]
                vlan = data.get("VLAN")

                # --- MODIFIED CHECK ---
                # Check if a record with the same MAC, PORT, AND olt_id already exists.
                cursor.execute(
                    """
                    SELECT ID FROM OLT_CUSTOMER_MAC
                    WHERE MAC = :mac AND PORT = :port AND OLT_ID = :olt_id
                    """,
                    {"mac": mac_address, "port": port, "olt_id": olt_id},
                )
                result = cursor.fetchone()

                if result:
                    # --- UPDATE PATH ---
                    # The record exists, so ONLY update VLAN and UDATE.
                    existing_id = result[0]
                    update_data = {
                        "id": existing_id,
                        "vlan": vlan,
                        "udate": current_time,
                    }
                    cursor.execute(
                        """
                        UPDATE OLT_CUSTOMER_MAC
                        SET VLAN = :vlan, UDATE = :udate
                        WHERE ID = :id
                        """,
                        update_data,
                    )
                    updated_count += 1
                    print(
                        f"Updated VLAN for existing record with MAC {mac_address} and PORT {port}"
                    )
                else:
                    # --- INSERT PATH ---
                    # No such record found, so insert a new one.
                    cursor.execute("SELECT OLT_CUSTOMER_MAC_sq.nextval FROM DUAL")
                    new_id = cursor.fetchone()[0]
                    insert_data = {
                        "id": new_id,
                        "olt_id": olt_id,
                        "vlan": vlan,
                        "port": port,
                        "mac": mac_address,
                        "udate": current_time,
                    }
                    cursor.execute(
                        """
                        INSERT INTO OLT_CUSTOMER_MAC (ID, OLT_ID, VLAN, PORT, MAC, UDATE)
                        VALUES (:id, :olt_id, :vlan, :port, :mac, :udate)
                        """,
                        insert_data,
                    )
                    inserted_count += 1
                    print(f"Inserted new record for MAC {mac_address} and PORT {port}")

                connection.commit()

            except cx_Oracle.DatabaseError as e:
                print(f"Database error processing MAC {data.get('MAC')}: {e}")
                connection.rollback()
                continue

        print(
            f"\nProcessing complete. Inserted: {inserted_count}, Updated: {updated_count}."
        )

    except cx_Oracle.DatabaseError as e:
        print(f"A database connection or setup error occurred: {e}")
        return False
    finally:
        if connection:
            connection.close()
            print("Database connection closed.")

    return True
