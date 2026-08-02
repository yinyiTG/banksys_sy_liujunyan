"""data_loader 与 eda 的单元测试。"""

import pandas as pd
import pytest

from banksys_sy_liujunyan.data_loader import TARGET_COLUMN, load_data
from banksys_sy_liujunyan.eda import (
    column_distribution,
    filter_dataframe,
    numeric_summary,
    overview,
    target_distribution,
)


def test_load_data_loads_csv(tmp_path):
    # Arrange
    path = tmp_path / "train.csv"
    pd.DataFrame(
        {
            "id": [1, 2],
            "age": [40, 35],
            "job": ["admin.", "admin."],
            "marital": ["married", "single"],
            "education": ["high.school", "high.school"],
            "default": ["no", "no"],
            "housing": ["yes", "yes"],
            "loan": ["no", "no"],
            "contact": ["cellular", "cellular"],
            "month": ["may", "may"],
            "day_of_week": ["mon", "mon"],
            "duration": [100, 200],
            "campaign": [1, 1],
            "pdays": [10, 10],
            "previous": [0, 0],
            "poutcome": ["nonexistent", "nonexistent"],
            "emp_var_rate": [1.1, 1.1],
            "cons_price_index": [93.0, 93.0],
            "cons_conf_index": [-40.0, -40.0],
            "lending_rate3m": [1.0, 1.0],
            "nr_employed": [5000.0, 5000.0],
            "subscribe": ["no", "yes"],
        }
    ).to_csv(path, index=False)

    # Act
    df = load_data(str(path))

    # Assert
    assert df.shape == (2, 22)
    assert set(df[TARGET_COLUMN].unique()) == {"yes", "no"}


def test_load_data_missing_column_raises(tmp_path):
    # Arrange
    path = tmp_path / "bad.csv"
    pd.DataFrame({"id": [1]}).to_csv(path, index=False)

    # Act / Assert
    with pytest.raises(ValueError, match="缺少必要列"):
        load_data(str(path))


def test_load_data_invalid_target_raises(tmp_path):
    # Arrange
    path = tmp_path / "bad_target.csv"
    pd.DataFrame(
        {
            "id": [1, 2],
            "age": [40, 35],
            "job": ["admin.", "admin."],
            "marital": ["married", "single"],
            "education": ["high.school", "high.school"],
            "default": ["no", "no"],
            "housing": ["yes", "yes"],
            "loan": ["no", "no"],
            "contact": ["cellular", "cellular"],
            "month": ["may", "may"],
            "day_of_week": ["mon", "mon"],
            "duration": [100, 200],
            "campaign": [1, 1],
            "pdays": [10, 10],
            "previous": [0, 0],
            "poutcome": ["nonexistent", "nonexistent"],
            "emp_var_rate": [1.1, 1.1],
            "cons_price_index": [93.0, 93.0],
            "cons_conf_index": [-40.0, -40.0],
            "lending_rate3m": [1.0, 1.0],
            "nr_employed": [5000.0, 5000.0],
            "subscribe": ["x", "y"],
        }
    ).to_csv(path, index=False)

    # Act / Assert
    with pytest.raises(ValueError, match="目标列"):
        load_data(str(path))


def test_overview_reports_columns(sample_df):
    # Act
    result = overview(sample_df)

    # Assert
    assert list(result.columns) == ["字段", "类型", "缺失数", "唯一值数"]
    assert len(result) == sample_df.shape[1]
    assert (result["缺失数"] == 0).all()
    assert result.loc[result["字段"] == TARGET_COLUMN, "唯一值数"].iloc[0] == 2


def test_target_distribution(sample_df):
    # Act
    result = target_distribution(sample_df)

    # Assert
    assert set(result.index) == {"yes", "no"}
    assert result.loc["no", "数量"] == 3
    assert result.loc["yes", "数量"] == 2
    assert result["占比"].sum() == pytest.approx(1.0)


def test_column_distribution(sample_df):
    # Act
    result = column_distribution(sample_df, "job")

    # Assert
    assert result.loc["admin.", "数量"] == 2
    assert result["占比"].sum() == pytest.approx(1.0)


def test_numeric_summary(sample_df):
    # Act
    result = numeric_summary(sample_df, "age")

    # Assert
    assert result["min"] == 26
    assert result["max"] == 51
    assert result["mean"] == pytest.approx(44.0)


def test_filter_categorical(sample_df):
    # Act
    result = filter_dataframe(sample_df, {"job": "admin."})

    # Assert
    assert len(result) == 2
    assert (result["job"] == "admin.").all()


def test_filter_numeric_range(sample_df):
    # Act
    result = filter_dataframe(sample_df, {"age_min": 30, "age_max": 50})

    # Assert
    assert len(result) == 3
    assert result["age"].between(30, 50).all()


def test_filter_no_op(sample_df):
    # Act
    result = filter_dataframe(sample_df, {})

    # Assert
    assert len(result) == len(sample_df)
