import configparser
from pathlib import Path
from typing import Any, Optional

from g3.domain.message_tone import MessageTone

CONFIG_DIR = ".g3"
CONFIG_FILE = "config"


class ConfigHandler:
    def __init__(self, config_path: Path = Path.home()):
        self.config_path = config_path / CONFIG_DIR
        self.config_file = self.config_path / CONFIG_FILE
        self.config = self.load_config()
        self.properties = self.load_properties()

    @property
    def as_dict(self) -> dict[str, Any]:
        return self.properties

    @property
    def github_token(self) -> str:
        return self.properties.get("github_token", "")

    @property
    def openai_key(self) -> str:
        return self.properties.get("openai_key", "")

    @property
    def api_base(self) -> Optional[str]:
        return self.properties.get("api_base")

    @property
    def deployment_id(self) -> Optional[str]:
        return self.properties.get("deployment_id")

    @property
    def api_type(self) -> Optional[str]:
        return self.properties.get("api_type")

    @property
    def model(self) -> str:
        return self.properties.get("model", "gpt-4-0613")

    @property
    def temperature(self) -> float:
        if not self.properties.get("temperature"):
            return 0

        return float(self.properties.get("temperature", "0"))

    @property
    def api_version(self) -> Optional[str]:
        return self.properties.get("api_version")

    @property
    def message_tone(self) -> Optional[MessageTone]:
        return MessageTone(self.tone) if self.tone else None

    @property
    def tone(self) -> Optional[str]:
        return self.properties.get("tone")

    @property
    def commit_description_max_words(self) -> int:
        return int(self.properties.get("commit_description_max_words", "50"))

    @property
    def pr_description_max_words(self) -> int:
        return int(self.properties.get("pr_description_max_words", "500"))

    def has_been_configured(self) -> bool:
        return self.config.has_section("credentials")

    def get(self, section: str, key: str, default: Optional[str] = None) -> Optional[str]:
        try:
            return self.config[section][key]
        except KeyError:
            return default

    def set(self, section: str, key: str, value: str):
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value

    def load_config(self) -> configparser.ConfigParser:
        self.config_path.mkdir(exist_ok=True)
        self.config_file.touch(exist_ok=True)

        parser = configparser.ConfigParser()
        parser.read(self.config_file)
        return parser

    def load_properties(self) -> dict[str, Any]:
        properties = {}
        for section in self.config.sections():
            for key, value in self.config.items(section):
                properties[key] = value

        return properties

    def save_config(self):
        with open(self.config_file, "w") as f:
            self.config.write(f)


class Defaults:
    def __init__(self, file_config: ConfigHandler):
        self.github_token = self.set_defaults(file_config.github_token)
        self.openai_key = self.set_defaults(file_config.openai_key)
        self.api_base = self.set_defaults(file_config.api_base)
        self.deployment_id = self.set_defaults(file_config.deployment_id)
        self.api_type = self.set_defaults(file_config.api_type, "open_ai")
        self.model = self.set_defaults(file_config.model, "gpt-4-0613")
        self.temperature = self.set_defaults(file_config.temperature, 0.0)
        self.api_version = self.set_defaults(file_config.api_version, "latest")
        self.tone = self.set_defaults(file_config.tone, MessageTone.FRIENDLY.value)
        self.commit_description_max_words = self.set_defaults(file_config.commit_description_max_words, 50)
        self.pr_description_max_words = self.set_defaults(file_config.pr_description_max_words, 500)

    def set_defaults(self, value, default=None):
        return value if value is not None else default
