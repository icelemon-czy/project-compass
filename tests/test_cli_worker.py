from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "compass" / "hooks" / "cli-worker" / "run.py"
SPEC = importlib.util.spec_from_file_location("compass_cli_worker", SCRIPT)
assert SPEC and SPEC.loader
worker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(worker)


class CliArgvTests(unittest.TestCase):
    def test_raw_claude_invocation_is_blocked_but_detection_is_allowed(self) -> None:
        self.assertTrue(
            worker.should_block_shell("claude -p --resume old-session 'continue'")
        )
        self.assertTrue(worker.should_block_shell("/usr/local/bin/claude -p task"))
        self.assertFalse(worker.should_block_shell("command -v claude"))
        self.assertFalse(worker.should_block_shell("claude --version"))

    def test_forces_fresh_bounded_session(self) -> None:
        argv = worker.cli_argv(
            {
                "invoke": (
                    "claude -p --resume old-session --continue --session-id deadbeef "
                    "--fork-session --model opus"
                ),
                "max-turns": "12",
            },
            "task",
        )

        self.assertNotIn("--resume", argv)
        self.assertNotIn("old-session", argv)
        self.assertNotIn("--continue", argv)
        self.assertNotIn("--session-id", argv)
        self.assertNotIn("deadbeef", argv)
        self.assertNotIn("--fork-session", argv)
        self.assertIn("--no-session-persistence", argv)
        self.assertEqual(argv[argv.index("--max-turns") + 1], "12")
        self.assertEqual(argv[-1], "task")

    def test_preserves_explicit_max_turns(self) -> None:
        argv = worker.cli_argv(
            {"invoke": "claude -p --max-turns 7 --no-session-persistence"},
            "task",
        )

        self.assertEqual(argv.count("--max-turns"), 1)
        self.assertEqual(argv.count("--no-session-persistence"), 1)

    def test_resume_without_value_does_not_consume_next_flag(self) -> None:
        argv = worker.cli_argv(
            {"invoke": "claude -p --resume --model sonnet"},
            "task",
        )

        self.assertNotIn("--resume", argv)
        self.assertIn("--model", argv)
        self.assertIn("sonnet", argv)


class DelegationTests(unittest.TestCase):
    def make_project(self, root: Path) -> None:
        context = root / ".compass" / "context"
        context.mkdir(parents=True)
        (context / "cli-worker.md").write_text(
            "status: enabled\n"
            "invoke: claude -p --resume old --permission-mode acceptEdits\n"
            "timeout-seconds: 600\n"
            "max-turns: 30\n",
            encoding="utf-8",
        )
        (context / "cli-worker-task.md").write_text(
            "Goal: change one behavior.\nAcceptance: focused test passes.\n",
            encoding="utf-8",
        )

    def test_same_task_revision_only_invokes_once(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            self.make_project(root)
            config = worker.parse_worker_file(root / worker.COMPASS_CONTEXT_REL)

            with mock.patch.dict(os.environ, {"COMPASS_CLI_WORKER_STUB": "1"}):
                self.assertEqual(worker.run_delegation(root, config, "codex"), 0)
                self.assertEqual(worker.run_delegation(root, config, "codex"), 0)

            audit = [
                json.loads(line)
                for line in (root / worker.AUDIT_REL).read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(
                [record["event"] for record in audit],
                ["delegation_started", "worker_succeeded", "delegation_reused"],
            )
            state = json.loads((root / worker.STATE_REL).read_text(encoding="utf-8"))
            self.assertEqual(state["status"], "succeeded")

    def test_rewriting_task_creates_new_revision(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            self.make_project(root)
            config = worker.parse_worker_file(root / worker.COMPASS_CONTEXT_REL)
            task_path = root / worker.TASK_REL

            with mock.patch.dict(os.environ, {"COMPASS_CLI_WORKER_STUB": "1"}):
                self.assertEqual(worker.run_delegation(root, config, "cursor"), 0)
                task_path.write_text(
                    "Goal: change a different behavior.\nAcceptance: another test passes.\n",
                    encoding="utf-8",
                )
                self.assertEqual(worker.run_delegation(root, config, "cursor"), 0)

            audit = [
                json.loads(line)
                for line in (root / worker.AUDIT_REL).read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(
                [record["event"] for record in audit].count("delegation_started"),
                2,
            )

    def test_rewriting_identical_task_is_still_deduplicated(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            self.make_project(root)
            config = worker.parse_worker_file(root / worker.COMPASS_CONTEXT_REL)
            task_path = root / worker.TASK_REL
            task = task_path.read_text(encoding="utf-8")

            with mock.patch.dict(os.environ, {"COMPASS_CLI_WORKER_STUB": "1"}):
                self.assertEqual(worker.run_delegation(root, config, "codex"), 0)
                task_path.write_text(task, encoding="utf-8")
                self.assertEqual(worker.run_delegation(root, config, "codex"), 0)

            audit = [
                json.loads(line)
                for line in (root / worker.AUDIT_REL).read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(
                [record["event"] for record in audit],
                ["delegation_started", "worker_succeeded", "delegation_reused"],
            )

    def test_success_history_prevents_alternating_task_loop(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            self.make_project(root)
            config = worker.parse_worker_file(root / worker.COMPASS_CONTEXT_REL)
            task_path = root / worker.TASK_REL
            first = task_path.read_text(encoding="utf-8")

            with mock.patch.dict(os.environ, {"COMPASS_CLI_WORKER_STUB": "1"}):
                self.assertEqual(worker.run_delegation(root, config, "codex"), 0)
                task_path.write_text("Goal: second task.\nAcceptance: pass.\n", encoding="utf-8")
                self.assertEqual(worker.run_delegation(root, config, "codex"), 0)
                task_path.write_text(first, encoding="utf-8")
                self.assertEqual(worker.run_delegation(root, config, "codex"), 0)

            audit = [
                json.loads(line)
                for line in (root / worker.AUDIT_REL).read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(
                [record["event"] for record in audit].count("delegation_started"),
                2,
            )
            self.assertEqual(audit[-1]["event"], "delegation_reused")

    def test_hook_message_requires_task_level_delegation(self) -> None:
        reason, user_message = worker.delegation_required("Edit", "codex")

        self.assertIn("cli-worker-task.md", reason)
        self.assertIn("--delegate", reason)
        self.assertIn("did not start Claude", reason)
        self.assertIn("task-level delegation", user_message)

    def test_native_hook_blocks_without_starting_worker(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            self.make_project(root)
            payload = json.dumps(
                {"tool_name": "Edit", "tool_input": {"file_path": "src/app.py"}}
            )

            result = subprocess.run(
                ["python3", str(SCRIPT), "--format", "internal"],
                cwd=root,
                input=payload,
                capture_output=True,
                text=True,
                check=False,
                env={**os.environ, "COMPASS_CLI_WORKER_STUB": "1"},
            )

            self.assertEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stdout)["action"], "deny")
            self.assertFalse((root / worker.STATE_REL).exists())
            audit = [
                json.loads(line)
                for line in (root / worker.AUDIT_REL).read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual([record["event"] for record in audit], ["planner_blocked"])


if __name__ == "__main__":
    unittest.main()
