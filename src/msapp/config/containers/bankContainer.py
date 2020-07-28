from dependency_injector import containers, providers
from .configContainer import ConfigContainer
from msapp.bank.domain.repository import BankRepository
from msapp.bank.domain import Bunq
from msapp.bank.domain import TransactionItem


class BankContainer(containers.DeclarativeContainer):
    _bunqPrivateAccount = providers.Singleton(
        Bunq,
        apiKey=ConfigContainer.config.bank.bunq.apiKey,
        authConfigFile=ConfigContainer.config.bank.bunq.auth.configFile,
        apiContextDescription=ConfigContainer.config.bank.bunq.apiContextDescription,
        sandboxMode=ConfigContainer.config.dry
    )
    bankRepository = providers.Singleton(
        BankRepository,
        banks={'Bunq': _bunqPrivateAccount}
    )
    transactionItemFactory = providers.Callable(
        TransactionItem.create,
        bankRepository=bankRepository
    )
