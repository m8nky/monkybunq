from typing import Iterable
from .transactionItem import TransactionItem


class Bank:
    def info(self):
        raise NotImplementedError("abstract")

    def transfer(self, source: dict, targets: list):
        raise NotImplementedError("abstract")

    @staticmethod
    def printTask(source: TransactionItem, targets: Iterable[TransactionItem]):
        print(f"Distribute '{str(source.amount)}' from '{source.iban}'...")
        for target in targets:
            print(f" -> '{str(target.amount)}' to '{target.iban}'")
