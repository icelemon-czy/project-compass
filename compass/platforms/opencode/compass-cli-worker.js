// compass:generated hook=cli-worker
import { spawnSync } from "node:child_process"
import path from "node:path"

export const CompassCliWorker = async ({ directory }) => {
  const script = path.join(directory, ".opencode", "hooks", "cli-worker.py")

  return {
    "tool.execute.before": async (input, output) => {
      const payload = {
        tool_name: input.tool,
        tool_input: output?.args || {},
      }
      const result = spawnSync("python3", [script, "--format", "internal"], {
        cwd: directory,
        encoding: "utf8",
        input: JSON.stringify(payload),
        timeout: 660000,
      })
      if (result.error || result.status !== 0) {
        return
      }
      let parsed
      try {
        parsed = JSON.parse((result.stdout || "").trim().split("\n").pop() || "{}")
      } catch {
        return
      }
      if (parsed.action === "deny") {
        throw new Error(parsed.reason || "CLI worker redirected this implementation to Claude Code CLI.")
      }
    },
  }
}
