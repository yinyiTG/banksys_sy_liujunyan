"""特征工程与离线训练的单元测试。"""

import pandas as pd

from banksys_sy_liujunyan.data_loader import TARGET_COLUMN
from banksys_sy_liujunyan.features import (
    FEATURE_COLUMNS,
    build_preprocessor,
)
from banksys_sy_liujunyan.train import (
    AUC_THRESHOLD,
    RANDOM_SEED,
    build_model,
    evaluate,
    train,
)


def test_feature_columns_order_matches_loader(sample_df):
    # Assert
    expected = [
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
    assert expected == FEATURE_COLUMNS
    assert set(FEATURE_COLUMNS) == set(sample_df.columns) - {"id", TARGET_COLUMN}


def test_preprocessor_transforms(sample_df):
    # Arrange
    pre = build_preprocessor()
    X = sample_df[FEATURE_COLUMNS]

    # Act
    Xt = pre.fit_transform(X)

    # Assert
    assert Xt.shape[0] == len(sample_df)
    assert Xt.shape[1] > len(FEATURE_COLUMNS)  # onehot 后列数应增加


def test_build_model_returns_pipeline_with_preprocess():
    # Act
    model = build_model()

    # Assert
    assert list(model.named_steps) == ["preprocess", "classifier"]
    assert model.named_steps["classifier"].class_weight == "balanced"
    assert model.named_steps["classifier"].random_state == RANDOM_SEED


def test_evaluate_returns_metrics(sample_df):
    # Arrange
    model = build_model()
    X = sample_df[FEATURE_COLUMNS]
    y = sample_df[TARGET_COLUMN]
    model.fit(X, y)

    # Act
    metrics = evaluate(model, X, y)

    # Assert
    assert set(metrics) == {"auc", "f1", "precision", "recall", "threshold"}
    assert 0.0 <= metrics["auc"] <= 1.0
    assert metrics["threshold"] == 0.5


def test_train_saves_model_and_metrics(tmp_path):
    # Arrange
    df = pd.DataFrame(
        {
            "id": [i for i in range(60)],
            "age": [30 + (i % 25) for i in range(60)],
            "job": ["admin." if i % 2 else "services" for i in range(60)],
            "marital": ["married" if i % 2 else "single" for i in range(60)],
            "education": ["high.school" for _ in range(60)],
            "default": ["no" for _ in range(60)],
            "housing": ["yes" if i % 3 else "no" for i in range(60)],
            "loan": ["no" for _ in range(60)],
            "contact": ["cellular" for _ in range(60)],
            "month": ["may" for _ in range(60)],
            "day_of_week": ["mon" for _ in range(60)],
            "duration": [100 + (i * 50) for i in range(60)],
            "campaign": [1] * 60,
            "pdays": [999] * 60,
            "previous": [0] * 60,
            "poutcome": ["nonexistent"] * 60,
            "emp_var_rate": [1.0] * 60,
            "cons_price_index": [93.0] * 60,
            "cons_conf_index": [-40.0] * 60,
            "lending_rate3m": [1.0] * 60,
            "nr_employed": [5000.0] * 60,
            "subscribe": ["yes" if i % 2 else "no" for i in range(60)],
        }
    )
    csv_path = tmp_path / "data.csv"
    df.to_csv(csv_path, index=False)
    model_path = tmp_path / "model.joblib"
    metrics_path = tmp_path / "metrics.json"

    # Act
    result = train(csv_path, model_path, metrics_path)

    # Assert
    assert model_path.exists()
    assert metrics_path.exists()
    assert result.n_train > 0
    assert result.n_val > 0


def test_train_auc_threshold_constant():
    # Assert
    assert AUC_THRESHOLD == 0.80
