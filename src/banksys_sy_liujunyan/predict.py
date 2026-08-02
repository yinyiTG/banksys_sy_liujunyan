"""在线预测:加载模型,把单条输入转换为特征并进行推理。"""

import joblib
import pandas as pd

from .data_loader import CATEGORICAL_COLUMNS, NUMERIC_COLUMNS
from .features import FEATURE_COLUMNS

DEFAULT_MODEL_PATH = "models/best_model.joblib"

_POSITIVE_LABEL = "yes"


def load_model(model_path: str = DEFAULT_MODEL_PATH):
    """加载训练好的 pipeline 模型。"""
    return joblib.load(model_path)


def predict_one(model, row: dict) -> dict:
    """对单条输入做推理。

    row 需包含全部 FEATURE_COLUMNS;返回认购结论与概率。
    """
    missing = set(FEATURE_COLUMNS) - set(row.keys())
    if missing:
        raise ValueError(f"输入缺少字段: {sorted(missing)}")

    sample = pd.DataFrame([row], columns=FEATURE_COLUMNS)
    for col in CATEGORICAL_COLUMNS:
        if col in sample.columns:
            sample[col] = sample[col].astype(str)
    for col in NUMERIC_COLUMNS:
        sample[col] = pd.to_numeric(sample[col], errors="raise")

    proba = float(model.predict_proba(sample)[0, 1])
    pred = _POSITIVE_LABEL if proba >= 0.5 else "no"
    return {"subscribe": pred, "probability": proba}
