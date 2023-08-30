import configparser
import logging
import os
from rc.api_client import APIClient, APIClientError
from rc.exceptions import RcException

from rc.dirs import app_config_dir

logger = logging.getLogger(__name__)


class ConfigError(RcException):
    def __init__(self, msg):
        super().__init__(msg)


RAGA_CONFIG_FILE = f"{app_config_dir()}/config"

DEFAULT_CONFIG_VALUES = {
    "rc_base_url": "https://example.com"
}

class CoreConfig():
    CONFIG_FILE_PATH = os.path.expanduser(os.path.join("~", RAGA_CONFIG_FILE))
    def __init__(self, profile) -> None:
        self.DEFAULT_PROFILE = profile

    def read_raga_config(self):
        if not os.path.isfile(self.CONFIG_FILE_PATH):
            self.create_default_config()
            ConfigError(f"A default config file has been created. Please update the credentials in the config file. You can update using this command `sudo vim {self.CONFIG_FILE_PATH}`")
        config = configparser.ConfigParser()
        try:
            config.read(self.CONFIG_FILE_PATH)
        except configparser.Error as e:
            raise ConfigError(f"Invalid config file format: {str(e)}")

        self.validate_default_section(config)

        config_data = {section: dict(config.items(section)) for section in config.sections()}
        return config_data

    def create_default_config(self):
        config = configparser.ConfigParser()
        config.add_section(self.DEFAULT_PROFILE)

        for option, value in DEFAULT_CONFIG_VALUES.items():
            config.set(self.DEFAULT_PROFILE, option, value)

        os.makedirs(os.path.dirname(self.CONFIG_FILE_PATH), exist_ok=True)

        with open(self.CONFIG_FILE_PATH, "w") as config_file:
            config.write(config_file)

    def validate_default_section(self, config):
        if self.DEFAULT_PROFILE not in config:
             raise ConfigError(f"profile '{self.DEFAULT_PROFILE}' not found in config data.")
        default_section = config[self.DEFAULT_PROFILE]
        for option, default_value in DEFAULT_CONFIG_VALUES.items():
            if option not in default_section or default_section[option] == default_value:
                raise ConfigError(f"please update the value of '{option}' in the [{self.DEFAULT_PROFILE}] section of the config file. You can update using this command `sudo vim {self.CONFIG_FILE_PATH}`")

    def get_core_config_value(self, option):
        section = self.DEFAULT_PROFILE
        config_data = self.read_raga_config()  # Load config data using the instance method
        if section in config_data:
            section_data = config_data[section]
            if option in section_data:
                return section_data[option]
            raise ConfigError(f"option '{option}' not found in profile '{section}'.")
        raise ConfigError(f"profile '{section}' not found in config data.")
    
    def get_all_core_configs(self, profile):
        config_data = self.read_raga_config()  # Load config data using the instance method
        if profile in config_data:
            return config_data[profile]
    

class Config(CoreConfig):
    from rc.required_config_keys import REQUIRED_KEYS
    def __init__(self, profile, required_keys=REQUIRED_KEYS):
        super().__init__(profile)
        self.core_config = self.get_all_core_configs(profile)
        self.config_dict = self._store_config_values(self.get_config_values_from_server())
        self.required_keys = required_keys or []

        missing_keys = [key for key in self.required_keys if key not in self.config_dict]
        if missing_keys:
            raise ConfigError(f"required config keys are missing: {', '.join(missing_keys)}")
    
    def _store_config_values(self, config_data):
        config_dict = {}
        for item in config_data:
            config_dict[item['conf_key']] = item['conf_value']
        return config_dict
    
    def get_config_value(self, key):
        value = self.config_dict.get(key, None)
        if value is None:
            raise ConfigError(f"key '{key}' not found in configuration")
        return value
    
    def get_config_values_from_server(self):
        with APIClient(self.core_config.get("rc_base_url")) as client:
            response = client.get("configs")
            if response:
                data = response.json()
                data = data.get('data', None)
                if data:
                    return data
                else:
                    raise APIClientError(f"no record found")
            else:
                raise APIClientError(f"something went wrong")
            