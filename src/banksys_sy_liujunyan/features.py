"""特征工程:类别编码 + 数值缩放,训练/预测共用同一套 pipeline。"""

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .data_loader import CATEGORICAL_COLUMNS, NUMERIC_COLUMNS

# 预测输入的字段顺序(与训练一致)
FEATURE_COLUMNS = CATEGORICAL_COLUMNS + NUMERIC_COLUMNS

# pdays=999 表示该客户此前从未被联系(经典营销数据集约定)
PDAYS_NEVER_CONTACTED = 999


def build_preprocessor() -> ColumnTransformer:
    """返回类别/数值两路的预处理转换器。

    - 类别:缺失填充 + OneHot(handle_unknown='ignore')。
    - 数值:缺失填充 + 标准化。
    """
    categorical_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    numeric_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("cat", categorical_pipe, CATEGORICAL_COLUMNS),
            ("num", numeric_pipe, NUMERIC_COLUMNS),
        ]
    )
