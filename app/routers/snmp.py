from fastapi import APIRouter
from ..get_snmp import retrieve_olt_data

router = APIRouter(
    prefix="/snmp",
    tags=["SNMP"],
)


@router.get("/onu-ports")
async def get_onu_ports(
    ip: str,
    community: str,
    brand: str,
    branch: str,
    port: int = 161,
    version: int = 0,
    retries: int = 3,
    timeout: int = 3,
    onu_index_str: Optional[str] = None,
    all_oid: bool = False,
    dry_run: bool = False,
):
    """
    Endpoint to retrieve customer MAC addresses.
    """
    data = await retrieve_olt_data()
    


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
