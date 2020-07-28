from decimal import Decimal
from msapp.monetaryDistribution.datamapper import MonetaryDistribution


class DistributorService:
    def __init__(self, distributionValueObject: MonetaryDistribution):
        self._source = distributionValueObject.source()
        self._targets = distributionValueObject.targets()

    def distribute(self):
        self._validate()
        self._source.bank.transfer(self._source, self._targets)

    def _validate(self):
        sumTargets = sum([x.amount for x in self._targets])
        diff = self._source.amount - sumTargets
        assert diff <= Decimal(0.01) and not diff.is_signed(), f"Sum targets {sumTargets} does not match expected transaction volume {self._source.amount}."
