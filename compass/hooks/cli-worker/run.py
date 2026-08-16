#!/usr/bin/env python3
# compass:generated hook=cli-worker
"""Hand a planner's pending tool call to the Claude Code CLI."""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any

COMPASS_CONTEXT_REL = Path(".compass") / "context" / "cli-worker.md"
LOCK_REL = Path(".compass") / "context" / "L4-session" / "cli-worker.lock"
DEFAULT_TIMEOUT = 600
MAX_PROMPT_CHARS = 200_000
DANGEROUS_FLAGS = {
    "--dangerously-skip-permissions",
    "--dangerously-bypass-hook-trust",
}
CLAUDE_CLI_RE = re.compile(r"^\s*(?:command\s+-v\s+)?claude(?:\s|$)")
READONLY_GIT_RE = re.compile(
    r"^\s*git\s+(status|diff|log|show|rev-parse|ls-files|blame|grep|describe|symbolic-ref)\b"
)
TEST_HINT_RE = re.compile(
    r"\b(pytest|npm\s+test|pnpm\s+test|yarn\s+test|cargo\s+test|go\s+test|"
    r"python\s+-m\s+pytest|vitest|jest|make\s+test|ctest)\b",
    re.I,
)
MUTATING_SHELL_RE = re.compile(
    r"(>>?|tee\s+|sed\s+-i|perl\s+-i|ruby\s+-i|rm\s+|mv\s+|cp\s+|mkdir\s+|touch\s+|"
    r"truncate\s+|install\s+|chmod\s+|chown\s+|ln\s+|rsync\s+|patch\s+|"
    r"python3?\s+-c\s+|node\s+-e\s+)",
    re.I,
)
WRITE_TOOLS = {
    "write",
    "edit",
    "strreplace",
    "apply_patch",
    "applypatch",
    "searchreplace",
    "notebookedit",
    "delete",
    "tabwrite",
}
SHELL_TOOLS = {"shell", "bash", "powershell", "command"}


def emit(payload: dict[str, Any], *, code: int = 0) -> int:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False))
    sys.stdout.write("\n")
    return code


def allow(fmt: str, extra: str | None = None) -> int:
    if fmt == "cursor":
        body: dict[str, Any] = {"permission": "allow"}
        if extra:
            body["agent_message"] = extra
        return emit(body)
    if fmt == "codex":
        body = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
            }
        }
        if extra:
            body["hookSpecificOutput"]["additionalContext"] = extra
        return emit(body)
    body = {"action": "allow"}
    if extra:
        body["reason"] = extra
    return emit(body)


def deny(fmt: str, reason: str) -> int:
    if fmt == "cursor":
        return emit(
            {
                "permission": "deny",
                "agent_message": reason,
                "user_message": reason,
            }
        )
    if fmt == "codex":
        return emit(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }
        )
    return emit({"action": "deny", "reason": reason})


def find_project_root(start: Path) -> Path | None:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / COMPASS_CONTEXT_REL).is_file():
            return candidate
    return None


def parse_worker_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip().lower()
        if key in {"status", "reason", "cli", "invoke", "checked-at", "timeout-seconds"}:
            values[key] = value.strip()
    return values


def load_payload() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def tool_name(data: dict[str, Any]) -> str:
    for key in ("tool_name", "toolName", "tool", "name"):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    nested = data.get("tool_input")
    if isinstance(nested, dict):
        inner = nested.get("tool")
        if isinstance(inner, str):
            return inner.strip()
    return ""


def tool_input(data: dict[str, Any]) -> dict[str, Any]:
    for key in ("tool_input", "toolInput", "arguments", "args", "input"):
        value = data.get(key)
        if isinstance(value, dict):
            return value
        if isinstance(value, str):
            return {"command": value}
    return data


