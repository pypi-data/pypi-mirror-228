"""
Programme's Global Settings.

Cannot use logger. That would cause Cyclical Dependency OR double or triple logging of the same message
"""

__all__ = ['GlobalSettingsModelSingleton', 'GlobalSettingsModel']

import logging
from pathlib import Path
from typing import List, Optional, Dict, Set, Any

import yaml
from pydantic import Field, model_validator

from api_compose.core.events.base import EventType
from api_compose.core.settings.yaml_settings import YamlBaseSettings, BaseSettings, SettingsConfigDict
from api_compose.services.persistence_service.models.enum import BackendProcessorEnum
from api_compose.services.reporting_service.models.enum import ReportProcessorEnum


class ActionSettings(BaseSettings):
    pass


class BackendSettings(BaseSettings):
    processor: BackendProcessorEnum = BackendProcessorEnum.SimpleBackend


class CliContext(BaseSettings):
    model_config = SettingsConfigDict(extra='allow')


class CliOptions(BaseSettings):
    is_interactive: bool = Field(False,
                                 description='When True, users will be prompted to create assertions dynamically at the end of each Scenario Run')
    cli_context: CliContext = Field(CliContext(), description='context passed via CLI')
    tags: Set[str] = set()
    select: Optional[str] = ''

    @model_validator(mode='before')
    @classmethod
    def validate_tags_and_select_not_set_together(cls, values):
        select = values.get('select')
        tags = values.get('tags')
        if select and tags:
            raise ValueError(f'Tags and Select cannot be set at the same time. Display \n'
                             f'{select=}, {tags=}')
        return values


class DiscoverySettings(BaseSettings):
    env_file_path: Optional[Path] = Path('env.yaml')
    manifests_folder_path: Path = Path.cwd().joinpath('manifests')
    functions_folder_path: Path = Path.cwd().joinpath('functions')
    tags: Set[str] = set()


class LoggingSettings(BaseSettings):
    logging_level: int = logging.INFO
    log_file_path: Optional[Path] = Path.cwd().joinpath('log.jsonl')
    event_filters: List[EventType] = []


class ReportingSettings(BaseSettings):
    processor: ReportProcessorEnum = ReportProcessorEnum.HtmlReport
    reports_folder: Path = Path('reports')


class GlobalSettingsModel(YamlBaseSettings):
    action: ActionSettings = ActionSettings()
    backend: BackendSettings = BackendSettings()
    build_folder: Path = Path().cwd().joinpath('build')
    cli_options: CliOptions = Field(CliOptions(), exclude=True)
    compiled_folder: Path = Path('compiled')
    discovery: DiscoverySettings = DiscoverySettings()
    logging: LoggingSettings = LoggingSettings()
    reporting: ReportingSettings = ReportingSettings()
    run_folder: Path = Path('run')

    model_config = SettingsConfigDict(
        env_nested_delimiter='__',
        yaml_file="config.yaml",
        env_prefix='acp__',
        extra='forbid'
    )

    @property
    def env_vars(self) -> Dict[str, Any]:
        if self.discovery.env_file_path.exists():
            with open(self.discovery.env_file_path, 'r') as f:
                return yaml.load(f, Loader=yaml.FullLoader)
        else:
            return {}


class GlobalSettingsModelSingleton():
    _GLOBAL_SETTINGS_MODEL: Optional[GlobalSettingsModel] = None

    @classmethod
    def set(cls):
        cls._GLOBAL_SETTINGS_MODEL = GlobalSettingsModel()

    @classmethod
    def get(cls) -> GlobalSettingsModel:
        if cls._GLOBAL_SETTINGS_MODEL is None:
            raise ValueError('Global Settings Model not yet created!')
        return cls._GLOBAL_SETTINGS_MODEL
