"""离线训练:加载数据、划分、训练、评估,输出模型产物与指标。"""

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    auc,
    f1_score,
    precision_score,
    recall_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from .data_loader import TARGET_COLUMN, load_data
from .features import FEATURE_COLUMNS, build_preprocessor

RANDOM_SEED = 42
VAL_RATIO = 0.2
AUC_THRESHOLD = 0.80

DEFAULT_MODEL_PATH = Path("models/best_model.joblib")
DEFAULT_METRICS_PATH = Path("models/metrics.json")


@dataclass
class TrainingResult:
    """一次训练的输出摘要。"""

    auc: float
    f1: float
    precision: float
    recall: float
    threshold: float
    n_train: int
    n_val: int
    model_path: str
    metrics_path: str


def build_model() -> Pipeline:
    """构建预处理 + 分类器的完整 pipeline(固定随机种子,可复现)。"""
    return Pipeline(
        steps=[
            ("preprocess", build_preprocessor()),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=300,
                    max_depth=18,
                    min_samples_leaf=2,
                    class_weight="balanced",
                    random_state=RANDOM_SEED,
                    n_jobs=-1,
                ),
            ),
        ]
    )


def evaluate(model: Pipeline, X_val: pd.DataFrame, y_val: pd.Series) -> dict:
    """在验证集上计算二分类指标,返回各阈值下的 auc 与默认阈值下的 f1/p/r。"""
    proba = model.predict_proba(X_val)[:, 1]
    y_pred = model.predict(X_val)

    fpr, tpr, _ = roc_curve(y_val, proba, pos_label="yes")
    return {
        "auc": float(auc(fpr, tpr)),
        "f1": float(f1_score(y_val, y_pred, pos_label="yes")),
        "precision": float(precision_score(y_val, y_pred, pos_label="yes")),
        "recall": float(recall_score(y_val, y_pred, pos_label="yes")),
        "threshold": 0.5,
    }


def train(
    data_path: str | Path,
    model_path: str | Path = DEFAULT_MODEL_PATH,
    metrics_path: str | Path = DEFAULT_METRICS_PATH,
) -> TrainingResult:
    """主训练流程:划分 -> 训练 -> 评估 -> 保存模型与指标。

    指标不达门槛(AUC_THRESHOLD)时抛出异常,阻止不合格产物进入在线预测。
    """
    df = load_data(data_path)
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=VAL_RATIO, random_state=RANDOM_SEED, stratify=y
    )

    model = build_model()
    model.fit(X_train, y_train)

    metrics = evaluate(model, X_val, y_val)
    if metrics["auc"] < AUC_THRESHOLD:
        raise RuntimeError(f"AUC={metrics['auc']:.3f} 低于门槛 {AUC_THRESHOLD},拒绝保存模型")

    model_path = Path(model_path)
    metrics_path = Path(metrics_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    metrics_path.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")

    return TrainingResult(
        auc=metrics["auc"],
        f1=metrics["f1"],
        precision=metrics["precision"],
        recall=metrics["recall"],
        threshold=metrics["threshold"],
        n_train=int(len(X_train)),
        n_val=int(len(X_val)),
        model_path=str(model_path),
        metrics_path=str(metrics_path),
    )


def main() -> None:
    """命令行入口:python -m src.banksys_sy_liujunyan.train"""
    result = train("data/train.csv")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
