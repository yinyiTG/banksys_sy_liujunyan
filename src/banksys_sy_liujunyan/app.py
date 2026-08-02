"""Streamlit 入口:数据分析页 + 在线预测页。"""

import streamlit as st

from banksys_sy_liujunyan.data_loader import load_data
from banksys_sy_liujunyan.pages_eda import render_eda_page
from banksys_sy_liujunyan.pages_predict import render_predict_page

DATA_PATH = "data/train.csv"

st.set_page_config(page_title="银行营销分析", layout="wide")


@st.cache_data
def load_dataset() -> object:
    return load_data(DATA_PATH)


def main() -> None:
    df = load_dataset()

    page = st.sidebar.radio(
        "功能",
        options=["数据分析", "在线预测"],
        index=0,
    )

    if page == "数据分析":
        render_eda_page(df)
    else:
        render_predict_page(df)


if __name__ == "__main__":
    main()
