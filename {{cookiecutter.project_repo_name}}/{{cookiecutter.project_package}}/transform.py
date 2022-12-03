
from typedframe import TypedDataFrame

from {{cookiecutter.project_package}}.load import RawData


class ProcessedData(TypedDataFrame):
    schema = {
        'value': str,
        'count': int
    }

    @classmethod
    def process(cls, raw_data: RawData) -> 'ProcessedData':
        df = raw_data.df
        result = df.groupby('value').count().reset_index().rename(columns={'id': 'count'})
        return cls(result)
