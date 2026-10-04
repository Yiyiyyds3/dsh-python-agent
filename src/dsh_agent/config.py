"""配置加载：统一从环境变量 / .env 读取，避免密钥散落在代码里。

用 pydantic-settings 的好处：类型不对、缺必填项时会在启动瞬间报错，
而不是等你跑到第 100 行调用 API 时才崩。
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Agent 运行配置。字段名大小写不敏感，对应 .env 中的大写变量。"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- 大模型 ---
    openai_api_key: str = Field(default="", description="大模型 API 密钥")
    openai_base_url: str = Field(default="https://api.openai.com/v1")

    # --- Agent 行为 ---
    agent_model: str = Field(default="gpt-4o-mini")
    agent_temperature: float = Field(default=0.0, ge=0.0, le=2.0)
    agent_max_tokens: int = Field(default=2048, gt=0)
    agent_max_iterations: int = Field(
        default=10,
        gt=0,
        description="最大推理轮数上限，防止 Agent 陷入死循环持续消耗 token",
    )

    log_level: str = Field(default="INFO")


def load_settings() -> Settings:
    """加载配置。缺失必填项时抛出清晰的错误提示。"""
    settings = Settings()
    if not settings.openai_api_key:
        raise RuntimeError(
            "未配置 OPENAI_API_KEY。\n"
            "请执行：copy .env.example .env\n"
            "然后在 .env 中填入你的真实密钥。"
        )
    return settings
