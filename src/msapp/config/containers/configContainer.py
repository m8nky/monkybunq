from dependency_injector import containers, providers
from msapp.config.configProvider import ConfigProvider


class ConfigContainer(containers.DeclarativeContainer):
    _config_provider = providers.Factory(ConfigProvider)
    config = providers.Configuration('config')
    config.from_dict(_config_provider().getConfig())
