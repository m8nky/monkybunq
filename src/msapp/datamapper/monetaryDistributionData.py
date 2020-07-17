from decimal import Decimal
from typing import Callable
import re
from msapp.config import ConfigProvider
from msapp.gateway import Gsheet
from msapp.domain import TransactionItem


class MonetaryDistributionData:
    def __init__(self, configProvider: ConfigProvider):
        self._config = configProvider.getConfig(self.__class__.__name__)
        self._gsheet = Gsheet(configProvider, self._config['sheetId'], self._config['worksheet'])

    def source(self) -> TransactionItem:
        return self._assembleTransactionItem(self._config['distribution']['source'])

    def targets(self) -> list:
        targets = []
        for target in self._config['distribution']['targets']:
            targets.append(self._assembleTransactionItem(target))
        return targets

    def _assembleTransactionItem(self, transactionItem: dict) -> TransactionItem:
        if type(transactionItem['value']) is dict:
            transactionItem['value'] = self._getWorksheetValue(transactionItem['value'], MonetaryDistributionData._fetchMonetaryValue)
        return TransactionItem(transactionItem)

    def _fetchMonetaryValue(self, cell: str) -> Decimal:
        value = self._gsheet.getValue(cell)
        value = re.sub(r'€', '', value)
        value = re.sub(r',', '', value)
        value = Decimal(value)
        return value

    def _getWorksheetValue(self, valueDict: dict, replacer: Callable):
        assert 'worksheetCell' in valueDict
        return replacer(self, valueDict['worksheetCell'])
