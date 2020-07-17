import gspread
from msapp.config import ConfigProvider


class Gsheet:
    def __init__(self, configProvider: ConfigProvider, documentKey: str, worksheet: str = None):
        self._config = configProvider.getConfig(self.__class__.__name__)
        gc = gspread.service_account(filename=self._config['auth']['configFile'])
        self._document = gc.open_by_key(documentKey)
        if worksheet is not None:
            self._activeWorksheet = self._document.worksheet(worksheet)

    def activeWorksheet(self, worksheet: str = None) -> str:
        if worksheet is not None:
            self._activeWorksheet = self._document.worksheet(worksheet)
        assert worksheet is not None
        return self._activeWorksheet

    def getValue(self, cell: str):
        return self._activeWorksheet.acell(cell).value


'''
    def getMonetaryValue(self, cell: str) -> Decimal:
        value = self.activeWorksheet.acell(cell).value
        value = re.sub(r'€', '', value)
        value = re.sub(r',', '', value)
        value = Decimal(value)
        print(value)
        return value
'''
