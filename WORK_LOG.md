# WORK_LOG

## 项目概述

- **目的**：智能营销 Agent（Intelligent Marketing Agent），当前处于起步阶段，仅搭建了基础目录结构。
- **技术栈**：Python（`.venv` 虚拟环境，依赖见 `requirements.txt`），配置走 `.env`。
- **当前文件**：
  - `common/path_utils.py` — 路径工具：以项目根目录为基准，把相对路径拼成绝对路径。
  - `.env` — 环境变量配置。
  - `requirements.txt` — 依赖清单。

## 2026-10-25

- 初始化 `WORK_LOG.md`，记录项目现状 — 按全局规范首次进入项目时建立工作日志。
- 说明 `common/path_utils.py` 的作用：`root_dir` 从 `common/` 上跳两级得到项目根目录，供 `get_file_path()` 统一拼接路径 — 纯解释，未改动代码。
- 定位 `python common/config.py` 报 `ModuleNotFoundError: No module named 'common'` 的原因：直接运行时 `sys.path[0]` 是 `common/` 而非项目根目录 — 约定本项目包内模块一律在项目根目录用 `python -m common.xxx` 运行，不改代码、不加 sys.path hack。
- 新增 `.vscode/launch.json`：以 `${file}` 为入口、`cwd` 和 `PYTHONPATH` 都指向项目根、解释器固定为 `.venv` — 让 IDE 的 ▶/F5 无需 `-m` 也能正常导入 `common` 包，且对任意包内文件通用。
- 新增 `.vscode/settings.json`：固定默认解释器、`python.analysis.extraPaths` 消除 Pylance 报红、`terminal.integrated.env.windows` 注入 PYTHONPATH — 让 ▶ 按钮（不读 launch.json）也能正常导入 `common`；已实测可越过 import 阶段。
- 曾出现 `llm.py` 调用模型 401 invalid_api_key（与运行方式无关，项目根 `-m` 运行同样报错）；用户更新 `.env` 后已恢复，后续 `test.py` 实测可正常调用。
- 修复节点文件导入名错误：目录最终改名为 `__001__langgraph_workflow`，与 import 名一致 — 已实测 import 成功。
- 修复 `test.py` 的 `create_agent` 调用：当前安装的是 `langchain 1.4.7`，新 API 第一个参数是 `model` 而非 `llm`，且没有 `verbose` 参数；`agent.invoke` 的入参必须是 `{"messages": [...]}` 而非裸字符串 — 已实测可生成回复。

