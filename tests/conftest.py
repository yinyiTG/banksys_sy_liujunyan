"""pytest 共享 fixture。"""

import pandas as pd
import pytest

from banksys_sy_liujunyan.data_loader import CATEGORICAL_COLUMNS


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """构造一个覆盖全部必需列的小样本数据集。"""
    data = {
        "id": [1, 2, 3, 4, 5],
        "age": [51, 50, 48, 26, 45],
        "job": ["admin.", "services", "blue-collar", "entrepreneur", "admin."],
        "marital": ["divorced", "married", "divorced", "single", "married"],
        "education": [
            "professional.course",
            "high.school",
            "basic.9y",
            "high.school",
            "university.degree",
        ],
        "default": ["no", "unknown", "no", "yes", "no"],
        "housing": ["yes", "yes", "no", "yes", "no"],
        "loan": ["yes", "no", "no", "yes", "no"],
        "contact": ["cellular", "cellular", "cellular", "cellular", "cellular"],
        "month": ["aug", "may", "apr", "aug", "nov"],
        "day_of_week": ["mon", "mon", "wed", "fri", "tue"],
        "duration": [4621, 4715, 171, 359, 3178],
        "campaign": [1, 1, 0, 26, 1],
        "pdays": [112, 412, 1027, 998, 240],
        "previous": [2, 2, 1, 0, 4],
        "poutcome": ["failure", "nonexistent", "failure", "nonexistent", "success"],
        "emp_var_rate": [1.4, -1.8, -1.8, 1.4, -3.4],
        "cons_price_index": [90.81, 96.33, 96.33, 97.08, 89.82],
        "cons_conf_index": [-35.53, -40.58, -44.74, -35.55, -33.83],
        "lending_rate3m": [0.69, 4.05, 1.5, 5.11, 1.17],
        "nr_employed": [5219.74, 4974.79, 5022.61, 5222.87, 4884.7],
        "subscribe": ["no", "yes", "no", "yes", "no"],
    }
    df = pd.DataFrame(data)
    for col in CATEGORICAL_COLUMNS:
        df[col] = df[col].astype("category")
    return df
