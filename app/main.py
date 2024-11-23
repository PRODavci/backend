import multiprocessing
import os

import click
import uvicorn

from consumer import start_consumer
from core.config import get_config
from core.logging import logger


@click.command()
@click.option(
    "--env",
    type=click.Choice(["dev", "prod"], case_sensitive=False),
    default="dev",
)
@click.option(
    "--debug",
    type=click.BOOL,
    is_flag=True,
    default=False,
)
@click.option(
    "--workers",
    type=click.INT,
    default=1,
)
def main(env: str = "dev", debug: bool = False, workers: int = 1):
    os.environ["ENV"] = env
    os.environ["DEBUG"] = str(debug)

    config = get_config()
    logger.info("Application start")
    logger.info(f"Config: {config.as_dict()}")

    uvicorn.run(
        app="app:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        workers=workers,
    )


if __name__ == "__main__":
    process = multiprocessing.Process(target=start_consumer)
    process.start()
    main()
    process.join()
