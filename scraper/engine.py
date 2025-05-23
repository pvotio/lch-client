import pandas as pd
import requests
from bs4 import BeautifulSoup

from config import logger
from utils import Request


class Engine:

    BASE_URL = "https://www.lseg.com/en/post-trade/clearing/lch-services/cdsclear/essentials/pricing-data"  # noqa: E501

    def __init__(self, max_retries, backoff_factor):
        self.data = {}
        self.dfs = {}
        self.request = Request(
            max_retries=max_retries, backoff_factor=backoff_factor
        ).request

    def fetch(self):
        logger.info("Starting fetch process")
        self.fetch_api_endpoints()
        logger.debug(
            f"Discovered {len(self.api_endpoints)} API endpoints: {self.api_endpoints}"
        )
        self.get_content()
        logger.debug(f"Fetched content for endpoints: {list(self.data.keys())}")
        self.convert_to_df()
        logger.debug(
            f"Converted content to DataFrames for keys: {list(self.dfs.keys())}"
        )
        self.validate_data()
        df = self.concat_tables()
        logger.debug(
            f"Concatenated DataFrame: {df.shape[0]} rows, {df.shape[1]} columns"
        )
        logger.info(f"Extracted {len(df)} rows.")
        return df

    def get_content(self):
        logger.info("Fetching content from API endpoints")
        for url in self.api_endpoints:
            logger.debug(f"Requesting URL: {url}")
            try:
                r = self.request("GET", url)
                r.raise_for_status()
                payload = r.json()
                key = url.split("/")[-1]
                data = payload.get("Data", payload)
                self.data[key] = data
                logger.info(
                    f"Successfully fetched data for '{key}', {len(data) if isinstance(data, list) else 'unknown'} records"  # noqa: E501
                )
            except requests.RequestException as e:
                logger.error(f"Error fetching content from {url}: {e}")

    def convert_to_df(self):
        logger.info("Converting fetched data to pandas DataFrames")
        for key, data in self.data.items():
            try:
                df = pd.DataFrame(data)
                self.dfs[key] = df
                logger.info(
                    f"Converted '{key}' to DataFrame with {len(df)} rows and {len(df.columns)} columns"  # noqa: E501
                )
            except Exception as e:
                logger.error(f"Error converting data for '{key}' to DataFrame: {e}")
                raise

    def validate_data(self):
        logger.info("Validating DataFrames")
        empty_frames = [key for key, df in self.dfs.items() if df.empty]
        if empty_frames:
            logger.error(
                f"Data validation failed. Empty DataFrames for keys: {empty_frames}"
            )
            raise ValueError("No price data provided by the provider as of now.")
        logger.debug("Data validation succeeded. All DataFrames contain data.")

    def fetch_api_endpoints(self):
        logger.info(f"Fetching API endpoints from base URL: {self.BASE_URL}")
        try:
            resp = self.request("GET", self.BASE_URL)
            resp.raise_for_status()
            bs4 = BeautifulSoup(resp.text, features="lxml")
            divs = bs4.find_all(
                "div", attrs={"data-rehydratable": "DataGridEnterprise"}
            )
            self.api_endpoints = [
                self.BASE_URL.split("/en")[0] + div["data-api-url"] for div in divs
            ]
            logger.info(f"Found {len(self.api_endpoints)} endpoints:")
            for url in self.api_endpoints:
                logger.info(f"  - {url}")
        except requests.RequestException as e:
            logger.error(f"Error fetching API endpoints: {e}")
            raise

    def concat_tables(self):
        logger.info("Concatenating DataFrames into final DataFrame")
        try:
            tables = list(self.dfs.values())[:2]
            result = pd.concat(tables, axis=0).reset_index(drop=True)
            logger.debug(f"Resulting DataFrame shape: {result.shape}")
            return result
        except Exception as e:
            logger.error(f"Error concatenating tables: {e}")
            raise
