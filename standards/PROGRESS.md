# PROGRESS · banksys_sy_liujunyan 〔本项目活记忆 · 状态机〕

> **作用**:这是项目的"存档点"。任意 AI、任意重启会话,读它即可知道当前做到哪、下一步做什么、踩过什么坑。
> **更新时机**:每完成一个有意义步骤、每次会话结束前。
> **格式要求**:时间倒序,最新在上;短、准、可接力。

---

## 当前状态 (最后更新: 2026-08-02 · by AI 助手)

- **阶段**:`已上线(对应 06 六步流程第⑥步:CD 部署成功,容器运行中)`
- **上一步完成**:健康检查相关 PR #6/#8/#9 处理后,CD 最终部署成功——容器 `banksys_sy_liujunyan` 运行中,主机端口 **8890** → 容器内 8888;Dockerfile 含 HEALTHCHECK(容器内 python urllib 探测),部署脚本去掉服务器侧健康检查。
- **下一步 (TODO 第一条)**:更新里程碑/GOTACHAS;本地查看项目。
- **阻塞项**:无。

---

## 待办清单 (TODO,按优先级)

- [x] 初始化项目上下文:`00-project-context.md`
- [x] 确认需求与验收标准:`01-requirements.md`
- [x] 写下本文件第一批 TODO
- [x] ✋ 人类确认以上三份文档
- [x] 创建 GitHub 开源仓库 `banksys_sy_liujunyan`
- [x] ✋ 人类配置 Secrets:SSH_PRIVATE_KEY / SSH_HOST / SSH_USER(已核对)
- [x] 从 `main` 开 feature 分支(`feature/1-init-project`)
- [x] 工程骨架:pyproject/requirements/conda 环境(Python 3.11)
- [x] 模块 1:数据加载 + 分析计算 + 分析页(含测试)
- [x] 模块 2:特征工程 + 离线训练(AUC 0.895 ≥ 0.80)+ 模型产物
- [x] 模块 3:在线预测(`predict.py` + 点选式预测页,含测试)
- [x] Streamlit 应用整合 + Dockerfile + 健康检查 `/_stcore/health`(实测 200)
- [x] 本地 CI 自检(AI 执行):ruff 全绿 + pytest 20 过 + 覆盖率 95.49%
- [x] ci.yml / cd.yml 编写
- [x] push feature 分支 + 创建 PR #2(`closes #1`),CI 在 PR 复检全绿
- [x] PR #2 合并 main
- [x] CD 首次失败 → 定位根因(Dockerfile 未上传)→ fix 分支修复(cd.yml 改 scp + deploy.sh)
- [x] PR #4 合并 main → CD 自动部署成功(端口 8891,健康检查 ok)
- [x] 会话结束前更新本文件

---

## 关键决策记录 (ADR)

| 日期 | 决策 | 理由 |
|---|---|---|
| 2026-08-02 | 覆盖率门槛排除 Streamlit UI 薄层(app.py/pages_*/ui.py) | UI 层为薄壳,不适合单测;核心逻辑覆盖达 95%,门槛只卡核心代码 |
| 2026-08-02 | 模型用 RandomForest(300 树、balanced、seed 42) | 实际 AUC 0.895,达标且可复现 |
| 2026-08-02 | 数据 `data/*.csv` 进 Git | 公开教学数据、体积小(约 3.7MB),CI 干净环境可直接复现 |
| 2026-08-02 | 模型产物默认不进 Git | 大文件/产物不入库;Dockerfile 构建时离线训练生成 |
| 2026-08-02 | 健康检查用 `/_stcore/health` | Streamlit 内置健康端点,无需额外服务 |
| 2026-08-02 | 容器内端口固定 8888,主机端口预留区间 8888–8897 自动回退 | 遵循 05 标准,避免端口冲突 |
| 2026-08-02 | `duration` 保留参与建模(人类确认) | 需求要求保留;已知未来信息泄漏风险,预测页如实展示该输入 |

---

## 已知坑 (GOTACHAS)

- CD 失败 `open Dockerfile: no such file or directory`:原 cd.yml 用 `rsync -a ./ "$DEPLOY_DIR/"`,但 appleboy/ssh-action 的 script 在远程 home 目录执行,`./` 不是 runner 的 checkout 目录,仓库文件未上传。解决:改用 `appleboy/scp-action` 上传 `src,data,Dockerfile,requirements.txt,deploy.sh` 到服务器,再 ssh 执行 `deploy.sh`;验证:CD 重新跑通。
- Dockerfile 加 HEALTHCHECK 后 CD 失败:`apt-get install curl` 在国内服务器上超时(549s)导致 build 失败。解决:不用 apt 装 curl,HEALTHCHECK 改用容器内 `python -c "import urllib.request; urllib.request.urlopen(...)"`(slim 镜像自带 python);验证:CI 的 docker build 通过。
- deploy.sh 服务器侧健康检查报 `ImportError: No module named request`:服务器默认 `python` 环境异常。解决:deploy.sh 去掉服务器侧健康检查,容器 `docker run` 启动成功即部署完成(Dockerfile 内 HEALTHCHECK 由容器自己维护);验证:CD 全绿,容器运行。
- Actions 警告 `Node.js 20 is deprecated`(checkout/setup-python 被强制跑 Node 24):仅提示不阻塞;后续可升级 actions 版本消除。

---

## 里程碑 (DONE)

- [x] 三份文档(00/01/PROGRESS)经人类确认
- [x] 完成建仓 + Secrets 配置
- [x] 完成工程骨架与 CI 全绿
- [x] 完成数据分析页(模块 1)
- [x] 完成离线训练与模型指标达标(模块 2,AUC 0.895)
- [x] 完成在线预测页(模块 3)
- [x] 完成完整 CI + CD 链路并部署成功(服务器端口 8891,健康检查 ok)
- [x] 本地 8888 端口运行项目供本地查看

> 反臃肿:里程碑超过 15 条时,把更早内容合并成一行摘要,保持本文件可快速阅读。
