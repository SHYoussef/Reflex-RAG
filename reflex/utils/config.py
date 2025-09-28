from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

class Settings(BaseSettings):
    toml_file: str = None  # field to hold the path

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # Use the toml_file attribute if provided, else default
        toml_path = getattr(settings_cls, "toml_file", None)
        if toml_path:
            toml_source = TomlConfigSettingsSource(settings_cls, toml_file=toml_path)
        else:
            toml_source = TomlConfigSettingsSource(settings_cls)
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            toml_source,
        )

class AgentConfig(Settings):
    pass


class IndexConfig(Settings):
    chunk_size: int
    chunk_overlap: int
    folder_path: str
    index_name: str
    pinecone_api_key: str
    region: str
    model: str


def get_index_config(toml_file: str = "./config/index.toml") -> IndexConfig:
    return IndexConfig(toml_file=toml_file)

def get_reflex_config(toml_file: str = "./config/agent.toml") -> AgentConfig:
    return AgentConfig(toml_file=toml_file)