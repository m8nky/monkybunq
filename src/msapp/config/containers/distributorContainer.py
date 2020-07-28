from dependency_injector import containers, providers
from .configContainer import ConfigContainer
from msapp.datastore.gateway import Gsheet
from msapp.monetaryDistribution.datamapper import MonetaryDistribution
from msapp.monetaryDistribution.domain.service import DistributorService
from .bankContainer import BankContainer


class DistributorContainer(containers.DeclarativeContainer):
    _distributionDataSource = providers.Factory(
        Gsheet,
        auth=ConfigContainer.config.gsheet.auth,
        documentKey=ConfigContainer.config.distributor.gsheet.sheetId,
        worksheet=ConfigContainer.config.distributor.gsheet.worksheet
    )
    _distributionData = providers.Factory(
        MonetaryDistribution,
        transactionItemFactory=BankContainer.transactionItemFactory.provider,
        distributionDataSource=_distributionDataSource,
        distributionConfig=ConfigContainer.config.distributor.distribution
    )
    distributorService = providers.Factory(
        DistributorService,
        distributionValueObject=_distributionData
    )
