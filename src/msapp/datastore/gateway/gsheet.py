import gspread
import os
import logging
from msapp.datastore.exceptions import DatastoreException


class Gsheet:
    _l = logging.getLogger(__name__)

    def __init__(self, auth: dict, documentKey: str, worksheet: str = None):
        assert 'configFile' in auth and os.path.isfile(auth['configFile']), f"ERROR: GSheet auth does not have a service account config file."
        self._auth = auth
        self._documentKey = documentKey
        self._initialWorksheet = worksheet
        self._document = None
        self._activeWorksheet = None

    def _initDocument(self):
        if not self._document:
            try:
                gc = gspread.service_account(filename=self._auth['configFile'])
                self._document = gc.open_by_key(self._documentKey)
            except Exception:
                Gsheet._l.exception(f"Error opening document")
                raise DatastoreException("Datastore can not be initialized")

    def activeWorksheet(self, worksheet: str = None) -> [gspread.models.Worksheet]:
        self._initDocument()
        if self._activeWorksheet is None:
            worksheet = worksheet if worksheet is not None else self._initialWorksheet
        if worksheet is not None:
            try:
                self._activeWorksheet = self._document.worksheet(worksheet)
            except gspread.exceptions.WorksheetNotFound:
                Gsheet._l.exception(f"Error activating worksheet '{worksheet}'")
        if not self._activeWorksheet:
            raise DatastoreException("Active worksheet is not set in datastore.")
        return self._activeWorksheet

    def getValue(self, cell: str):
        return self.activeWorksheet().acell(cell).value

    def setValue(self, cell: str, value) -> None:
        self.activeWorksheet().update(cell, value)
