from ..enums import (
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
    CDATA_EPON,
    CDATA_GPON,
    VSOL_EPON,
    VSOL_GPON,
)
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
