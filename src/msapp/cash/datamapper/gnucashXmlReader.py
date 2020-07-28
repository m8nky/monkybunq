#!/usr/bin/env python3
import logging
import re
from lxml import etree
from decimal import Decimal
from datetime import datetime
from msapp.cash.domain.service import CashServiceImporter
from msapp.cash.domain import CashTransaction


class GnucashXmlReader(CashServiceImporter):
    _l = logging.getLogger(__name__)
    NS = {
        'gnc': "http://www.gnucash.org/XML/gnc",
        'act': "http://www.gnucash.org/XML/act",
        'book': "http://www.gnucash.org/XML/book",
        'cd': "http://www.gnucash.org/XML/cd",
        'cmdty': "http://www.gnucash.org/XML/cmdty",
        'price': "http://www.gnucash.org/XML/price",
        'slot': "http://www.gnucash.org/XML/slot",
        'split': "http://www.gnucash.org/XML/split",
        'trn': "http://www.gnucash.org/XML/trn",
        'ts': "http://www.gnucash.org/XML/ts",
        'sx': "http://www.gnucash.org/XML/sx",
        'bgt': "http://www.gnucash.org/XML/bgt",
        'recurrence': "http://www.gnucash.org/XML/recurrence"
    }

    def __init__(self, xmlFilename: str):
        super().__init__()
        self._xmlFile = xmlFilename
        self._accounts = {}
        self._transactions = []

    def process(self) -> CashServiceImporter.CashType:
        data = self._readXml()
        self._extractAccountData(data)
        self._extractTransactionData(data)
        return {
            'accounts': self._accounts,
            'transactions': [ GnucashXmlReader._createTransactionValueObject(t) for t in self._transactions ]
        }

    @staticmethod
    def _node(ns: str, element: str) -> str:
        return f'{{{GnucashXmlReader.NS[ns]}}}{element}'

    def _readXml(self):
        try:
            parser = etree.XMLParser(remove_blank_text=True)
            t = etree.parse(self._xmlFile, parser)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            GnucashXmlReader._l.exception(f"ERROR: Parsing XML file '{self._xmlFile}' - {str(e)}")
            return None
        return t.getroot()

    def _extractAccountData(self, data) -> None:
        self._accounts = {}
        for account in [node for node in data.iterfind(f".//{GnucashXmlReader._node('gnc', 'account')}")]:
            _id = account.find(f"./{GnucashXmlReader._node('act', 'id')}").text
            name = account.find(f"./{GnucashXmlReader._node('act', 'name')}").text
            self._accounts[_id] = {
                'name': name
            }

    def _extractTransactionData(self, data) -> None:
        def _toDecimal(by100: str) -> Decimal:
            m = re.match(r'^(?P<value>-?\d+)/100$', by100).groupdict()
            assert 'value' in m and len(m['value']) > 0, "ERROR: Quantity malformed."
            return Decimal(m['value']) / Decimal(100)
        self._transactions = []
        for transaction in [node for node in data.iterfind(f".//{GnucashXmlReader._node('gnc', 'transaction')}")]:
            _id = transaction.find(f"./{GnucashXmlReader._node('trn', 'id')}").text
            date = transaction.find(f"./{GnucashXmlReader._node('trn', 'date-posted')}/{GnucashXmlReader._node('ts', 'date')}").text
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S %z')
            splits = []
            for split in [node for node in transaction.iterfind(f".//{GnucashXmlReader._node('trn', 'split')}")]:
                account = split.find(f"./{GnucashXmlReader._node('split', 'account')}").text
                account = self._accounts[account]
                quantity = split.find(f"./{GnucashXmlReader._node('split', 'quantity')}").text
                quantity = _toDecimal(quantity)
                splits.append(
                    {
                        'account': account,
                        'quantity': quantity
                    }
                )
            self._transactions.append(
                {
                    'id': _id,
                    'date': date,
                    'splits': splits
                }
            )

    @staticmethod
    def _createTransactionValueObject(transaction: dict) -> CashTransaction:
        _id = transaction['id']
        date = transaction['date']
        assert type(date) is datetime, f"ERROR: Invalid date '{date}'."
        splits = []
        for entry in transaction['splits']:
            assert type(entry['account']) is dict and 'name' in entry['account']
            assert isinstance(entry['quantity'], Decimal)
            splits.append(
                {
                    'account': entry['account']['name'],
                    'quantity': entry['quantity']
                }
            )
        return CashTransaction(_id, date, splits)
