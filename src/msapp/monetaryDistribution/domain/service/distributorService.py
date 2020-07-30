from decimal import Decimal
import logging
from msapp.monetaryDistribution.datamapper import MonetaryDistribution


class DistributorService:
    _l = logging.getLogger(__name__)

    def __init__(self, distributionValueObject: MonetaryDistribution):
        self._source = distributionValueObject.source()
        self._targets = distributionValueObject.targets()

    def distribute(self):
        # Drop transactions with negative or zero amounts.
        self._filterNegativeZero()
        # Validate sum of transferred amounts match the source amount.
        self._validate()
        # Initiate transaction.
        self._source.bank.transfer(self._source, self._targets)

    def _filterNegativeZero(self):
        targets = []
        for t in self._targets:
            if t.amount > Decimal(0):
                targets.append(t)
            else:
                DistributorService._l.info(f"Omitting transaction of zero or negative amount: '{t.name}' - '{t.iban}' ({t.subject})")
        self._targets = targets

    def _validate(self):
        sumTargets = sum([x.amount for x in self._targets])
        diff = self._source.amount - sumTargets
        assert diff <= Decimal(0.01) and not diff.is_signed(), f"Sum targets {sumTargets} does not match expected transaction volume {self._source.amount}."
