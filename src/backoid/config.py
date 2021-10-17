import configparser
import os
import re
import sys

import yaml

from .helpers import MetaSingleton


class Config(metaclass=MetaSingleton):

    def __repr__(self):
        return f'<Config {hex(id(self))}>'

    def __init__(self, config_file, logger=None):
        self.config = self.parse_file(config_file, logger=logger)

    def yaml_lookup_environment(self):
        env_pattern = re.compile(r".*?\${(.*?)}.*?")

        def env_constructor(loader, node):
            value = loader.construct_scalar(node)
            for group in env_pattern.findall(value):
                value = value.replace(f"${{{group}}}", os.environ.get(group, value))
            return value

        yaml.add_implicit_resolver("!pathex", env_pattern)
        yaml.add_constructor("!pathex", env_constructor)
        return yaml


    def parse_yaml(self, config_file, logger=None):
        try:
            self.yaml_lookup_environment()
            config = yaml.load(open(config_file), Loader=yaml.FullLoader)
        except yaml.YAMLError:
            if logger:
                logger.error(
                    "Error opening or parsing the YAML file {}".format(config_file)
                )
            return
        except FileNotFoundError:
            if logger:
                logger.error("File {} not found".format(config_file))
            sys.exit(2)
        return config


    def parse_conf(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        return config


    def parse_file(self, config_file, logger=None):
        """
        Parses the configuration file parameters.

        :return: parser object
        """
        if os.path.splitext(config_file)[-1] == ".conf":
            return self.parse_conf(config_file)
        return self.parse_yaml(config_file, logger=logger)
