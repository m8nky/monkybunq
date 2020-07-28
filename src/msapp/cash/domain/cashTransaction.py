from decimal import Decimal
from datetime import datetime
from typing import TypedDict, Iterable


class CashTransaction:
    class SplitsType(TypedDict):
        account: str
        quantity: Decimal

    def __init__(self, _id: str, date: datetime, splits: Iterable[SplitsType]):
        self._id = _id
        self._date = date
        self._splits = splits

    def id(self) -> str:
        return self._id

    def date(self) -> datetime:
        return self._date

    def splits(self) -> Iterable[SplitsType]:
        return self._splits
