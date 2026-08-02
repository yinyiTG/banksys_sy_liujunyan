"""数据加载与基础校验。"""

from pathlib import Path

import pandas as pd

TARGET_COLUMN = "subscribe"
ID_COLUMN = "id"

CATEGORICAL_COLUMNS = [
    "job",
    "marital",
    "education",
    "default",
    "housing",
    "loan",
    "contact",
    "month",
    "day_of_week",
    "poutcome",
]

NUMERIC_COLUMNS = [
    "age",
    "duration",
    "campaign",
    "pdays",
    "previous",
    "emp_var_rate",
    "cons_price_index",
    "cons_conf_index",
    "lending_rate3m",
    "nr_employed",
]


def load_data(path: str | Path) -> pd.DataFrame:
    """加载 CSV 数据并做基础校验。

    - 缺失目标列或特征列时报错。
    - 目标列非二分类时按列报错。
    """
    df = pd.read_csv(path)

    required = [ID_COLUMN, TARGET_COLUMN, *CATEGORICAL_COLUMNS, *NUMERIC_COLUMNS]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"数据缺少必要列: {missing}")

    if set(df[TARGET_COLUMN].unique()) != {"yes", "no"}:
        raise ValueError(f"目标列 {TARGET_COLUMN} 取值必须为 yes/no")

    return df
