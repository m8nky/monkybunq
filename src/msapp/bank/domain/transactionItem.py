from msapp.bank.domain.repository import BankRepository
from typing import ForwardRef
from decimal import Decimal


Bank = ForwardRef('msapp.bank.domain.Bank')


class TransactionItem:
    bankRepository = None

    @staticmethod
    def create(data: dict, bankRepository: BankRepository):
        bank = bankRepository.probe(data['bank'])
        bank = bank if not None else data['bank']
        if 'subject' not in data or len(data['subject']) == 0:
            data['subject'] = data['name'];
        return TransactionItem(data['name'], bank, data['iban'], data['recipient'], data['subject'], data['value'])

    def __init__(self, name: str, bank: [str, Bank], iban: str, recipient: str, subject: str, value: Decimal):
        self._name = name
        self._bank = bank
        self._iban = iban
        self._recipient = recipient
        self._subject = subject
        self._value = value

    @property
    def name(self) -> str:
        return self._name

    @property
    def bank(self) -> [Bank, str]:
        return self._bank

    @property
    def iban(self) -> str:
        return self._iban

    @property
    def recipient(self) -> str:
        return self._recipient

    @property
    def subject(self) -> str:
        return self._subject

    @property
    def amount(self) -> Decimal:
        return self._value
