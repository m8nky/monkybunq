from typing import Dict, TypedDict, Iterable
from msapp.cash.domain.cashTransaction import CashTransaction


class CashServiceImporter:
    class CashType(TypedDict):
        accounts: Dict[str, TypedDict('Account', {'name': str})]
        transactions: Iterable[CashTransaction]

    def __init__(self):
        pass

    def process(self) -> CashType:
        raise NotImplementedError('abstract')
