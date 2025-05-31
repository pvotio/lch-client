# LCH CDS Pricing Data Ingestion Pipeline

This project implements a structured and automated pipeline for retrieving, transforming, and storing Credit Default Swap (CDS) pricing data published by the LCH Group. It scrapes pricing content from the LCH post-trade website, processes the data into a normalized format, and loads it into a Microsoft SQL Server database for downstream use in risk analysis, reconciliation, and compliance reporting.

## Overview

### Purpose

This pipeline serves the following objectives:
- Retrieve daily CDS pricing data, including fixed rate curves, tiers, maturities, and contract identifiers.
- Transform the raw JSON into a clean, structured tabular format.
- Persist the resulting dataset into a SQL Server environment for enterprise-scale consumption.

The processed data supports functions across finance, operations, and regulatory reporting teams.

## Source of Data

Pricing data is publicly provided by LCH via its CDSClear post-trade portal:

- Source: https://www.lseg.com/en/post-trade/clearing/lch-services/cdsclear/essentials/pricing-data
- Data Format: JSON via discovered hyperlinks embedded in the pricing portal
- Coverage: Credit Index and Single Name CDS curves, series-based valuation

Fields included in the transformed dataset:
- `valuation_date`
- `instrument`
- `instrument_name`
- `series`
- `version`
- `contractual_definitions`
- `fixed_rate`
- `maturity`
- `index_factor`
- `price`
- `ticker`
- `tier`
- `doc_clause`

## Pipeline Flow

The ingestion process is organized into the following stages:

1. **Discovery**:
   - Web scraping logic extracts URLs pointing to relevant JSON pricing files.

2. **Data Retrieval**:
   - The scraper downloads each JSON file and converts it to a DataFrame.

3. **Data Transformation**:
   - Field normalization, date parsing, and column mapping are handled by the transformation layer.

4. **Database Insertion**:
   - The transformed dataset is inserted into SQL Server using batch insertion with retry support.

## Project Structure

```
lch-client-main/
├── main.py                   # Entry point
├── config/                   # Environment and logger setup
│   ├── settings.py
│   └── logger.py
├── scraper/                  # LCH pricing discovery and JSON loader
│   └── engine.py
├── transformer/              # Pricing transformation routines
│   └── agent.py
├── database/                 # MSSQL helper functions
├── utils/                    # Retry logic and inserter abstraction
├── .env.sample               # Example environment variables
├── Dockerfile                # Container setup
├── requirements.txt          # Python dependencies
```

## Environment Variables

The application is configured via a `.env` file modeled after `.env.sample`. The following variables are required:

| Variable | Description |
|----------|-------------|
| `LOG_LEVEL` | Logging level (`INFO`, `DEBUG`, etc.) |
| `OUTPUT_TABLE` | SQL Server table for data storage |
| `MSSQL_SERVER`, `MSSQL_DATABASE`, `MSSQL_USERNAME`, `MSSQL_PASSWORD` | Database connection configuration |
| `INSERTER_MAX_RETRIES` | Maximum retry attempts for failed inserts |
| `REQUEST_MAX_RETRIES`, `REQUEST_BACKOFF_FACTOR` | Control exponential backoff behavior during data fetch |

## Docker Deployment

To run the pipeline in a containerized environment:

### Build
```bash
docker build -t lch-client .
```

### Execute
```bash
docker run --env-file .env lch-client
```

## Local Installation

Install dependencies via:

```bash
pip install -r requirements.txt
```

Key libraries used:
- `requests`, `beautifulsoup4`, `lxml` for scraping and parsing
- `pandas` for data manipulation
- `SQLAlchemy`, `pyodbc` for SQL Server integration
- `python-decouple` for configuration management

## Execution

Once the environment is set:

```bash
python main.py
```

This will:
- Discover CDS JSON files
- Extract, clean, and transform pricing data
- Insert the result into the specified database table

## License

This project is distributed under the MIT License. Users are responsible for ensuring compliance with LCH Group’s published data usage terms.
