# 00 · 项目上下文 〔本项目活记忆 · AI 维护〕

> **作用**:这是项目的"身份档案"。AI 接管项目时先读这里,了解项目目标、技术栈、目录、部署取值。
> **更新时机**:架构、技术栈、目录结构、端口、部署目录、重要约束变化时更新。
> **填写方式**:把 `<...>` 替换成真实内容;用不到的行删掉。

---

## 1. 项目是什么

- **项目名称**:`banksys_sy_liujunyan`
- **一句话目标**:基于银行营销数据,构建一个 Web 应用,同时提供「数据交互分析」与「是否认购定期存款的在线预测」两类能力。
- **使用者/受益者**:银行营销分析师(看数据找规律)、营销/客服人员(录入客户信息,实时判断营销优先级)。
- **核心功能**:
  - 数据分析交互页面:数据概览、字段分布、目标变量分布、交互筛选与可视化。
  - 在线预测系统:离线训练「是否认购」二分类模型 → 用户在页面上以点选/下拉/数字方式输入 → 实时返回是否认购及概率。
- **输入/数据**:`data/train.csv`(22 500 行)与 `data/test.csv`(7 500 行),目标列 `subscribe`(yes/no)。来源为公开银行营销教学数据集,非敏感、体积小(共约 3.7MB),**进 Git** 供 CI 复现。

## 2. 技术栈

| 层 | 选型 | 理由 |
|---|---|---|
| 语言/运行时 | Python 3.11 | 用户指定 |
| Web/UI 框架 | Streamlit | 用户指定,适合数据应用,一个入口承载分析页 + 预测页 |
| 数据/ML | pandas、scikit-learn、imbalanced-learn | 表格处理与二分类建模;类别不均衡时用 SMOTE |
| 测试 | pytest | 用户指定 |
| 格式/静态检查 | ruff(format + check) | 用户指定 |
| 打包/运行 | Docker(容器名 `banksys_sy_liujunyan`) | 用户指定,便于 CI/CD 部署 |
| CI/CD | GitHub Actions | 通用、可视化、适合教学与团队协作 |

## 3. 目录地图

```text
banksys_sy_liujunyan/
├── standards/                 # AI 项目记忆与通用规范
├── data/                      # train.csv / test.csv(公开教学数据,进 Git)
├── src/banksys_sy_liujunyan/  # 源码包
│   ├── __init__.py
│   ├── app.py                 # Streamlit 入口:分析页 + 预测页
│   ├── data_loader.py         # CSV 加载与基础校验
│   ├── eda.py                 # 概览/分布/相关性的纯计算逻辑
│   ├── features.py            # 特征工程:编码、缩放、pdays 等处理
│   ├── train.py               # 离线训练、评估、保存模型
│   └── predict.py             # 模型加载与推理
├── tests/                     # 单元测试(核心逻辑)
├── models/                    # 模型产物(joblib,默认不进 Git)
├── requirements.txt           # 生产运行依赖
├── requirements-dev.txt       # 本地/CI 检查依赖
├── pyproject.toml             # ruff / pytest 配置
├── Dockerfile
├── .github/workflows/
│   ├── ci.yml
│   └── cd.yml
└── README.md
```

> 新增目录前先更新本节,避免项目越做越散。

## 4. 质量门槛

| 类型 | 本项目标准 |
|---|---|
| 格式检查 | `ruff format --check .` |
| 静态检查 | `ruff check .` |
| 单元测试 | `pytest` |
| 覆盖率 | `pytest --cov --cov-fail-under=80`(核心逻辑 ≥ 80%;Streamlit UI 薄层 app.py/pages_*/ui.py 不计入) |
| 构建 | `docker build` 成功(在 CI/服务器,本地不强制 Docker) |
| 业务/模型指标 | 二分类 **AUC ≥ 0.80**(基线,数据探索后校准);健康检查 `/_stcore/health` 返回 200 |

> 注:`duration`(上次通话时长)字段**保留参与建模**(经人类确认)。已知其存在未来信息泄漏风险,线上预测的意义需在 PROGRESS/ADR 说明;作为决策记录保存。

## 5. 不变约束

- 密钥、密码、私钥、Token **绝不写进代码或文档**,只进 GitHub Secrets / 环境变量。
- **数据进 Git**:`data/train.csv`、`data/test.csv` 为公开教学数据,体积小,进 Git 供 CI 复现。
- **模型产物默认不进 Git**:`models/*.joblib` 由离线训练脚本产出,构建/运行时按需生成与加载。
- `main` 分支受保护,日常开发必须走 feature 分支 + PR。
- CI 红灯不合并。

## 6. 部署/CI 占位符取值

| 占位符 | 本项目取值 | 说明 |
|---|---|---|
| `<APP>` | `banksys_sy_liujunyan` | 应用名/镜像名/容器名 |
| `<DEPLOY_DIR>` | `/opt/banksys_sy_liujunyan` | 服务器部署目录 |
| `<PORT>` | `8888` | 服务端口(容器内固定 8888,主机优先 8888) |
| `<PORT_MAX>` | `8897` | 主机端口回退区间上限(8888–8897) |
| `<PYVER>` | `3.11` | Python 版本 |
| `<HEALTHCHECK>` | `/_stcore/health` | Streamlit 内置健康端点 |
| `<SSH_USER>` | 待部署时配置 | 如 `root` 或 `deploy` |
| `<SSH_HOST>` | 待部署时配置 | 服务器公网 IP 或域名 |
