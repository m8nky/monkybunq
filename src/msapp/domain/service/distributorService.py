from msapp.datamapper import MonetaryDistribution
from decimal import Decimal


class DistributorService:
    def __init__(self, monetaryDistributionConfig: MonetaryDistribution):
        self._source = monetaryDistributionConfig.source()
        self._targets = monetaryDistributionConfig.targets()

    def distribute(self):
        bank = self._source.bank
        self._validate()
        bank.transfer(self._source, self._targets)

    def _validate(self):
        sumTargets = sum([x.amount for x in self._targets])
        diff = self._source.amount - sumTargets
        assert diff <= Decimal(0.01) and not diff.is_signed(), f"Sum targets {sumTargets} does not match expected transaction volume {self._source.amount}."
