from decimal import Decimal
from datetime import datetime
from typing import Tuple, List, Dict
from msapp.cash.domain import CashTransaction


class AccountRepository:
    @staticmethod
    def accountsSum(transactions: List[CashTransaction]) -> Tuple[datetime, Dict[str, Decimal]]:
        accounts = {}
        maxDate = None
        for t in transactions:
            for s in t.splits():
                if s['account'] not in accounts:
                    accounts[s['account']] = Decimal(0)
                accounts[s['account']] += s['quantity']
                maxDate = max(maxDate, t.date()) if maxDate is not None else t.date()
        return maxDate, accounts
