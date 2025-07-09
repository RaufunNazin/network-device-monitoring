import asyncio
import json
from fastapi import APIRouter, Query, HTTPException
from ..utils import validate_brand, validate_branch
from typing import Optional
import os # Import the os module

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
    dry_run: bool = Query(False, description="Run the script in dry-run mode (no actual SNMP queries)"),
    onu_index: Optional[str] = Query(None, description="Specific interface index string to query"),
    all_oid: bool = Query(False, description="Retrieve all OIDs for the specified branch"),
):
    """
    Retrieves OLT information by executing an external Python script.
    - **ip**: The target OLT IP address.
    - **brand**: The brand identifier of the OLT.
    - **branch**: The OID branch to query (e.g., MAC, STATUS).
    """
    try:
        # 1. Validate inputs (this part remains the same)
        valid_brand = validate_brand(brand.upper())
        valid_branch = validate_branch(branch.upper())

        # 2. Define the path to your script
        # IMPORTANT: Use an absolute or reliable relative path
        # This assumes your FastAPI app runs from the project root directory
        script_path = os.path.join("NDM-SNMP", "separate_functions.py")
        if not os.path.exists(script_path):
             raise HTTPException(
                status_code=500, detail=f"Script not found at path: {script_path}"
            )


        # 3. Build the command as a list of arguments for security
        command = [
            "python",
            script_path,
            "-i", ip,
            "-c", community,
            "-p", str(port),
            "-bc", valid_branch,
            "-bd", valid_brand,
            "-v", "1",
            "-r", "3",
        ]
        
        # Add optional arguments if they are provided
        if onu_index:
            command.extend(["-idx", onu_index])
        if dry_run:
            command.append("-d")
        if all_oid:
            command.append("-all") # Another flag

        # 4. Execute the command asynchronously
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # 5. Wait for the command to complete and get the output
        stdout, stderr = await process.communicate()

        # 6. Handle errors from the script
        if process.returncode != 0:
            error_message = stderr.decode() if stderr else "Unknown error in script execution."
            raise HTTPException(
                status_code=500,
                detail={"message": "Error executing the SNMP script.", "error": error_message}
            )

        # 7. Process the successful output
        # The script prints JSON to stdout, so we load it
        try:
            # We get the last part of the output, where the JSON is printed
            json_output = stdout.decode().strip().split('--- Parsed ONU Data ---')[-1]
            data = json.loads(json_output)
            return {"value":data, "path": script_path, "command": command}
        except (json.JSONDecodeError, IndexError) as e:
            raise HTTPException(
                status_code=500,
                detail={"message": "Failed to parse JSON output from script.", "raw_output": stdout.decode()}
            )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )