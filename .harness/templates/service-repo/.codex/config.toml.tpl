model = "gpt-5.5"
model_reasoning_effort = "medium"
review_model = "gpt-5.6"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
project_doc_fallback_filenames = ["CLAUDE.md"]
project_root_markers = ["AGENTS.md", ".codex/config.toml", "service.yaml", "docs-manifest.json"]

[features]
codex_hooks = true

[sandbox_workspace_write]
network_access = false
writable_roots = ["/tmp"]

[agents]
max_threads = 6
max_depth = 1
