import asyncio
import json
from fastapi import APIRouter, Query, HTTPException
from ..utils import validate_brand, validate_branch, get_switch_info
from typing import Optional
import sys
import os  # Import the os module

router = APIRouter(
    prefix="/snmp",
    tags=["SNMP"],
)


@router.get("/onu-ports/{switch_id}/{branch}")
async def get_onu_ports(
    # --- Path Parameters ---
    switch_id: int = Path(
        ..., description="The ID of the switch from the SWITCHES table"
    ),
    branch: str = Path(..., description="The OID branch to query (e.g., MAC, STATUS)"),
    # --- Query Parameters ---
    dry_run: bool = Query(
        False, description="Run in dry-run mode without actual SNMP queries"
    ),
    onu_index: Optional[str] = Query(
        None, description="Specific interface index to query"
    ),
    all_oid: bool = Query(
        False, description="Retrieve all OIDs for the specified branch"
    ),
):
    """
    Retrieves OLT information by looking up switch details using its ID
    and then executing an external Python script.
    - **switch_id**: The unique identifier for the switch in the database.
    - **branch**: The OID branch to query (e.g., MAC, STATUS).
    """
    try:
        # 1. Fetch switch connection details from the database using the ID
        switch_details = await get_switch_info(switch_id)
        if not switch_details:
            raise HTTPException(
                status_code=404, detail=f"Switch with ID {switch_id} not found."
            )

        ip = switch_details["ip"]
        brand = switch_details["brand"]
        community = switch_details["community"]
        port = switch_details["port"]

        if not all([ip, brand, community, port]):
            raise HTTPException(
                status_code=400,
                detail=f"Incomplete SNMP configuration for Switch ID {switch_id} in the database.",
            )

        # 2. Validate inputs from the database
        valid_brand = validate_brand(brand.upper())
        valid_branch = validate_branch(branch.upper())

        # 3. Define the path to your script (this part remains the same)
        current_api_dir = os.path.dirname(os.path.abspath(__file__))
        project_base = os.path.dirname(
            os.path.dirname(os.path.dirname(current_api_dir))
        )
        script_path = os.path.join(project_base, "NDM-SNMP", "separate_functions.py")

        if not os.path.exists(script_path):
            raise HTTPException(
                status_code=500, detail=f"Script not found at path: {script_path}"
            )

        # 4. Build the command using details from the database
        command = [
            sys.executable,
            script_path,
            "-i",
            ip,
            "-c",
            community,
            "-p",
            str(port),
            "-bc",
            valid_branch,
            "-bd",
            valid_brand,
            "-v",
            "1",
            "-r",
            "3",
        ]

        # Add optional arguments
        if onu_index:
            command.extend(["-idx", onu_index])
        if dry_run:
            command.append("-d")
        if all_oid:
            command.append("-all")

        # 5. Execute the command asynchronously
        process = await asyncio.create_subprocess_exec(
            *command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        # 6. Handle script errors
        if process.returncode != 0:
            error_message = (
                stderr.decode() if stderr else "Unknown script execution error."
            )
            raise HTTPException(
                status_code=500,
                detail={
                    "message": "Error executing the SNMP script.",
                    "error": error_message,
                },
            )

        # 7. Process successful output
        try:
            json_output = stdout.decode().strip().split("--- Parsed ONU Data ---")[-1]
            data = json.loads(json_output)

            response_message = (
                "Dry run completed successfully. Data not inserted."
                if dry_run
                else "ONU ports retrieved successfully. Data inserted into the database."
            )
            response_status = "dry run" if dry_run else "success"

            return {
                "status": response_status,
                "message": response_message,
                "data": data,
            }

        except (json.JSONDecodeError, IndexError):
            raise HTTPException(
                status_code=500,
                detail={
                    "message": "Failed to parse JSON from script.",
                    "raw_output": stdout.decode(),
                },
            )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Catch exceptions from get_switch_info or other unexpected errors
        if isinstance(e, HTTPException):
            raise e  # Re-raise HTTPException to preserve status code and detail
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )
