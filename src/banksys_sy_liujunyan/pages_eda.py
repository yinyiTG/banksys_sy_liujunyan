"""数据分析交互页面。"""

import pandas as pd
import streamlit as st

from .data_loader import CATEGORICAL_COLUMNS, NUMERIC_COLUMNS, TARGET_COLUMN
from .eda import (
    column_distribution,
    filter_dataframe,
    numeric_summary,
    overview,
    target_distribution,
)
from .ui import FEATURE_COLUMNS, field_label


def _sidebar_filters(df: pd.DataFrame) -> dict:
    """构建侧边栏筛选器,返回 filter_dataframe 可用的筛选字典。"""
    filters: dict = {}
    with st.sidebar:
        st.subheader("筛选条件")
        for col in CATEGORICAL_COLUMNS:
            values = sorted(df[col].dropna().unique())
            selected = st.multiselect(
                f"{field_label(col)}(可多选)",
                options=values,
                default=[],
                key=f"filt_{col}",
            )
            if selected:
                filters[col] = selected
        for col in NUMERIC_COLUMNS:
            lo = float(df[col].min())
            hi = float(df[col].max())
            if lo >= hi:
                continue
            min_v, max_v = st.slider(
                f"{field_label(col)}范围",
                min_value=lo,
                max_value=hi,
                value=(lo, hi),
                key=f"filt_{col}",
            )
            filters[f"{col}_min"] = min_v
            filters[f"{col}_max"] = max_v
    return filters


def _render_plots(df: pd.DataFrame) -> None:
    """渲染各类分布图。"""
    st.subheader("目标变量分布")
    target = target_distribution(df)
    st.bar_chart(target["数量"])

    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("分类字段分布")
        cat_col = st.selectbox(
            "选择分类字段",
            options=CATEGORICAL_COLUMNS,
            format_func=field_label,
            key="eda_cat_col",
        )
        dist = column_distribution(df, cat_col)
        st.bar_chart(dist["数量"])
    with col_right:
        st.subheader("数值字段分布")
        num_col = st.selectbox(
            "选择数值字段",
            options=NUMERIC_COLUMNS,
            format_func=field_label,
            key="eda_num_col",
        )
        st.write(numeric_summary(df, num_col))
        dist_num = df[num_col]
        st.bar_chart(dist_num.value_counts().sort_index().head(20))


def render_eda_page(df: pd.DataFrame) -> None:
    """渲染数据分析页面主体。"""
    st.title("银行营销数据分析")
    st.caption("基于营销数据 train.csv,分析哪些客户更容易认购定期存款")

    filters = _sidebar_filters(df)
    filtered = filter_dataframe(df, filters)

    st.subheader("数据概览")
    st.write(f"总记录数 **{len(df)}**,当前筛选后 **{len(filtered)}**")
    st.dataframe(overview(filtered))

    st.subheader("原始数据预览")
    st.dataframe(filtered.head(100))

    _render_plots(filtered)

    # 认购率按关键特征交叉对比
    st.subheader("认购率对比")
    cross_col = st.selectbox(
        "选择交叉特征",
        options=FEATURE_COLUMNS,
        format_func=field_label,
        key="eda_cross_col",
    )
    rate = filtered.groupby(cross_col)[TARGET_COLUMN].apply(lambda s: (s == "yes").mean())
    st.bar_chart(rate)
