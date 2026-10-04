"""命令行入口。"""

from __future__ import annotations

import sys

from rich.console import Console

from dsh_agent.agent import Agent
from dsh_agent.config import load_settings


def _fix_windows_console_encoding() -> None:
    """让中文在 Windows 控制台正常显示。

    Windows 默认代码页是 GBK(936)，直接 print 中文会变成乱码
    （例如「未配置」显示为「δ����」）。这里强制切到 UTF-8。
    Python 3.7+ 才有 reconfigure，故需兼容旧版本。
    """
    if sys.platform != "win32":
        return
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


_fix_windows_console_encoding()
console = Console()


def main() -> int:
    """解析参数、加载配置、运行 Agent。"""
    try:
        settings = load_settings()
    except RuntimeError as exc:
        console.print(f"[red]配置错误：[/red]{exc}")
        return 1

    prompt = " ".join(sys.argv[1:]).strip() or "你好，请用一句话介绍你自己。"
    console.print(f"[dim]模型：{settings.agent_model}[/dim]")
    console.print(f"[bold cyan]你：[/bold cyan]{prompt}")

    agent = Agent(settings)
    try:
        result = agent.run(prompt)
    except Exception as exc:  # noqa: BLE001 - CLI 边界统一兜底并给出可读提示
        console.print(f"[red]调用失败：[/red]{exc}")
        return 1

    console.print(f"[bold green]Agent：[/bold green]{result.content}")
    console.print(
        f"[dim]tokens: 输入 {result.prompt_tokens} / 输出 {result.completion_tokens}[/dim]"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
