from .bank import Bank
from decimal import Decimal


class TransactionItem:
    def __init__(self, data: dict):
        assert 'name' in data
        assert 'bank' in data
        assert 'iban' in data
        assert 'recipient' in data
        assert 'value' in data
        self._item = data

    @property
    def name(self) -> str:
        return self._item['name']

    @property
    def bank(self) -> [Bank, None]:
        bank = Bank.probeBank(self._item['bank'])
        return self._item['bank'] if bank is None else bank

    @property
    def iban(self) -> str:
        return self._item['iban']

    @property
    def recipient(self) -> str:
        return self._item['recipient']

    @property
    def amount(self) -> Decimal:
        return self._item['value']
