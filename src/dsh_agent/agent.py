"""Agent 核心逻辑（骨架）。

当前只是一个能跑通的最小循环，用来验证工程链路：
配置加载 -> 调用大模型 -> 返回结果 -> 可测试。

后续你要做的是在这里加：
1. 工具定义与 Function Calling
2. 多轮上下文管理（注意 token 上限，长对话必须做裁剪或摘要）
3. 失败重试与超时（可参考 tenacity）
"""

from __future__ import annotations

from dataclasses import dataclass

from openai import OpenAI

from dsh_agent.config import Settings


@dataclass
class AgentResponse:
    """一次 Agent 调用的结果。"""

    content: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0


class Agent:
    """最小可用的 LLM Agent。

    设计上把 client 作为可注入依赖，这样写测试时能塞假 client，
    不必真的联网烧 token —— 这是让项目「可测试」的关键一步。
    """

    def __init__(self, settings: Settings, client: OpenAI | None = None) -> None:
        self.settings = settings
        self._client = client or OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
        )

    def run(self, user_input: str) -> AgentResponse:
        """处理一轮用户输入并返回结果。"""
        completion = self._client.chat.completions.create(
            model=self.settings.agent_model,
            temperature=self.settings.agent_temperature,
            max_tokens=self.settings.agent_max_tokens,
            messages=[{"role": "user", "content": user_input}],
        )

        choice = completion.choices[0]
        usage = completion.usage
        return AgentResponse(
            content=choice.message.content or "",
            model=completion.model,
            prompt_tokens=usage.prompt_tokens if usage else 0,
            completion_tokens=usage.completion_tokens if usage else 0,
        )
