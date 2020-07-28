import argparse
from msapp.config.containers.bankContainer import BankContainer
from msapp.config.containers.distributorContainer import DistributorContainer
from msapp.config.containers.cashServiceContainer import CashServiceContainer


class App:
    @staticmethod
    def cliParser():
        commands = ['info', 'distribute', 'cashimport']
        parser = argparse.ArgumentParser(description="monkybunq")
        parser.add_argument('cmd', help=' | '.join(commands), choices=commands)
        parser.add_argument('--dry', help="Do not issue transactions or modify DB values.", action='store_true')
        return vars(parser.parse_args())

    @staticmethod
    def info():
        bankRepository = BankContainer.bankRepository()
        bank = bankRepository.probe('Bunq')
        bank.info()

    @staticmethod
    def distribute():
        distributorService = DistributorContainer.distributorService()
        distributorService.distribute()

    @staticmethod
    def cashimport():
        cashService = CashServiceContainer.cashService()
        cashService.importCashBalance()
