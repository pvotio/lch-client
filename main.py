from config import logger, settings
from scraper import Engine
from transformer import Agent
from utils.db_helper import init_db_instance


def main():
    logger.info("Initializing Scraper Engine")
    engine = Engine(
        max_retries=settings.REQUEST_MAX_RETRIES,
        backoff_factor=settings.REQUEST_BACKOFF_FACTOR,
    )
    df = engine.fetch()
    logger.info("Transforming Data")
    df_transformed = Agent(df).transform()
    logger.info(f"\n{df_transformed}")
    logger.info("Preparing Database Inserter")
    inserter = init_db_instance()
    logger.info(f"Inserting Data into {settings.OUTPUT_TABLE}")
    inserter.insert_table(df_transformed, settings.OUTPUT_TABLE)
    logger.info("Application completed successfully")
    return


if __name__ == "__main__":
    main()
