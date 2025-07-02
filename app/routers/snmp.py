import asyncio
from ..enums import MAC, OPERATION_STATUS, ADMIN_STATUS, DISTANCE, UP_SINCE, VENDOR, MODEL, SERIAL_NO, POWER, DESC, CDATA_EPON, CDATA_GPON, VSOL_EPON, VSOL_GPON
import argparse
from ..utils import get_olt_information
from app.parsers.default_parser import process_snmp_data