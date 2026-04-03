"""CLI analytics helpers."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass, field

from app.analytics.events import Event
from app.analytics.provider import Properties, capture


def _string_value(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _mapping_value(mapping: Mapping[str, object], key: str) -> str | None:
    return _string_value(mapping.get(key))


@dataclass(slots=True)
class CommandContext:
    command: str = "opensre"
    properties: Properties = field(default_factory=dict)


_command_context = CommandContext()


def reset_command_context(command: str = "opensre", properties: Properties | None = None) -> None:
    global _command_context  # noqa: PLW0603
    _command_context = CommandContext(command=command, properties=dict(properties or {}))


def set_command_context(command: str, properties: Properties | None = None) -> None:
    reset_command_context(command, properties)


def update_command_context(properties: Properties) -> None:
    _command_context.properties.update(properties)


def current_command_context() -> CommandContext:
    return CommandContext(command=_command_context.command, properties=dict(_command_context.properties))


def onboard_properties(config: Mapping[str, object]) -> Properties:
    properties: Properties = {}

    wizard_obj = config.get("wizard")
    if isinstance(wizard_obj, Mapping):
        wizard_mode = _mapping_value(wizard_obj, "mode")
        configured_target = _mapping_value(wizard_obj, "configured_target")
        if wizard_mode is not None:
            properties["wizard_mode"] = wizard_mode
        if configured_target is not None:
            properties["configured_target"] = configured_target

    targets_obj = config.get("targets")
    if isinstance(targets_obj, Mapping):
        local_obj = targets_obj.get("local")
        if isinstance(local_obj, Mapping):
            provider = _mapping_value(local_obj, "provider")
            model = _mapping_value(local_obj, "model")
            if provider is not None:
                properties["provider"] = provider
            if model is not None:
                properties["model"] = model

    return properties


def investigation_properties(
    *,
    input_path: str | None,
    input_json: str | None,
    interactive: bool,
    print_template: str | None,
    output: str | None,
) -> Properties:
    properties: Properties = {
        "has_input_file": input_path is not None,
        "has_inline_json": input_json is not None,
        "interactive": interactive,
        "print_template": print_template is not None,
        "has_output_file": output is not None,
    }
    llm_provider = _string_value(os.getenv("LLM_PROVIDER"))
    llm_model = _string_value(os.getenv("ANTHROPIC_MODEL")) or _string_value(os.getenv("OPENAI_MODEL"))
    if llm_provider is not None:
        properties["llm_provider"] = llm_provider
    if llm_model is not None:
        properties["llm_model"] = llm_model
    return properties


def capture_command_completed(
    *,
    command: str,
    exit_code: int,
    duration_ms: int,
    properties: Properties | None = None,
) -> None:
    capture(
        Event.COMMAND_COMPLETED,
        {
            "command": command,
            "exit_code": exit_code,
            "success": exit_code == 0,
            "duration_ms": duration_ms,
            **(properties or {}),
        },
    )
