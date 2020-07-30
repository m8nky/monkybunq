from decimal import Decimal
import logging
from bunq import ApiEnvironmentType
from bunq.sdk.context.api_context import ApiContext
from bunq.sdk.exception.bunq_exception import BunqException
from bunq.sdk.model.generated import endpoint
from bunq.sdk.model.generated.endpoint import MonetaryAccountBank, MonetaryAccountSavings
from bunq.sdk.model.generated.object_ import Amount, DraftPaymentEntry, Pointer
from msapp.bank.gateway.share_lib import ShareLib
from msapp.bank.gateway.bunq_lib import BunqLib
from .bank import Bank
from .transactionItem import TransactionItem


class Bunq(Bank):
    _l = logging.getLogger(__name__)

    def __init__(self, apiKey: str, authConfigFile: str, apiContextDescription: str, sandboxMode: bool):
        self._apiKey = apiKey
        self._authConfigFile = authConfigFile
        self._contextDescription = apiContextDescription
        self._isDryRun = sandboxMode
        if self._isDryRun:
            Bunq._l.info("Running in 'sandbox' mode. Transactions will not be executed.")
        # Re-open or create bunq context/session
        try:
            BunqLib._BUNQ_CONF_PRODUCTION = self._authConfigFile
            self.bunq = BunqLib(ApiEnvironmentType.PRODUCTION)
        except BunqException:
            self.createContext()
            self.bunq = BunqLib(ApiEnvironmentType.PRODUCTION)
        self.accounts = self.bunq.get_all_monetary_account_active()
        self.bunq.update_context()

    def createContext(self):
        ShareLib.print_header()
        ApiContext.create(
            ApiEnvironmentType.PRODUCTION,
            self._apiKey,
            self._contextDescription
        ).save(self._authConfigFile)

    def info(self):
        ShareLib.print_header()
        user = self.bunq.get_current_user()
        ShareLib.print_user(user)
        ShareLib.print_all_monetary_account_bank(self.accounts)
        self.bunq.update_context()

    def transfer(self, source: TransactionItem, targets: list):
        Bunq.printTask(source, targets)
        sourceAccount = self.getMonetaryAccountByIban(source.iban)
        assert isinstance(sourceAccount, MonetaryAccountBank), f"Monetary account not found for '{source.iban}'."
        drafts = []
        for target in targets:
            assert isinstance(target, TransactionItem)
            # Probe target IBAN is Bunq account of current user.
            targetAccount = self.getMonetaryAccountByIban(target.iban)
            if targetAccount is not None:
                # Bunq internal user account.
                targetAccount = Bunq.getMonetaryAccountPointer(targetAccount)
            else:
                # External Bunq user or bank account.
                targetAccount = Bunq.getExternalIbanPointer(target.iban, target.recipient)
            assert isinstance(targetAccount, Pointer)
            drafts.append(Bunq.draftPaymentEntryByValue(sourceAccount, targetAccount, target.amount, target.subject))
        if len(drafts) <= 0:
            return
        res = Bunq.draftPayment(sourceAccount, drafts) if not self._isDryRun else 0
        print(f"Draft payment initiated with ID {res}")
        self.bunq.update_context()

    def getMonetaryAccountByIban(self, iban: str) -> [MonetaryAccountBank, MonetaryAccountSavings, None]:
        for account in self.accounts:
            if iban == Bunq.getMonetaryAccountPointer(account).value:
                return account
        return None

    @staticmethod
    def getMonetaryAccountPointer(monetaryAccount: [MonetaryAccountBank, MonetaryAccountSavings]) -> [Pointer]:
        return list(filter(lambda x: x.type_ == "IBAN", monetaryAccount.alias))[0]

    @staticmethod
    def getExternalIbanPointer(iban: str, recipient: str) -> [Pointer]:
        return Pointer("IBAN", iban, recipient)

    @staticmethod
    def draftPayment(source: MonetaryAccountBank, drafts: list) -> int:
        return endpoint.DraftPayment.create(drafts, number_of_required_accepts=1, status="PENDING", monetary_account_id=source.id_).value

    @staticmethod
    def draftPaymentEntryByValue(
            input_account: MonetaryAccountBank,
            output_account: Pointer,
            value: Decimal,
            description: str
    ) -> DraftPaymentEntry:
        return DraftPaymentEntry(
            Amount(str(value), input_account.currency),
            output_account,
            description
        )
