from typing import List

import pandas as pd
import requests

from config import logger
from utils import Request


class Engine:
    def __init__(self, url: str, max_retries: int, backoff_factor: int) -> None:
        self.url = url
        self.request = Request(max_retries=max_retries, backoff_factor=backoff_factor)

    def fetch(self, content: str = None) -> pd.DataFrame:
        logger.debug(f"Attempting to fetch content from {self.url}.")
        if not content:
            content = self.get_content()
            logger.debug(
                f"Successfully fetched content from {self.url}. Now parsing the content."  # noqa: E501
            )
        else:
            logger.debug(
                "Successfully loaded the content from the user provided argument. Now parsing the content."  # noqa: E501
            )

        dfs = self.parse_html(content)
        logger.debug(f"\n{dfs}")
        self.validate_data(dfs)
        df = self.concat_tables(dfs)
        logger.info(f"Parsed content from {self.url}. Extracted {len(df)} rows.")
        return df

    def get_content(self) -> str:
        try:
            data = {"form_id": "lch_data_token_cookie_accept_terms", "op": "Accept"}
            r = self.request.request("POST", self.url, data=data)
            r.raise_for_status()
            return r.text
        except requests.RequestException as e:
            logger.error(f"Error fetching content from {self.url}. Error: {e}")
            raise ConnectionError(f"Failed to connect to {self.url}.") from e

    def parse_html(self, content: str) -> pd.DataFrame:
        try:
            dfs = pd.read_html(content)
        except Exception as e:
            logger.error(f"Error parsing HTML via pandas. Error: {e}")
            raise e

        if len(dfs):
            logger.debug(
                f"Successfully parsed content from {self.url}. Extracted {len(dfs)} tables."  # noqa: E501
            )
            return dfs
        else:
            raise ValueError(f"No data found when parsing content from {self.url}.")

    def validate_data(self, dfs: List[pd.DataFrame]) -> None:
        if not all([len(df) for df in dfs]):
            logger.error("Data validation failed")
            raise ValueError("No price data provided by the provider as of now.")

        logger.debug("Data validation succeeded.")

    def concat_tables(self, dfs: List[pd.DataFrame]) -> pd.DataFrame:
        return pd.concat(dfs[:2], axis=0).reset_index()
