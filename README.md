# Coding Harness — Setup Guide

This guide describes how to assemble a development harness for AI coding agents, composed of plugins and skills covering spec-driven development, frontend design, code review, security, and cross-session memory.

The harness is **agent-agnostic**: the core (`CONSTITUTION.md`) works with any agent.

---

## Prerequisites

- An AI coding agent (e.g., [Claude Code](https://claude.ai/code), [OpenCode](https://opencode.ai), [Cursor](https://cursor.sh), Codex, Hermes, etc.)
- [GitHub CLI](https://cli.github.com/) (`gh`) installed and authenticated (required for the code review plugin)
- Git

---

## 1. CONSTITUTION.md Setup

`CONSTITUTION.md` defines the architectural and behavioral principles the agent **must** follow in every session. It must be placed at the root of each project.

### 1.1 Copy to the project root

```bash
cp /path/to/skills/harness/CONSTITUTION.md ./CONSTITUTION.md
```

### 1.2 Register in the agent instructions file

Each agent reads a specific instructions file at the project root. Use the table below to identify the correct file for your agent:

| Agent | Instructions file |
|-------|-------------------|
| Claude Code | `CLAUDE.md` |
| OpenCode / Codex | `AGENTS.md` |
| Cursor | `.cursorrules` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Other agents | Check the agent's documentation |

Create the file if it does not exist, then add the snippet below:

```markdown
## Project Constitution

At the start of **every session**, the agent MUST read the `CONSTITUTION.md` file located at the
root of this repository and rigorously follow all its principles, architectural rules, and
behavioral guidelines throughout the entire session.

Non-compliance invalidates any output generated.
```

---

## 2. Plugins and Skills

### 2.1 Superpowers — Spec-Driven Development

**Repository:** https://github.com/obra/superpowers

A complete software development methodology for AI coding agents: brainstorming with spec validation, detailed implementation plans, strict TDD, and subagent-driven development.

#### Installation

**Via official marketplace:**
```
/plugin install superpowers@claude-plugins-official
```

**Via Superpowers marketplace:**
```
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

#### Main workflow

| Step | Skill | Description |
|------|-------|-------------|
| 1 | `brainstorming` | Refines the idea into a validated spec |
| 2 | `using-git-worktrees` | Creates an isolated branch and workspace |
| 3 | `writing-plans` | Generates a granular task plan |
| 4 | `subagent-driven-development` | Executes tasks with two-stage review |
| 5 | `test-driven-development` | RED → GREEN → REFACTOR cycle |
| 6 | `requesting-code-review` | Review before advancing |
| 7 | `finishing-a-development-branch` | Merge/PR/discard |

Skills are triggered automatically by the agent — no manual invocation is needed.

---

### 2.2 Frontend Design — Production-Ready Interfaces

**Repository:** https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design

Generates frontend interfaces with deliberate aesthetic choices, typography, color palettes, and animations — avoiding the generic look of AI-generated code.

#### Installation

```
/plugin install frontend-design@claude-plugins-official
```

#### Usage

Simply describe what you want to build; the plugin is invoked automatically for frontend work:

```
"Create a dashboard for a music streaming app"
"Build a landing page for an AI security startup"
"Design a settings panel with dark mode"
```

---

### 2.3 Code Review — Automated Pull Request Review

**Repository:** https://github.com/anthropics/claude-code/blob/main/plugins/code-review/README.md

Launches multiple agents in parallel to audit PRs from distinct perspectives (guideline compliance, bugs, git history), with a confidence scoring system that filters out false positives.

#### Installation

```
/plugin install code-review@claude-plugins-official
```

#### Additional requirements

```bash
# macOS
brew install gh

# Authenticate
gh auth login
```

#### Usage

```
# Local review (output to terminal):
/code-review

# Post review as a PR comment:
/code-review --comment
```

The plugin automatically skips closed, draft, trivial, or already-reviewed PRs. Only issues with confidence ≥ 80 are reported.

#### Best practices

- Keep clear agent instructions files (e.g., `CLAUDE.md`, `AGENTS.md`) in the repository so the agent can verify guideline compliance
- Run on all PRs with meaningful changes
- Update the instructions file based on recurring patterns identified in reviews

---

### 2.4 Security Guidance — Secure Code Generation

**Repository:** https://github.com/anthropics/claude-code/tree/main/plugins/security-guidance

Guides the agent to apply security best practices during code generation and review.

#### Installation

```
/plugin install security-guidance@claude-plugins-official
```

The plugin is activated automatically while writing code — no manual invocation required.

---

### 2.5 OpenCode-Mem — Persistent Cross-Session Memory

**Repository:** https://github.com/tickernelz/opencode-mem

A persistent memory system for AI coding agents that enables long-term context retention across sessions using a local vector database. Features automatic user profile learning, smart deduplication, memory scoping, and a web UI for inspection.

#### Prerequisites

- [Bun](https://bun.sh/) (recommended runtime)
- Standard plugin environment

#### Installation

Add to your configuration at `~/.config/opencode/opencode.json`:

```json
{
  "plugin": ["opencode-mem"]
}
```

The plugin downloads automatically on next startup.

#### Configuration

Create or edit `~/.config/opencode/opencode-mem.jsonc`:

```jsonc
{
  "storagePath": "~/.opencode-mem/data",
  "embeddingModel": "Xenova/nomic-embed-text-v1",
  "memory": {
    "defaultScope": "project"
  },
  "webServerEnabled": true,
  "webServerPort": 4747,
  "autoCaptureEnabled": true,

  // Use any provider already authenticated in OpenCode (no separate API key needed)
  "opencodeProvider": "anthropic",
  "opencodeModel": "claude-haiku-4-5-20251001"
}
```

#### Usage

```
memory({ mode: "add", content: "Project uses microservices architecture" });
memory({ mode: "search", query: "architecture decisions" });
memory({ mode: "search", query: "architecture decisions", scope: "all-projects" });
memory({ mode: "list", limit: 10 });
```

Access the web UI at `http://127.0.0.1:4747` for visual memory browsing and management.

#### Memory scope

| Scope | Behavior |
|-------|----------|
| `project` (default) | Queries only the current project |
| `all-projects` | Queries across all project shards |

---

## 3. Per-project setup checklist

```
[ ] Copy CONSTITUTION.md to the project root
[ ] Add the CONSTITUTION.md read instruction to your agent's instructions file
      (CLAUDE.md, AGENTS.md, .cursorrules, .github/copilot-instructions.md, etc.)
[ ] Install the plugins and skills you want to use (see section 2)
```

### Suggested stack

```
[ ] Install Superpowers (spec-driven development + TDD)
[ ] Install Frontend Design (if the project has a UI)
[ ] Install Code Review (requires authenticated gh CLI)
[ ] Install Security Guidance
[ ] Install OpenCode-Mem (cross-session memory)
```

---

## 4. References

| Resource | Link |
|----------|------|
| Superpowers | https://github.com/obra/superpowers |
| Frontend Design Plugin | https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design |
| Code Review Plugin | https://github.com/anthropics/claude-code/blob/main/plugins/code-review/README.md |
| Security Guidance Plugin | https://github.com/anthropics/claude-code/tree/main/plugins/security-guidance |
| OpenCode-Mem | https://github.com/tickernelz/opencode-mem |
| GitHub CLI | https://cli.github.com/ |
| Bun | https://bun.sh/ |

---

## Inspiration

This project was inspired by the Anthropic engineering paper:

> **Harness Design for Long-Running Applications**
> Anthropic Engineering — https://www.anthropic.com/engineering/harness-design-long-running-apps

---

## To Do

- [ ] **Evaluation feedback mechanism** — The paper highlights that an effective harness requires a robust feedback loop to evaluate the quality of implemented code (correctness, adherence to spec, and iteration quality).
