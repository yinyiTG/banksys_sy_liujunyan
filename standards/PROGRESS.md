# PROGRESS · banksys_sy_liujunyan 〔本项目活记忆 · 状态机〕

> **作用**:这是项目的"存档点"。任意 AI、任意重启会话,读它即可知道当前做到哪、下一步做什么、踩过什么坑。
> **更新时机**:每完成一个有意义步骤、每次会话结束前。
> **格式要求**:时间倒序,最新在上;短、准、可接力。

---

## 当前状态 (最后更新: 2026-08-02 · by AI 助手)

- **阶段**:`初始化(对应 06 六步流程第①步之前)`
- **上一步完成**:读取 `standards/` 全部规范与数据;填写 `00-project-context.md`、`01-requirements.md`、本文件第一批 TODO。
- **下一步 (TODO 第一条)**:人类确认三份文档 → 创建 GitHub 开源仓库 `banksys_sy_liujunyan`。
- **阻塞项**:无。文档确认后,建仓完成即需人类配置 Secrets(SSH_PRIVATE_KEY / SSH_HOST / SSH_USER),否则 CD 必失败。

---

## 待办清单 (TODO,按优先级)

- [x] 初始化项目上下文:`00-project-context.md`
- [x] 确认需求与验收标准:`01-requirements.md`
- [x] 写下本文件第一批 TODO
- [ ] ✋ 人类确认以上三份文档
- [ ] 创建 GitHub 开源仓库 `banksys_sy_liujunyan`(main 只放 .gitignore / 占位 README)
- [ ] ✋ 提示人类配置 Secrets:SSH_PRIVATE_KEY / SSH_HOST / SSH_USER(新仓库默认为空)
- [ ] 从 `main` 开 feature 分支(如 `feature/1-init-project`),严禁直接改 main
- [ ] 工程骨架:源码包目录、`requirements.txt` / `requirements-dev.txt`、`pyproject.toml`(ruff+pytest 配置)、`.gitignore`
- [ ] 模块 1:数据加载(`data_loader.py`)+ 分析计算(`eda.py`)+ 分析页(含测试)
- [ ] 模块 2:特征工程(`features.py`)+ 离线训练与评估(`train.py`,含指标门槛与可复现种子)+ 模型产物
- [ ] 模块 3:在线预测(`predict.py`)+ 预测页(点选式输入)(含测试)
- [ ] Streamlit 应用整合 + `Dockerfile` + 健康检查 `/_stcore/health`
- [ ] 本地 CI 自检(AI 执行):`ruff format --check .` + `ruff check .` + `pytest --cov --cov-fail-under=80`
- [ ] `.github/workflows/ci.yml`(格式/lint/测试/覆盖率/docker build)
- [ ] push feature 分支 + 创建 PR(`closes #<issue>`),CI 在 PR 复检
- [ ] ✋ 人工 Review → 人类合并 main(合并是人类的动作,AI 绝不自行合并)
- [ ] `.github/workflows/cd.yml`:SSH 部署 + 健康检查,验证端口 8888 与访问地址
- [ ] 会话结束前更新本文件

---

## 关键决策记录 (ADR)

| 日期 | 决策 | 理由 |
|---|---|---|
| 2026-08-02 | 数据 `data/*.csv` 进 Git | 公开教学数据、体积小(约 3.7MB),CI 干净环境可直接复现 |
| 2026-08-02 | 模型产物默认不进 Git | 大文件/产物不入库;由训练脚本产出,构建/运行时按需生成加载 |
| 2026-08-02 | 健康检查用 `/_stcore/health` | Streamlit 内置健康端点,无需额外服务 |
| 2026-08-02 | 容器内端口固定 8888,主机端口预留区间 8888–8897 自动回退 | 遵循 05 标准,避免端口冲突 |
| 2026-08-02 | `duration` 保留参与建模(人类确认) | 需求要求保留;已知未来信息泄漏风险,预测页如实展示该输入 |

---

## 已知坑 (GOTACHAS)

- <现象>:<根因>;解决:<怎么处理>;验证:<如何确认已修复>。
  - 待遇到真实故障后按 06「故障反哺铁律」填写。

---

## 里程碑 (DONE)

- [ ] 三份文档(00/01/PROGRESS)经人类确认
- [ ] 完成建仓 + Secrets 配置
- [ ] 完成工程骨架与 CI 全绿
- [ ] 完成数据分析页(模块 1)
- [ ] 完成离线训练与模型指标达标(模块 2)
- [ ] 完成在线预测页(模块 3)
- [ ] 完成完整 CI + CD 链路并部署成功

> 反臃肿:里程碑超过 15 条时,把更早内容合并成一行摘要,保持本文件可快速阅读。
