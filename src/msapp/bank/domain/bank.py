from typing import Iterable
import logging
from .transactionItem import TransactionItem


class Bank:
    _l = logging.getLogger(__name__)

    def info(self):
        raise NotImplementedError("abstract")

    def transfer(self, source: dict, targets: list):
        raise NotImplementedError("abstract")

    @staticmethod
    def printTask(source: TransactionItem, targets: Iterable[TransactionItem]):
        loglines = [f"Distribute '{str(source.amount)}' from '{source.iban}'..."]
        loglines += [f" -> '{str(t.amount)}' to '{t.iban}' ({t.subject})" for t in targets]
        Bank._l.info('\n'.join(loglines))
