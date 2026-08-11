import asyncio

from aitest.main import main


def cli_entrypoint():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    cli_entrypoint()
