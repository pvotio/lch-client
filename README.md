# LCH Data CDS Settlement Prices

Extract, transform, and load (ETL) LCH (London Clearing House) CDS clearing essentials pricing data into an MSSQL database, leveraging Docker for seamless deployment and scalability. CDS settlement prices are converted to spreads using the ISDA model.


## 📌 Features:

- **Efficient Scraping:** Designed to scrape CDS clearing essentials pricing data directly from the LCH's official website.
- **Data Transformation:** Tailored data transformation for easy database insertion.
- **MSSQL Support:** Built-in support to insert data into a Microsoft SQL Server database.
- **Dockerized:** Simplified deployment and setup using Docker.
- **Robust Error Handling:** Multi-retry mechanisms and comprehensive logging.


## Getting Started:  

### Environment Setup

1. Clone the repository:
   ``` bash 
    git clone git@github.com:alimghmi/lch-client.git
    cd lch-client
   ```
2. Create an `.env` file in the project root and configure the following:
   ```
    URL="https://www.lch.com/services/cdsclear/essentials/pricing-data"
    LOG_LEVEL="INFO"
    OUTPUT_TABLE=<name_of_the_output_table>
    INSERTER_MAX_RETRIES=2
    REQUEST_MAX_RETRIES=3
    REQUEST_BACKOFF_FACTOR=2
    MSSQL_SERVER=<mssql_server>
    MSSQL_DATABASE=<mssql_database>
    MSSQL_USERNAME=<mssql_username>
    MSSQL_PASSWORD=<mssql_password>
   ```
    Replace the placeholders (`<...>`) with the appropriate values.

### Running with Python

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the `main.py` script:
   ```bash
   python main.py
   ```

### Running with Docker

1. Build the Docker image:
   ```bash
   docker build -t lch-data-scraper .
   ```
2. Run the Docker container:
   ```bash
   docker run --env-file .env lch-data-scraper
   ```

## Authors

- Ali Moghimi ([alimghmi](https://github.com/alimghmi))
- Clemens Struck ([clemstruck](https://github.com/clemstruck))


## Contribution

Contributions are welcome! Fork the repository, apply your changes, and submit a pull request.
