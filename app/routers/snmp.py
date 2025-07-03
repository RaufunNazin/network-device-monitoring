from fastapi import APIRouter

router = APIRouter(
    prefix="/snmp",
    tags=["SNMP"],
)


@router.get("/onu-ports")
async def get_onu_ports():
    """
    Endpoint to retrieve ONU ports information.
    """
    return {"message": "This endpoint will return ONU ports information."}


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
