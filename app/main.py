import os

import click
import uvicorn


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
def main(env: str = "dev", debug: bool = False):
    os.environ["ENV"] = env
    os.environ["DEBUG"] = str(debug)

    from core.config import config

    uvicorn.run(
        app="app:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=(env != "prod"),
    )


if __name__ == "__main__":
    main()
