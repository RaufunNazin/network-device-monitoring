from fastapi import APIRouter, Query, HTTPException
from ..get_snmp import retrieve_olt_data
from ..utils import validate_brand, validate_branch
from typing import Optional

router = APIRouter(
    prefix="/snmp",
    tags=["SNMP"],
)


@router.get("/onu-ports/{ip}/{brand}/{branch}")
async def get_onu_ports(
    # --- Path Parameters ---
    ip: str,
    brand: str,
    branch: str,
    # --- Query Parameters ---
    community: str = Query(..., description="SNMP community string for read access"),
    port: int = Query(161, description="SNMP port"),
    version: int = Query(0, ge=0, le=1, description="SNMP version (0 for v1, 1 for v2c)"),
    retries: int = Query(3, description="Number of SNMP retries"),
    timeout: int = Query(3, description="SNMP timeout in seconds"),
    onu_index: Optional[str] = Query(None, description="Specific interface index string to query"),
    all_oid: bool = Query(False, description="Retrieve all OIDs for the specified branch"),
    dry_run: bool = Query(False, description="Parse data but do not insert into the database"),
):
    """
    Retrieves OLT information for a given brand and branch via SNMP.
    - **ip**: The target OLT IP address.
    - **brand**: The brand identifier of the OLT.
    - **branch**: The OID branch to query (e.g., MAC, STATUS).
    """
    try:
        # Validate the inputs first
        valid_brand = validate_brand(brand.upper())
        valid_branch = validate_branch(branch.upper())

        # Call the core logic with all parameters from the API
        processed_data, db_success = await retrieve_olt_data(
            target_ip=ip,
            community_string=community,
            brand=valid_brand,
            port=port,
            version=version,
            retries=retries,
            timeout=timeout,
            branch=valid_branch,
            onu_index_str=onu_index,
            all_oid=all_oid,  
            dry_run=dry_run,
        )

        if dry_run:
            return {
                "status": "dry_run",
                "message": "Data retrieved successfully. Database insertion was skipped.",
                "data": processed_data,
            }

        if db_success:
            return {
                "status": "success",
                "message": "Data retrieved and stored successfully.",
                "data": processed_data,
            }
        else:
            # If insertion fails, it's a server-side issue.
            raise HTTPException(
                status_code=500,
                detail={
                    "status": "error",
                    "message": "Data was retrieved, but failed to store in the database.",
                    "data": processed_data,
                },
            )

    except ValueError as e:
        # Catches validation errors for brand/branch
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Catches other potential errors (e.g., SNMP timeout, connection error)
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )
    


@router.get("/customer-mac")
async def get_customer_mac():
    """
    Endpoint to retrieve customer MAC addresses.
    """
    return {"message": "This endpoint will return customer MAC addresses."}


@router.get("/web-scraping")
async def web_scraping():
    """
    Endpoint to perform web scraping.
    """
    return {"message": "This endpoint will perform web scraping."}
