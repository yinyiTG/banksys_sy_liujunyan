"""数据分析的计算逻辑,与 UI 分离,方便测试与复用。"""

import pandas as pd

from .data_loader import TARGET_COLUMN


def overview(df: pd.DataFrame) -> pd.DataFrame:
    """返回数据概览:每列的字段类型、缺失数、唯一值数量。"""
    rows = []
    for col in df.columns:
        rows.append(
            {
                "字段": col,
                "类型": str(df[col].dtype),
                "缺失数": int(df[col].isna().sum()),
                "唯一值数": int(df[col].nunique()),
            }
        )
    return pd.DataFrame(rows)


def target_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """返回目标变量 subscribe 的计数与占比。"""
    counts = df[TARGET_COLUMN].value_counts()
    return pd.DataFrame({"数量": counts, "占比": counts / counts.sum()})


def column_distribution(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """返回指定列的值分布(计数与占比)。"""
    counts = df[column].value_counts()
    return pd.DataFrame({"数量": counts, "占比": counts / counts.sum()})


def numeric_summary(df: pd.DataFrame, column: str) -> dict:
    """返回数值列的统计摘要。"""
    return df[column].describe().to_dict()


def filter_dataframe(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """按筛选条件过滤数据。

    filters 形如 {"job": "admin.", "housing": "yes", "age_min": 30, "age_max": 60}。
    只应用已给定的键;空字典返回原数据。
    """
    result = df.copy()
    for column, value in filters.items():
        if value is None or value == []:
            continue
        if column.endswith("_min") and isinstance(value, (int, float)):
            base = column[:-4]
            result = result[result[base] >= value]
        elif column.endswith("_max") and isinstance(value, (int, float)):
            base = column[:-4]
            result = result[result[base] <= value]
        elif isinstance(value, (list, tuple)) and len(value) > 0:
            result = result[result[column].isin(value)]
        elif isinstance(value, str) and value != "全部":
            result = result[result[column] == value]
    return result
