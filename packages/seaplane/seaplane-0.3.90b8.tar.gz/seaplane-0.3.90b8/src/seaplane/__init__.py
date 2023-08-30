from importlib.metadata import version

from .api.api_substation import SubstationAPI
from .api.sql_api import GlobalSQL
from .api.token_api import TokenAPI
from .apps import App, Task, app, build, context, start, task
from .configuration import Configuration, config
from .logging import log

__version__ = version(__name__)


class Seaplane:
    @property
    def config(self) -> Configuration:
        return config

    @property
    def auth(self) -> TokenAPI:
        return config._token_api

    @property
    def substation(self) -> SubstationAPI:
        return SubstationAPI(config)

    @property
    def global_sql(self) -> GlobalSQL:
        return GlobalSQL(config)


sea = Seaplane()

__all__ = ["App", "Task", "task", "app", "start", "log", "context", "build"]
