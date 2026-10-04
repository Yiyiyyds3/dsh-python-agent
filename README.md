# dsh-python-agent

> 一个用 Python 从零实现的 LLM Agent 项目。

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 这是什么

<!-- ⚠️ 把这段话换成你自己的项目一句话说明。面试官只会看这里的前两行。 -->
用 Python 实现的一个 LLM Agent：能理解用户意图、调用工具、多轮推理并返回结果。

**核心特性**

- [ ] 工具调用（Function Calling）
- [ ] 多轮对话与上下文管理
- [ ] 失败重试与超时控制
- [ ] 可观测的调用日志

## 快速开始

前置要求：[uv](https://docs.astral.sh/uv/)（本项目用 uv 管理依赖，比 pip 快且能锁定版本）

```bash
# 1. 获取代码
git clone https://github.com/Yiyiyyds3/dsh-python-agent.git
cd dsh-python-agent

# 2. 安装依赖（自动创建虚拟环境并写入 uv.lock）
uv sync

# 3. 配置密钥
cp .env.example .env        # Windows: copy .env.example .env
# 然后编辑 .env，填入你的 API Key

# 4. 运行
uv run dsh-agent
```

> **依赖必须声明在 `pyproject.toml`，不要手动 `pip install`。**
> 这样别人 `uv sync` 一次就能跑起来，而不是看你 README 里列一堆安装命令。

## 环境变量

全部配置见 [`.env.example`](.env.example)。**`.env` 绝不会被提交**（已加入 `.gitignore`，且有 pre-commit 钩子二次拦截）。

| 变量 | 说明 | 必填 |
|---|---|---|
| `OPENAI_API_KEY` | 大模型 API 密钥 | 是 |
| `AGENT_MODEL` | 使用的模型名 | 否 |
| `AGENT_MAX_ITERATIONS` | Agent 最大推理轮数，防止死循环烧钱 | 否 |

## 项目结构

```text
.
├── src/dsh_agent/          # 源码（src 布局，避免测试时导入错包）
│   ├── __init__.py
│   ├── cli.py              # 命令行入口
│   ├── config.py           # 配置加载（pydantic-settings + .env）
│   └── agent.py            # Agent 核心逻辑
├── tests/                  # 测试
│   └── fixtures/           # 测试夹具（*.jsonl 在此目录会被入库）
├── data/                   # 数据集 / 知识库（未被忽略的 jsonl 会入库）
├── .githooks/pre-commit    # 密钥拦截钩子
├── .env.example            # 环境变量模板
└── pyproject.toml          # 依赖 + ruff + mypy + pytest 配置
```

## 开发

```bash
uv run pytest            # 跑测试
uv run ruff check .      # 代码检查
uv run ruff format .     # 代码格式化
uv run mypy src          # 类型检查
```

### 首次克隆后必须做一次

```bash
git config core.hooksPath .githooks
```

这行启用密钥拦截钩子。`core.hooksPath` 是本地配置、不会被提交，所以每个克隆者都要执行一次。

## 许可证

MIT
