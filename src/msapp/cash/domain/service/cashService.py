from msapp.datastore.gateway import Gsheet
from msapp.cash.domain.repository import AccountRepository
from .cashServiceImporter import CashServiceImporter
from datetime import datetime, timezone


class CashService:
    def __init__(self, importer: CashServiceImporter, exporter: Gsheet, latestDateKey: str, accountsMapping: dict):
        self._importer = importer
        # TODO: Decouple Gsheet as KVStore
        self._exporter = exporter
        self._latestDateKey = latestDateKey
        self._accountsMapping = accountsMapping

    def importCashBalance(self) -> None:
        cash = self._importer.process()
        latestTransactionDate, accountsSum = AccountRepository.accountsSum(cash['transactions'])
        #gdate = (recentDate - datetime(1899, 12, 30, tzinfo=timezone.utc)).days
        gdate = latestTransactionDate.strftime('%d.%m.%Y')
        self._exporter.setValue(self._latestDateKey, gdate)
        for account, aSum in accountsSum.items():
            if account in self._accountsMapping:
                self._exporter.setValue(self._accountsMapping[account], aSum)
