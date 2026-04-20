{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$(git rev-parse --show-toplevel 2>/dev/null || pwd)/scripts/harness.py\" codex-session-start",
            "statusMessage": "Loading service harness notes"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$(git rev-parse --show-toplevel 2>/dev/null || pwd)/scripts/harness.py\" codex-pre-tool-use",
            "statusMessage": "Checking risky shell command"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$(git rev-parse --show-toplevel 2>/dev/null || pwd)/scripts/harness.py\" codex-stop",
            "timeout": 30,
            "statusMessage": "Checking task completion rules"
          }
        ]
      }
    ]
  }
}

