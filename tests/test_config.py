"""测试：验证配置加载逻辑。

注意这里不联网、不消耗 token —— 好的测试应该快且确定。
"""

from __future__ import annotations

import pytest

from dsh_agent.config import Settings, load_settings


def test_defaults() -> None:
    settings = Settings()
    assert settings.agent_model == "gpt-4o-mini"
    # 默认温度为 0，保证输出可复现，便于写断言
    assert settings.agent_temperature == 0.0


def test_missing_api_key_raises_clear_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(Settings, "model_config", {**Settings.model_config, "env_file": None})

    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        load_settings()
