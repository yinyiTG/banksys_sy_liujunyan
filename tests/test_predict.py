"""在线预测模块的单元测试。"""

import pandas as pd
import pytest

from banksys_sy_liujunyan.predict import load_model, predict_one


@pytest.fixture
def trained_model(tmp_path):
    """用小型数据集训练一个可用模型,返回 (model, 一行合法输入)。"""
    from banksys_sy_liujunyan.train import train

    n = 120
    df = pd.DataFrame(
        {
            "id": list(range(n)),
            "age": [30 + (i % 30) for i in range(n)],
            "job": ["admin." if i % 2 else "services" for i in range(n)],
            "marital": ["married" if i % 2 else "single" for i in range(n)],
            "education": ["high.school"] * n,
            "default": ["no"] * n,
            "housing": ["yes" if i % 3 else "no" for i in range(n)],
            "loan": ["no"] * n,
            "contact": ["cellular"] * n,
            "month": ["may"] * n,
            "day_of_week": ["mon"] * n,
            "duration": [100 + (i * 50) for i in range(n)],
            "campaign": [1] * n,
            "pdays": [999] * n,
            "previous": [0] * n,
            "poutcome": ["nonexistent"] * n,
            "emp_var_rate": [1.0] * n,
            "cons_price_index": [93.0] * n,
            "cons_conf_index": [-40.0] * n,
            "lending_rate3m": [1.0] * n,
            "nr_employed": [5000.0] * n,
            "subscribe": ["yes" if i % 2 else "no" for i in range(n)],
        }
    )
    csv_path = tmp_path / "data.csv"
    model_path = tmp_path / "model.joblib"
    metrics_path = tmp_path / "metrics.json"
    df.to_csv(csv_path, index=False)
    train(csv_path, model_path, metrics_path)
    return load_model(str(model_path)), df


def test_predict_one_returns_label_and_probability(trained_model):
    model, df = trained_model
    row = df.iloc[0].to_dict()
    row.pop("id")

    # Act
    result = predict_one(model, row)

    # Assert
    assert set(result) == {"subscribe", "probability"}
    assert result["subscribe"] in {"yes", "no"}
    assert 0.0 <= result["probability"] <= 1.0


def test_predict_one_missing_field_raises(trained_model):
    model, df = trained_model
    row = df.iloc[0].to_dict()
    row.pop("id")
    del row["age"]

    # Act / Assert
    with pytest.raises(ValueError, match="缺少字段"):
        predict_one(model, row)


def test_predict_one_deterministic(trained_model):
    model, df = trained_model
    row = df.iloc[0].to_dict()
    row.pop("id")

    # Act
    first = predict_one(model, row)
    second = predict_one(model, row)

    # Assert
    assert first == second


def test_predict_one_numeric_fields_are_numbers(trained_model):
    model, df = trained_model
    row = df.iloc[0].to_dict()
    row.pop("id")

    # Act
    result = predict_one(model, row)

    # Assert
    assert isinstance(result["probability"], float)
