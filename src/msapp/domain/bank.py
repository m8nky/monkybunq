class TransactionItem:
    pass


class Bank:
    _banks = {}

    @staticmethod
    def probeBank(name: str):
        if name in Bank._banks:
            return Bank._banks[name]
        return None

    def __init__(self):
        Bank._banks[self.__class__.__name__] = self

    def transfer(self, source: dict, targets: list):
        raise NotImplementedError("abstract")

    @staticmethod
    def printTask(source: TransactionItem, targets: list):
        print(f"Distribute '{str(source.amount)}' from '{source.iban}'...")
        for target in targets:
            print(f" -> '{str(target.amount)}' to '{target.iban}'")
