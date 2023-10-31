import datetime

import pandas as pd

from config import logger


class Agent:
    COLUMNS_NAME = {
        "Valuation Date": "valuation_date",
        "Instrument": "instrument",
        "Instrument Name": "instrument_name",
        "Series": "series",
        "Version": "version",
        "Contractual Definitions": "contractual_definitions",
        "Fixed Rate": "fixed_rate",
        "Maturity": "maturity",
        "Index Factor": "index_factor",
        "Markit LCH Settlement Price": "price",
        "Ticker": "ticker",
        "Tier": "tier",
        "Doc Clause": "doc_clause",
    }

    def __init__(self, df: pd.DataFrame) -> None:
        self.dataframe = df

    def transform(self) -> pd.DataFrame:
        logger.info("Starting data transformation.")
        try:
            self.parse_date()
            logger.debug("Parsed dates successfully.")
            self.add_timestamp()
            logger.debug("Added timestamps successfully.")
            self.rename_columns()
            logger.debug("Renamed columns successfully.")
        except Exception as e:
            logger.error(f"Data transformation failed. Error: {e}")
            raise

        logger.info("Data transformation completed successfully.")
        logger.debug(f"\n{self.dataframe}")
        return self.dataframe

    def parse_date(self) -> None:
        try:
            self.dataframe["Valuation Date"] = pd.to_datetime(
                self.dataframe["Valuation Date"], format="%Y-%m-%d"
            )
            self.dataframe["Maturity"] = pd.to_datetime(
                self.dataframe["Maturity"], format="%Y-%m-%d"
            )
        except Exception as e:
            logger.error(f"Failed to parse dates. Error: {e}")
            raise

    def add_timestamp(self) -> None:
        try:
            self.dataframe["timestamp_created_utc"] = datetime.datetime.utcnow()
        except Exception as e:
            logger.error(f"Failed to add timestamps. Error: {e}")
            raise

    def rename_columns(self) -> None:
        try:
            self.dataframe.rename(columns=self.COLUMNS_NAME, inplace=True)
        except Exception as e:
            logger.error(f"Failed to rename columns. Error: {e}")
            raise
