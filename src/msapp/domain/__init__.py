from .transactionItem import TransactionItem
from .bunq import Bunq
from msapp.config import ConfigProvider
bunq = None


def init():
    global bunq
    bunq = Bunq(ConfigProvider())
