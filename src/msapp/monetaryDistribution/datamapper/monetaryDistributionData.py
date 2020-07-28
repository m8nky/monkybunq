from decimal import Decimal
from typing import Callable, Iterable, ForwardRef
import re
from msapp.datastore.gateway import Gsheet

TransactionItem = ForwardRef('msapp.bank.domain.TransactionItem')


class MonetaryDistributionData:
    def __init__(self, transactionItemFactory: Callable, distributionDataSource: Gsheet, distributionConfig: dict):
        self._transactionItemFactory = transactionItemFactory
        self._dataSource = distributionDataSource
        assert 'source' in distributionConfig and 'targets' in distributionConfig, "ERROR: Distribution configuration missing."
        self._config = distributionConfig

    def source(self) -> TransactionItem:
        return self._assembleTransactionItem(self._config['source'])

    def targets(self) -> Iterable[TransactionItem]:
        targets = []
        for target in self._config['targets']:
            targets.append(self._assembleTransactionItem(target))
        return targets

    def _assembleTransactionItem(self, transactionItem: dict) -> TransactionItem:
        if type(transactionItem['value']) is dict:
            transactionItem['value'] = self._getDatastoreValue(transactionItem['value'], MonetaryDistributionData._fetchMonetaryValue)
        return self._transactionItemFactory(data=transactionItem)

    def _fetchMonetaryValue(self, cell: str) -> Decimal:
        value = self._dataSource.getValue(cell)
        value = re.sub(r'€', '', value)
        value = re.sub(r',', '', value)
        value = Decimal(value)
        return value

    def _getDatastoreValue(self, valueDict: dict, replacer: Callable):
        assert 'worksheetCell' in valueDict
        return replacer(self, valueDict['worksheetCell'])
