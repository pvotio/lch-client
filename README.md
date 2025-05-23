# LCH Scraper and Ingestion Pipeline

This project implements a structured ETL pipeline that scrapes data from the **LCH Group** (London Clearing House) website, transforms it into a standardized format, and loads it into a Microsoft SQL Server database. It is ideal for ingesting daily margin or collateral-related data used in risk and treasury analytics.

## Overview

### Purpose

This pipeline automates:
- Web scraping of structured tabular data from LCH portals.
- Parsing and cleansing scraped data using Pandas.
- Inserting the transformed dataset into a specified SQL Server table.

The scraper ensures data availability for downstream reporting, margin analysis, and regulatory workflows.

## Application Flow

Execution is orchestrated by `main.py` and follows this sequence:

1. **Initialize Scraper Engine**:
   - Instantiates a retry-aware scraper via the `Engine` class (from `scraper` module).

2. **Fetch Data**:
   - Makes HTTP requests to LCH pages, extracts HTML tables using `lxml`/`pandas`.

3. **Transform**:
   - The `Agent` class from `transformer` handles data normalization and formatting.

4. **Database Insert**:
   - Uses `create_inserter_objects()` to prepare a database interface.
   - Data is inserted into the table specified by the `OUTPUT_TABLE` variable.

## Project Structure

```
lch-client-main/
├── main.py                     # Pipeline entrypoint
├── config/                     # Logger and settings
│   ├── settings.py             # Loads .env variables
├── database/                   # SQL Server connectivity and inserters
├── scraper/                    # Custom HTML parsing logic
├── transformer/                # Transformation layer
├── utils/                      # Inserter factory and helpers
├── .env.sample                 # Environment variable config template
├── Dockerfile                  # Containerization support
├── requirements.txt            # Python dependencies
```

## Environment Variables

Use the `.env.sample` file to create a `.env`. Required settings include:

| Variable | Description |
|----------|-------------|
| `LOG_LEVEL` | Logging level (`INFO`, `DEBUG`) |
| `OUTPUT_TABLE` | Destination table in SQL Server |
| `INSERTER_MAX_RETRIES` | Number of retries for failed DB inserts |
| `REQUEST_MAX_RETRIES` | Retry count for web scraping requests |
| `REQUEST_BACKOFF_FACTOR` | Exponential backoff factor between retries |
| `MSSQL_SERVER` | SQL Server hostname or IP |
| `MSSQL_DATABASE` | Target database name |
| `MSSQL_USERNAME` / `MSSQL_PASSWORD` | Authentication credentials |

## Docker Support

You can run this application as a container for consistent environments.

### Build
```bash
docker build -t lch-client .
```

### Run
```bash
docker run --env-file .env lch-client
```

## Requirements

Install dependencies with pip:

```bash
pip install -r requirements.txt
```

Notable packages used:
- `requests`: HTTP client for scraping
- `pandas`: Table parsing and data transformation
- `lxml`: HTML parsing
- `SQLAlchemy`, `pyodbc`: SQL Server access
- `python-decouple`: Secure environment variable loading

## Running the App

Once `.env` is configured, launch the application using:

```bash
python main.py
```

You’ll see logs indicating:
- Fetch progress
- Data transformation results
- Insert status

## License

This project is provided under the MIT License. Always verify usage rights when scraping external sources.
