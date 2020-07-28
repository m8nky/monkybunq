from dependency_injector import containers, providers
from .configContainer import ConfigContainer
from msapp.cash.datamapper import GnucashXmlReader
from msapp.datastore.gateway import Gsheet
from msapp.cash.domain.service import CashService


class CashServiceContainer(containers.DeclarativeContainer):
    _importer = providers.Factory(
        GnucashXmlReader,
        xmlFilename=ConfigContainer.config.cash.gnucash.xmlFilename
    )
    _exporter = providers.Factory(
        Gsheet,
        auth=ConfigContainer.config.gsheet.auth,
        documentKey=ConfigContainer.config.cash.gsheet.sheetId,
        worksheet=ConfigContainer.config.cash.gsheet.worksheet
    )
    cashService = providers.Factory(
        CashService,
        importer=_importer,
        exporter=_exporter,
        latestDateKey=ConfigContainer.config.cash.datamap.latestDateKey,
        accountsMapping=ConfigContainer.config.cash.datamap.accountsMapping
    )
