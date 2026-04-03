from __future__ import annotations

from typing import cast
from unittest.mock import patch

from app.cli.__main__ import main


def test_main_emits_command_completed_for_health(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_capture_command_completed(
        *,
        command: str,
        exit_code: int,
        duration_ms: int,
        properties: dict[str, object] | None = None,
    ) -> None:
        captured["command"] = command
        captured["exit_code"] = exit_code
        captured["duration_ms"] = duration_ms
        captured["properties"] = properties or {}

    monkeypatch.setattr("app.cli.__main__.capture_first_run_if_needed", lambda: None)
    monkeypatch.setattr("app.cli.__main__.capture_command_completed", fake_capture_command_completed)

    with patch("app.integrations.verify.verify_integrations") as mock_verify, patch(
        "app.integrations.verify.format_verification_results"
    ) as mock_format:
        mock_verify.return_value = [
            {
                "service": "aws",
                "source": "local store",
                "status": "passed",
                "detail": "ok",
            }
        ]
        mock_format.return_value = (
            "\n"
            "  SERVICE    SOURCE       STATUS      DETAIL\n"
            "  aws        local store  passed      ok\n"
        )

        exit_code = main(["health"])

    assert exit_code == 0
    assert captured["command"] == "health"
    assert captured["exit_code"] == 0
    assert cast(int, captured["duration_ms"]) >= 0
    assert captured["properties"] == {}
