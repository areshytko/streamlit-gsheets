import argparse

import streamlit as st

from {{cookiecutter.project_package}}.config import Config
from {{cookiecutter.project_package}}.gsheets import GoogleSheetsLoader
from {{cookiecutter.project_package}}.load import RawData
from {{cookiecutter.project_package}}.transform import ProcessedData
import {{cookiecutter.project_package}}.widgets as wg

st.set_page_config(layout="wide")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Productivity Dashboard')
    parser.add_argument('config', default='./config/default.yml', help='path to config file', nargs='?')
    return parser.parse_args()


@st.cache
def load_data(config: Config) -> RawData:
    sa_info = config.get_service_account_info()
    gsheets = GoogleSheetsLoader(sa_info=sa_info)
    return RawData.load(gsheets=gsheets, config=config)


args = parse_arguments()
config = Config.load(args.config)

wg.sidebar(config=config)

raw_data = load_data(config=config)
data = ProcessedData.process(raw_data=raw_data)

wg.data_bar_chart(data)
