# Network Device Monitoring Backend

This project is a backend service for monitoring network devices, specifically Optical Network Units (ONUs). It is built with FastAPI and provides endpoints to retrieve and cross-check ONU data.

## Features

- Retrieve ONU information:
  - MAC address
  - Serial number
  - Operational status
  - Administrative status
  - Vendor ID
  - Model ID
  - Power level
  - Distance
  - Uptime

- Obtain user MAC addresses via:
  - Telnet
  - Web scraping

- Cross-check and validate ONU and user data.

## Getting Started

1. Clone the repository.
2. Install dependencies:

   ```bash
   pip install fastapi uvicorn
   ```

3. Run the server:

   ```bash
   uvicorn main:app --reload
   ```

## API Overview

- Will be updated later

## Notes

- Requires network access to ONUs for data collection.
- Telnet and web scraping credentials/configuration may be needed.

## License

MIT
