from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)
from pathlib import Path
from loguru import logger

class Settings(BaseSettings):
    
    toml_file: str
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        toml_settings = TomlConfigSettingsSource(settings_cls, toml_file=init_settings().get("toml_file"))
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            toml_settings,
        )

class AgentConfig(Settings):
    pass


class IndexConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )
    index_name: str
    pinecone_api_key: str
    region: str
    model: str


class PreprocessorConfig(BaseModel):
    chunk_size: int
    chunk_overlap: int
    folder_path: str  

class IndexerConfig(Settings):

    preprocessor: PreprocessorConfig
    index: IndexConfig



def get_indexer_config(toml_file: str = "config/indexer.toml") -> IndexerConfig:
    """Load indexer configuration from TOML file."""

    config = IndexerConfig(toml_file= toml_file)
    logger.info(f"Successfully loaded indexer configuration")
    return config

def get_agent_config(toml_file: str = "./config/agent.toml") -> AgentConfig:
    config = AgentConfig(toml_file=toml_file)
    logger.info(f"Successfully loaded agent configuration")
    return config