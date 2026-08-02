"""Streamlit 页面共用辅助:字段清单与中文展示标签。"""

from .data_loader import CATEGORICAL_COLUMNS, NUMERIC_COLUMNS

# 中文字段名,用于 UI 展示
FIELD_LABELS: dict[str, str] = {
    "id": "客户编号",
    "age": "年龄",
    "job": "职业",
    "marital": "婚姻状况",
    "education": "教育程度",
    "default": "是否有信用违约",
    "housing": "是否有房贷",
    "loan": "是否有个人贷款",
    "contact": "联系方式",
    "month": "联系月份",
    "day_of_week": "联系星期",
    "duration": "上次通话时长(秒)",
    "campaign": "本次营销联系次数",
    "pdays": "上次联系间隔天数",
    "previous": "此前联系次数",
    "poutcome": "上次营销结果",
    "emp_var_rate": "就业变化率",
    "cons_price_index": "消费者物价指数",
    "cons_conf_index": "消费者信心指数",
    "lending_rate3m": "3个月贷款利率",
    "nr_employed": "就业人数",
    "subscribe": "是否认购",
}

TARGET_LABELS: dict[str, str] = {"yes": "认购", "no": "未认购"}

FEATURE_COLUMNS = CATEGORICAL_COLUMNS + NUMERIC_COLUMNS


def field_label(column: str) -> str:
    """返回字段的中文标签,未知字段回退为原列名。"""
    return FIELD_LABELS.get(column, column)


def target_label(value: str) -> str:
    """目标取值转中文标签。"""
    return TARGET_LABELS.get(value, value)
