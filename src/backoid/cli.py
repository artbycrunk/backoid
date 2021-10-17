from argparse import ArgumentParser, Namespace


from .config import Config
from .logger import Logger

DEFAULT_CONFIG_FILE = "./test_config.yml"


def parse_options():
    parser: ArgumentParser = ArgumentParser(
        description=("Setup backups for various tools")
    )
    parser.add_argument(
        "--config-file",
        help="Config file to use. By default, {} .".format(DEFAULT_CONFIG_FILE),
        default=DEFAULT_CONFIG_FILE,
    )

    options: Namespace = parser.parse_args().__dict__
    return options


def main():
    options = parse_options()

    logger = Logger(logfile="./log/backoid-backup", logger_name="backoid")
    config = Config(options["config_file"], logger=logger)
    print(config.config)
