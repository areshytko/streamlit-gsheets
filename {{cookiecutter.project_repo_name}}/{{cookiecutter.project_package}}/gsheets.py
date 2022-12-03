"""
Fetching data from google sheets
"""

from typing import Any, List, Optional

import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build

READ_SCOPE = 'https://www.googleapis.com/auth/spreadsheets.readonly'


class GoogleSheetsLoader:

    def __init__(self, sa_info: dict):
        self._sa_info = sa_info
        self._token = None

    def get_token(self) -> Optional[Credentials]:
        if not self._token:
            self._authenticate()

        if self._token and self._token.expired and self._token.refresh_token:
            self._token.refresh(Request())

        return self._token

    def _authenticate(self):
        self._token = service_account.Credentials.from_service_account_info(self._sa_info)

    def _pull_sheet_data(self, spreadsheet_id: str, range_name: str) -> List[List[Any]]:
        """
        Pulls data from Google Sheets API

        Parameters
        ----------
        token : Credentials
            OAuth2 token see :ref:`ManualFlow` or :ref:`LocalServerFlow`
        spreadsheet_id : str
            id of the spreadsheet (you can copy it from a spreadsheet URL)
        range_name : str
            see range [A1 notation](https://developers.google.com/sheets/api/guides/concepts#a1_notation)

        Returns
        -------
        List[List[Any]]
            list of rows from a given spreadsheet range
        """
        creds = self.get_token()
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()  # pylint: disable=no-member
        result = sheet.values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name).execute()
        values = result.get('values', [])
        return values

    def get_data(self,
                 spreadsheet_id: str,
                 range_name: str,
                 columns: Optional[List[str]] = None,
                 merged_cols: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Pulls data from Google Sheets API and transforms it into a pandas DataFrame.

        Parameters
        ----------
        token : Credentials
            OAuth2 token see :ref:`ManualFlow` or :ref:`LocalServerFlow`
        spreadsheet_id : str
            id of the spreadsheet (you can copy it from a spreadsheet URL)
        range_name : str
            see range [A1 notation](https://developers.google.com/sheets/api/guides/concepts#a1_notation)
        columns: Optional[List[str]]
            optional schema, if not provided first row of the range is considered as column names
        merged_cols: Optional[List[str]]
            columns that contain merged cells. Google Sheet doesn't copy the value to each merged row
        """

        data = self._pull_sheet_data(spreadsheet_id=spreadsheet_id, range_name=range_name)
        if columns:
            df = pd.DataFrame(data, columns=columns)
        else:
            df = pd.DataFrame(data[1:], columns=data[0])

        df = df.replace([''], [None])

        if merged_cols:
            df[merged_cols] = df[merged_cols].ffill()

        return df