def collect_paths(inp: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    for key in (
        "path",
        "file_path",
        "filePath",
        "file",
        "target_file",
        "targetFile",
        "uri",
    ):
        value = inp.get(key)
        if isinstance(value, str) and value.strip():
            paths.append(value.strip())
    command = inp.get("command")
    if isinstance(command, str) and "apply_patch" in command:
        for match in re.finditer(r"(?m)^\+\+\+ [ab]/(.+)$", command):
            paths.append(match.group(1).strip())
        for match in re.finditer(r"(?m)^\*\*\* (?:Update|Add|Delete) File: (.+)$", command):
            paths.append(match.group(1).strip())
    return paths


def normalize_rel(project_root: Path, raw: str) -> str:
    path = Path(raw)
    if not path.is_absolute():
        path = (project_root / path).resolve()
    else:
        path = path.resolve()
    try:
        rel = path.relative_to(project_root)
    except ValueError:
        return raw.replace("\\", "/")
    return rel.as_posix()


def is_planner_owned_path(rel: str) -> bool:
    posix = rel.replace("\\", "/")
    return posix == ".compass/context" or posix.startswith(".compass/context/")


def is_write_tool(name: str) -> bool:
    compact = re.sub(r"[^a-z]", "", name.lower())
    return compact in WRITE_TOOLS or name.lower() in WRITE_TOOLS


def is_shell_tool(name: str) -> bool:
    return name.lower() in SHELL_TOOLS or re.sub(r"[^a-z]", "", name.lower()) in SHELL_TOOLS


def shell_command(inp: dict[str, Any]) -> str:
    for key in ("command", "cmd", "script"):
        value = inp.get(key)
        if isinstance(value, str):
            return value
    return ""


def should_block_shell(command: str) -> bool:
    if not command.strip():
        return False
    if CLAUDE_CLI_RE.search(command):
        return False
    if READONLY_GIT_RE.search(command):
        return False
    if TEST_HINT_RE.search(command):
        return False
    return bool(MUTATING_SHELL_RE.search(command))


def should_hand_off(project_root: Path, name: str, inp: dict[str, Any]) -> bool:
    if is_write_tool(name):
        rels = [normalize_rel(project_root, item) for item in collect_paths(inp)]
        return not (rels and all(is_planner_owned_path(rel) for rel in rels))
    if is_shell_tool(name) or shell_command(inp):
        return should_block_shell(shell_command(inp))
    return False


def worker_timeout(worker: dict[str, str]) -> int:
    raw = worker.get("timeout-seconds") or str(DEFAULT_TIMEOUT)
    try:
        value = int(raw)
    except ValueError:
        return DEFAULT_TIMEOUT
    return max(30, min(value, 3600))


def build_prompt(name: str, inp: dict[str, Any]) -> str:
    body = json.dumps({"tool": name, "input": inp}, ensure_ascii=False, indent=2)
    if len(body) > MAX_PROMPT_CHARS:
        body = body[:MAX_PROMPT_CHARS] + "\n...[truncated]"
    return (
        "A planner agent was about to perform the following tool call. "
        "Do that same action in this project now.\n"
        "Read `.compass/context/` for relevant L2/L3 constraints when needed.\n"
        "Do not commit or push. Do not invoke claude again.\n\n"
        "Pending action:\n"
        f"{body}\n"
    )


def cli_argv(worker: dict[str, str], prompt: str) -> list[str]:
    raw = worker.get("invoke") or "claude -p --permission-mode acceptEdits"
    if raw in {"", "none"}:
        raw = "claude -p --permission-mode acceptEdits"
    parts = [part for part in shlex.split(raw) if part not in DANGEROUS_FLAGS]
    if not parts:
        parts = ["claude", "-p"]
    if "-p" not in parts and "--print" not in parts:
        parts.extend(["-p", prompt])
    else:
        parts.append(prompt)
    return parts


def invoke_cli(project_root: Path, worker: dict[str, str], prompt: str) -> tuple[int, str]:
    if os.environ.get("COMPASS_CLI_WORKER_STUB") == "1":
        return 0, "stubbed CLI worker"
    argv = cli_argv(worker, prompt)
    timeout = worker_timeout(worker)
    result = subprocess.run(
        argv,
        cwd=str(project_root),
        input="",
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    output = ((result.stdout or "") + (result.stderr or "")).strip()
    if len(output) > 4000:
        output = output[-4000:]
    return result.returncode, output


class ExclusiveLock:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.handle = None

    def __enter__(self) -> "ExclusiveLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.handle = open(self.path, "a+", encoding="utf-8")
        try:
            import fcntl

            fcntl.flock(self.handle.fileno(), fcntl.LOCK_EX)
        except ImportError:
            pass
        return self

    def __exit__(self, *args: object) -> None:
        if self.handle is None:
            return
        try:
            import fcntl

            fcntl.flock(self.handle.fileno(), fcntl.LOCK_UN)
        except ImportError:
            pass
        self.handle.close()
        self.handle = None


def hand_off_result(code: int, output: str) -> str:
    tail = f"\n\nCLI output:\n{output}" if output else ""
    if code == 0:
        return (
            "CLI worker already performed this pending action (exit 0). "
            "Do not retry this tool call. Inspect the diff, then continue "
            "review, doc-sync, and closeout only. Do not commit or push "
            f"unless the user explicitly asked.{tail}"
        )
    return (
        f"CLI worker failed (exit {code}) while performing the pending action. "
        "This is a blocker. Do not silently implement it locally. "
        f"Do not commit or push.{tail}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--format", default="internal")
    args, _ = parser.parse_known_args()
    fmt = args.format if args.format in {"cursor", "codex", "internal"} else "internal"

    try:
        project_root = find_project_root(Path.cwd())
        if project_root is None:
            return allow(fmt)

        worker = parse_worker_file(project_root / COMPASS_CONTEXT_REL)
        if worker.get("status", "unknown") != "enabled":
            return allow(fmt)

        data = load_payload()
        name = tool_name(data)
        inp = tool_input(data)
        if not should_hand_off(project_root, name, inp):
            return allow(fmt)
    except Exception:
        return allow(fmt)

    try:
        prompt = build_prompt(name, inp)
        with ExclusiveLock(project_root / LOCK_REL):
            code, output = invoke_cli(project_root, worker, prompt)
        return deny(fmt, hand_off_result(code, output))
    except subprocess.TimeoutExpired:
        return deny(
            fmt,
            "CLI worker timed out while performing the pending action. "
            "This is a blocker. Do not silently implement it locally.",
        )
    except Exception as exc:
        return deny(
            fmt,
            f"CLI worker failed to start: {exc}. "
            "This is a blocker. Do not silently implement it locally.",
        )


if __name__ == "__main__":
    os.environ.setdefault("PYTHONUTF8", "1")
    raise SystemExit(main())
