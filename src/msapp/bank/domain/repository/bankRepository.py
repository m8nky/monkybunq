from typing import Dict, ForwardRef
from dependency_injector.providers import Factory

Bank = ForwardRef('msapp.bank.domain.Bank')


class BankRepository:
    def __init__(self, banks: Dict[str, Factory]):
        self._banks = banks

    def probe(self, bank: str) -> [Bank, None]:
        bankFactory = self._banks.get(bank, None)
        return bankFactory() if bankFactory is not None else None
