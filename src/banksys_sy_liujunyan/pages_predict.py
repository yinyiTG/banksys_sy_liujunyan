"""在线预测页面:点选式输入客户信息,实时返回认购预测。"""

import pandas as pd
import streamlit as st

from .data_loader import CATEGORICAL_COLUMNS, NUMERIC_COLUMNS
from .predict import DEFAULT_MODEL_PATH, load_model, predict_one
from .ui import field_label


def _categorical_input(df: pd.DataFrame, column: str) -> str:
    """分类字段:从训练数据取值域生成下拉选择。"""
    options = sorted(df[column].dropna().unique().astype(str))
    return st.selectbox(
        f"{field_label(column)}",
        options=options,
        key=f"pred_cat_{column}",
    )


def _numeric_input(df: pd.DataFrame, column: str) -> float:
    """数值字段:用训练数据的 min/max 作为输入范围。"""
    lo = float(df[column].min())
    hi = float(df[column].max())
    default = float(df[column].median())
    return st.number_input(
        f"{field_label(column)}",
        min_value=lo,
        max_value=hi,
        value=default,
        step=0.01,
        key=f"pred_num_{column}",
    )


def render_predict_page(df: pd.DataFrame) -> None:
    """渲染在线预测页面主体。"""
    st.title("在线认购预测")
    st.caption("录入客户信息,预测其是否会认购定期存款(点选式输入)")

    model_path = st.session_state.get("model_path", DEFAULT_MODEL_PATH)

    with st.sidebar:
        st.subheader("客户信息录入")
        row: dict = {}
        for col in CATEGORICAL_COLUMNS:
            row[col] = _categorical_input(df, col)
        for col in NUMERIC_COLUMNS:
            row[col] = _numeric_input(df, col)

    if st.button("预测", type="primary"):
        try:
            model = load_model(model_path)
            result = predict_one(model, row)
        except FileNotFoundError:
            st.error(
                f"模型文件 {model_path} 不存在,请先运行离线训练:"
                "`python -m src.banksys_sy_liujunyan.train`"
            )
            return

        proba = result["probability"]
        label = "认购" if result["subscribe"] == "yes" else "未认购"
        st.subheader("预测结果")
        st.metric("预测结论", label)
        st.metric("认购概率", f"{proba:.1%}")
        st.progress(min(proba, 1.0))
        st.write("说明:概率 ≥ 50% 判定为「认购」,模型 AUC = 0.89(训练集验证)。")
