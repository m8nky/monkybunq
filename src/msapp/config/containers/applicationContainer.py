from dependency_injector import containers, providers
from msapp.application import App

# http://python-dependency-injector.ets-labs.org/examples/bundles_miniapp.html
class ApplicationContainer(containers.DeclarativeContainer):
    _config = providers.Configuration('app')
    _configParser = providers.Callable(App.cliParser)
    _config.from_dict(_configParser())
    main = providers.Selector(
        _config.cmd,
        info=providers.Callable(App.info),
        distribute=providers.Callable(App.distribute),
        cashimport=providers.Callable(App.cashimport)
    )
