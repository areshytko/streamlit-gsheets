
from typedframe import TypedDataFrame

from {{cookiecutter.project_package}}.config import Config
from {{cookiecutter.project_package}}.gsheets import GoogleSheetsLoader


class RawData(TypedDataFrame):
    schema = {
        'id': int,
        'value': str
    }

    @classmethod
    def load(cls, gsheets: GoogleSheetsLoader, config: Config) -> 'RawData':
        df = gsheets.get_data(
            spreadsheet_id=config.spreadsheet_id,
            range_name=config.spreadsheet_range
        )
        return cls.convert(df)
