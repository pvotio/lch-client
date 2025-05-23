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

    def fetch(self) -> pd.DataFrame:
        self.fetch_api_endpoints()
        self.get_content()
        self.convert_to_df()
        self.validate_data()
        df = self.concat_tables()
        logger.debug(f"\n{df}")
        logger.info(f"Extracted {len(df)} rows.")
        return df

    def get_content(self) -> str:
        for url in self.api_endpoints:
            try:
                r = self.request("GET", url)
                r.raise_for_status()
                self.data[url.split("/")[-1]] = (
                    r.json()["Data"] if "Data" in r.json() else r.json()
                )
            except requests.RequestException as e:
                logger.error(f"Error fetching content from {url}. Error: {e}")

    def convert_to_df(self):
        for key, data in self.data.items():
            self.dfs[key] = pd.DataFrame(data)

    def validate_data(self):
        if not all([len(df) for df in self.dfs]):
            logger.error("Data validation failed")
            raise ValueError("No price data provided by the provider as of now.")

        logger.debug("Data validation succeeded.")

    def fetch_api_endpoints(self):
        resp = self.request("GET", self.BASE_URL)
        bs4 = BeautifulSoup(resp.text, features="lxml")
        divs = bs4.find_all("div", attrs={"data-rehydratable": "DataGridEnterprise"})
        self.api_endpoints = [
            self.BASE_URL.split("/en")[0] + div["data-api-url"] for div in divs
        ]

        for url in self.api_endpoints:
            logger.info(url)

    def concat_tables(self):
        # Filter out third table on Pricing Data page
        return pd.concat(list(self.dfs.values())[:2], axis=0).reset_index(drop=True)
