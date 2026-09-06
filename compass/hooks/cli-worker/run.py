#!/usr/bin/env python3
# compass:generated hook=cli-worker
"""Delegate one bounded implementation task to a fresh Claude Code CLI session."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

COMPASS_CONTEXT_REL = Path(".compass") / "context" / "cli-worker.md"
LOCK_REL = Path(".compass") / "context" / "cli-worker.lock"
AUDIT_REL = Path(".compass") / "context" / "cli-worker-audit.jsonl"
TASK_REL = Path(".compass") / "context" / "cli-worker-task.md"
STATE_REL = Path(".compass") / "context" / "cli-worker-state.json"
DEFAULT_TIMEOUT = 600
DEFAULT_MAX_TURNS = 30
MAX_TASK_CHARS = 40_000
MAX_SUCCESS_HISTORY = 100
ALLOWED_MODELS = frozenset({"sonnet", "opus", "haiku", "fable"})
DEFAULT_MODEL = "sonnet"
MODEL_LINE_RE = re.compile(r"(?im)^model:\s*(sonnet|opus|haiku|fable)\s*$")
DANGEROUS_FLAGS = {
    "--dangerously-skip-permissions",
    "--dangerously-bypass-hook-trust",
}
SESSION_REUSE_FLAGS = {
    "--continue",
    "-c",
    "--fork-session",
}
SESSION_REUSE_FLAGS_WITH_VALUE = {
    "--resume",
    "-r",
    "--session-id",
    "--from-pr",
    "--teleport",
}
CLAUDE_READONLY_RE = re.compile(
    r"^\s*(?:command\s+-v\s+claude|(?:\S*/)?claude\s+--version)\s*$"
)
CLAUDE_CLI_RE = re.compile(r"^\s*(?:(?:env|command)\s+)?(?:\S*/)?claude(?:\s|$)")
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
ENV_ASSIGNMENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
SKIP_PREFIX_WORDS = frozenset({"sudo", "command", "env", "then", "do"})
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


def deny(fmt: str, reason: str, user_message: str) -> int:
    if fmt == "cursor":
        return emit(
            {
                "permission": "deny",
                "agent_message": reason,
                "user_message": user_message,
            }
        )
    if fmt == "codex":
        return emit(
            {
                "systemMessage": user_message,
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }
        )
    return emit({"action": "deny", "reason": reason, "user_message": user_message})


def platform_name(fmt: str) -> str:
    return "opencode" if fmt == "internal" else fmt


def first_string(data: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def append_audit(
    project_root: Path,
    fmt: str,
    data: dict[str, Any],
    name: str,
    event: str,
    *,
    exit_code: int | None = None,
    failure: str | None = None,
    model: str | None = None,
) -> bool:
    record: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "event": event,
        "platform": platform_name(fmt),
        "tool": name or "unknown",
    }
    optional = {
        "session_id": first_string(data, "session_id", "sessionId", "conversation_id"),
        "turn_id": first_string(data, "turn_id", "turnId"),
        "tool_use_id": first_string(data, "tool_use_id", "toolUseId", "call_id"),
    }
    record.update({key: value for key, value in optional.items() if value is not None})
    if exit_code is not None:
        record["exit_code"] = exit_code
    if failure:
        record["failure"] = failure
    if model:
        record["model"] = model

    try:
        path = project_root / AUDIT_REL
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")))
            handle.write("\n")
        return True
    except OSError:
        return False


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
        if key in {
            "status",
            "reason",
            "cli",
            "invoke",
            "checked-at",
            "timeout-seconds",
            "max-turns",
            "default-model",
        }:
            values[key] = value.strip()
    return values


def parse_task_model(task: str, worker: dict[str, str]) -> str:
    matches = MODEL_LINE_RE.findall(task)
    if matches:
        return matches[-1].lower()
    default = (worker.get("default-model") or "").strip().lower()
    if default in ALLOWED_MODELS:
        return default
    return DEFAULT_MODEL


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
    if isinstance(command, str):
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


def iter_shell_statements(command: str) -> list[str]:
    """Split on top-level &&, ||, ;, |, and newlines, keeping quoted strings intact."""
    statements: list[str] = []
    buf: list[str] = []
    quote: str | None = None
    index = 0
    length = len(command)

    def flush() -> None:
        text = "".join(buf).strip()
        buf.clear()
        if text:
            statements.append(text)

    while index < length:
        char = command[index]
        if quote:
            buf.append(char)
            if char == "\\" and quote == '"' and index + 1 < length:
                buf.append(command[index + 1])
                index += 2
                continue
            if char == quote:
                quote = None
            index += 1
            continue
        if char in {"'", '"'}:
            quote = char
            buf.append(char)
            index += 1
            continue
        if command.startswith("&&", index) or command.startswith("||", index):
            flush()
            index += 2
            continue
        if char in {";", "|", "\n"}:
            flush()
            index += 1
            continue
        buf.append(char)
        index += 1
    flush()
    return statements


def statement_program(statement: str) -> str:
    tokens = statement.split()
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token in SKIP_PREFIX_WORDS or ENV_ASSIGNMENT_RE.match(token):
            index += 1
            continue
        if token.startswith("-") and index > 0 and tokens[index - 1] == "env":
            index += 1
            continue
        return token.rsplit("/", 1)[-1]
    return ""


def should_block_shell(command: str) -> bool:
    if not command.strip():
        return False
    if CLAUDE_READONLY_RE.search(command):
        return False
    if CLAUDE_CLI_RE.search(command):
        return True
    if TEST_HINT_RE.search(command):
        return False
    remainder = [
        statement
        for statement in iter_shell_statements(command)
        if statement_program(statement) not in {"", "git"}
    ]
    if not remainder:
        return False
    return bool(MUTATING_SHELL_RE.search(" ; ".join(remainder)))


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


def build_prompt(task: str) -> str:
    return (
        "You are the implementation worker for one bounded task.\n"
        "Treat the task below as the complete scope. Do not expand it into adjacent "
        "refactors, migrations, audits, or cleanup.\n"
        "Read README.md and only the relevant files under doc/ when needed. Preserve "
        "unrelated user changes. Implement the minimum complete change and run focused "
        "verification. If the task cannot be completed within its stated scope, stop and "
        "report the blocker instead of broadening the work.\n"
        "Do not commit or push. Do not invoke claude again.\n\n"
        "Bounded implementation task:\n"
        f"{task.rstrip()}\n"
    )


def configured_max_turns(worker: dict[str, str]) -> int:
    raw = worker.get("max-turns") or str(DEFAULT_MAX_TURNS)
    try:
        value = int(raw)
    except ValueError:
        return DEFAULT_MAX_TURNS
    return max(1, min(value, 100))


def fresh_session_parts(parts: list[str]) -> list[str]:
    clean: list[str] = []
    index = 0
    while index < len(parts):
        part = parts[index]
        if part in SESSION_REUSE_FLAGS_WITH_VALUE:
            index += 1
            if index < len(parts) and not parts[index].startswith("-"):
                index += 1
            continue
        if part in SESSION_REUSE_FLAGS:
            index += 1
            continue
        if any(part.startswith(f"{flag}=") for flag in SESSION_REUSE_FLAGS_WITH_VALUE):
            index += 1
            continue
        clean.append(part)
        index += 1
    return clean


def strip_flag(parts: list[str], flag: str) -> list[str]:
    clean: list[str] = []
    index = 0
    while index < len(parts):
        part = parts[index]
        if part == flag:
            index += 1
            if index < len(parts) and not parts[index].startswith("-"):
                index += 1
            continue
        if part.startswith(f"{flag}="):
            index += 1
            continue
        clean.append(part)
        index += 1
    return clean


def cli_argv(
    worker: dict[str, str], prompt: str, model: str | None = None
) -> list[str]:
    chosen = (model or DEFAULT_MODEL).strip().lower()
    if chosen not in ALLOWED_MODELS:
        chosen = DEFAULT_MODEL
    raw = worker.get("invoke") or "claude -p --permission-mode acceptEdits"
    if raw in {"", "none"}:
        raw = "claude -p --permission-mode acceptEdits"
    parts = [part for part in shlex.split(raw) if part not in DANGEROUS_FLAGS]
    parts = fresh_session_parts(parts)
    parts = strip_flag(parts, "--model")
    if not parts:
        parts = ["claude", "-p"]
    if "--no-session-persistence" not in parts:
        parts.append("--no-session-persistence")
    if "--max-turns" not in parts and not any(
        part.startswith("--max-turns=") for part in parts
    ):
        parts.extend(["--max-turns", str(configured_max_turns(worker))])
    parts.extend(["--model", chosen])
    if "-p" not in parts and "--print" not in parts:
        parts.extend(["-p", prompt])
    else:
        parts.append(prompt)
    return parts


def invoke_cli(
    project_root: Path,
    worker: dict[str, str],
    prompt: str,
    model: str | None = None,
) -> tuple[int, str]:
    if os.environ.get("COMPASS_CLI_WORKER_STUB") == "1":
        return 0, "stubbed CLI worker"
    argv = cli_argv(worker, prompt, model)
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


def task_revision(task: str) -> str:
    return hashlib.sha256(task.encode("utf-8")).hexdigest()


def load_state(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def write_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(
        json.dumps(state, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    os.replace(temp, path)


def successful_revisions(state: dict[str, Any]) -> list[str]:
    raw = state.get("successful_revisions")
    revisions = (
        [item for item in raw if isinstance(item, str)]
        if isinstance(raw, list)
        else []
    )
    legacy = state.get("task_revision")
    if (
        state.get("status") == "succeeded"
        and isinstance(legacy, str)
        and legacy not in revisions
    ):
        revisions.append(legacy)
    return revisions[-MAX_SUCCESS_HISTORY:]


def state_record(
    revision: str,
    status: str,
    successful: list[str],
    *,
    exit_code: int | None = None,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "task_revision": revision,
        "status": status,
        "successful_revisions": successful[-MAX_SUCCESS_HISTORY:],
        "updated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    if exit_code is not None:
        record["exit_code"] = exit_code
    return record


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


def delegate_command(fmt: str) -> str:
    if fmt == "codex":
        script = ".codex/hooks/cli-worker.py"
    elif fmt == "cursor":
        script = ".cursor/hooks/cli-worker.py"
    else:
        script = ".opencode/hooks/cli-worker.py"
    return f"python3 {script} --format {fmt} --delegate"


def delegation_required(name: str, fmt: str) -> tuple[str, str]:
    command = delegate_command(fmt)
    reason = (
        "Direct planner implementation is blocked. The hook intentionally did not "
        "start Claude for this individual tool call. Write or replace "
        f"{TASK_REL.as_posix()} with one bounded implementation goal, confirmed scope, "
        f"and acceptance criteria; then run `{command}` exactly once. Review the diff "
        "after it returns. Do not use --resume, --continue, or a session ID."
    )
    user_message = (
        f"🧭 Compass：已拦截 {name or 'write'}；未按单个 tool call 启动 Claude；"
        "planner 需要改用一次 task-level delegation。"
    )
    return reason, user_message


def blocker_message(detail: str) -> str:
    return f"🧭 Compass：task-level delegation 的 Claude CLI {detail}。"


def run_delegation(project_root: Path, worker: dict[str, str], fmt: str) -> int:
    task_path = project_root / TASK_REL
    state_path = project_root / STATE_REL
    try:
        task = task_path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        sys.stderr.write(f"Missing task specification at {TASK_REL.as_posix()}: {exc}\n")
        return 2
    if not task:
        sys.stderr.write(f"Task specification at {TASK_REL.as_posix()} is empty.\n")
        return 2
    if len(task) > MAX_TASK_CHARS:
        sys.stderr.write(
            f"Task specification exceeds {MAX_TASK_CHARS} characters; narrow the scope.\n"
        )
        return 2

    revision = task_revision(task)
    model = parse_task_model(task, worker)
    with ExclusiveLock(project_root / LOCK_REL):
        state = load_state(state_path)
        successful = successful_revisions(state)
        if revision in successful:
            append_audit(
                project_root,
                fmt,
                {},
                "task",
                "delegation_reused",
                exit_code=0,
                model=model,
            )
            sys.stdout.write(
                "Compass: this exact task revision already succeeded; inspect the diff "
                "instead of invoking Claude again.\n"
            )
            return 0

        write_state(state_path, state_record(revision, "running", successful))
        append_audit(project_root, fmt, {}, "task", "delegation_started", model=model)
        try:
            code, output = invoke_cli(project_root, worker, build_prompt(task), model)
        except subprocess.TimeoutExpired:
            write_state(state_path, state_record(revision, "failed", successful))
            append_audit(
                project_root,
                fmt,
                {},
                "task",
                "worker_failed",
                failure="timeout",
                model=model,
            )
            sys.stderr.write(blocker_message("执行超时") + "\n")
            return 124
        except Exception as exc:
            write_state(state_path, state_record(revision, "failed", successful))
            append_audit(
                project_root,
                fmt,
                {},
                "task",
                "worker_failed",
                failure="start-failed",
                model=model,
            )
            sys.stderr.write(blocker_message(f"启动失败：{exc}") + "\n")
            return 1

        status = "succeeded" if code == 0 else "failed"
        if code == 0:
            successful.append(revision)
        write_state(
            state_path,
            state_record(revision, status, successful, exit_code=code),
        )
        append_audit(
            project_root,
            fmt,
            {},
            "task",
            "worker_succeeded" if code == 0 else "worker_failed",
            exit_code=code,
            model=model,
        )
        if output:
            stream = sys.stdout if code == 0 else sys.stderr
            stream.write(output + "\n")
        if code == 0:
            sys.stdout.write(
                "Compass: task-level delegation succeeded in a fresh, non-persistent "
                "Claude session. Inspect the diff and run independent verification.\n"
            )
        else:
            sys.stderr.write(blocker_message(f"执行失败（exit {code}）") + "\n")
        return code


def main() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--format", default="internal")
    parser.add_argument("--delegate", action="store_true")
    args, _ = parser.parse_known_args()
    fmt = args.format if args.format in {"cursor", "codex", "internal"} else "internal"

    try:
        project_root = find_project_root(Path.cwd())
        if project_root is None:
            if args.delegate:
                sys.stderr.write("Compass project root not found.\n")
                return 2
            return allow(fmt)

        worker = parse_worker_file(project_root / COMPASS_CONTEXT_REL)
        if worker.get("status", "unknown") != "enabled":
            if args.delegate:
                sys.stderr.write("Compass CLI worker is not enabled for this project.\n")
                return 2
            return allow(fmt)

        if args.delegate:
            return run_delegation(project_root, worker, fmt)

        data = load_payload()
        name = tool_name(data)
        inp = tool_input(data)
        if not should_hand_off(project_root, name, inp):
            return allow(fmt)
    except Exception as exc:
        if args.delegate:
            sys.stderr.write(f"Compass task-level delegation failed to initialize: {exc}\n")
            return 1
        return allow(fmt)

    append_audit(project_root, fmt, data, name, "planner_blocked")
    reason, user_message = delegation_required(name, fmt)
    return deny(fmt, reason, user_message)


if __name__ == "__main__":
    os.environ.setdefault("PYTHONUTF8", "1")
    raise SystemExit(main())
