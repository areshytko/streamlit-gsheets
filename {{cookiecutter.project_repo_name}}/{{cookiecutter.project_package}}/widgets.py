

import streamlit as st

from {{cookiecutter.project_package}}.config import Config
from {{cookiecutter.project_package}}.transform import ProcessedData


def sidebar(config: Config):
    config.spreadsheet_id = st.sidebar.text_input(
        "Spreadsheet id",
        value=config.spreadsheet_id
    )
    config.spreadsheet_range = st.sidebar.text_input(
        "Spreadsheet range",
        value=config.spreadsheet_range
    )


def data_bar_chart(data: ProcessedData):
    st.subheader("Example Chart:")
    st.bar_chart(data.df.set_index('value'), y='count')
