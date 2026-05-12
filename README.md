# Coding Harness — Setup Guide

This guide describes how to assemble a development harness for AI coding workflows, composed of plugins, tools, and skills covering spec-driven development, frontend design, code review, security, browser automation, and persistent memory.

The harness is **agent-agnostic**: the core (`CONSTITUTION.md`) works with any assistant, CLI, editor integration, or coding environment.

---

## Prerequisites

- An AI coding environment (for example: CLI assistants, editor integrations, or agent-based coding tools)
- [GitHub CLI](https://cli.github.com/) (`gh`) installed and authenticated (required for the code review workflow)
- Git

---

## 1. CONSTITUTION.md Setup

`CONSTITUTION.md` defines the architectural and behavioral principles that must be followed in every session. It must be placed at the root of each project.

### 1.1 Copy to the project root

```bash
cp /path/to/skills/harness/CONSTITUTION.md ./CONSTITUTION.md
```

### 1.2 Register in your environment instructions file

Each coding environment typically provides a project-level instructions file or configuration entry. Add a reference to `CONSTITUTION.md` in the mechanism your environment uses for persistent project instructions.

Common examples include:

| Environment | Instructions file |
|------------|-------------------|
| Claude Code | `CLAUDE.md` |
| OpenCode / Codex | `AGENTS.md` |
| Cursor | `.cursorrules` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Other environments | Check the environment documentation |

Create the file if it does not exist, then add the snippet below:

```markdown
## Project Constitution

At the start of **every session**, the coding system MUST read the `CONSTITUTION.md` file located at the
root of this repository and rigorously follow all its principles, architectural rules, and
behavioral guidelines throughout the entire session.

Non-compliance invalidates any output generated.
```

---

## 2. Plugins, Tools, and Skills

### 2.1 Superpowers — Spec-Driven Development

**Repository:** https://github.com/obra/superpowers

A complete software development methodology for AI-assisted coding: brainstorming with spec validation, detailed implementation plans, strict TDD, and multi-step task execution.

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

These skills may be triggered automatically or manually depending on the environment in which they are installed.

---

### 2.2 UI UX Pro Max Skill — Production-Ready Interfaces

**Repository:** https://github.com/nextlevelbuilder/ui-ux-pro-max-skill

A UI/UX-focused skill for generating polished, production-ready interfaces with strong visual hierarchy, layout quality, and refined user experience decisions.

#### Installation

```
/plugin install @nextlevelbuilder/ui-ux-pro-max-skill
```

#### Usage

Describe the interface you want to build using prompts such as:

```
"Create a dashboard for a music streaming app"
"Build a landing page for an AI security startup"
"Design a settings panel with dark mode"
```

---

### 2.3 Agent Browser — Browser Automation for AI Agents

**Repository:** https://github.com/vercel-labs/agent-browser/tree/main

A browser automation plugin that enables AI agents to navigate pages, interact with web interfaces, and perform browser-based workflows for testing, research, and task execution.

#### Installation

Follow the installation and setup instructions in the repository:

```
https://github.com/vercel-labs/agent-browser/tree/main
```

#### Usage

Use it when your workflow requires actions such as:

```
"Open the app in a browser and validate the main flow"
"Navigate through a signup form and inspect UI behavior"
"Use browser automation to verify a dashboard interaction"
```

---

### 2.4 Code Review — Automated Pull Request Review

**Repository:** https://github.com/anthropics/claude-code/blob/main/plugins/code-review/README.md

Launches multiple review passes in parallel to audit pull requests from distinct perspectives (guideline compliance, bugs, and git history), with a confidence scoring system that filters out false positives.

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

The review flow automatically skips closed, draft, trivial, or already-reviewed pull requests. Only issues with confidence ≥ 80 are reported.

#### Best practices

- Keep clear project instruction files in the repository so the review workflow can verify guideline compliance
- Run reviews on all pull requests with meaningful changes
- Update project instructions based on recurring patterns identified in reviews

---

### 2.5 Security Guidance — Secure Code Generation

**Repository:** https://github.com/anthropics/claude-code/tree/main/plugins/security-guidance

Provides guidance for applying security best practices during code generation and review.

#### Installation

```
/plugin install security-guidance@claude-plugins-official
```

This guidance is typically applied automatically during implementation and review workflows.

---

### 2.6 OpenCode-Mem — Persistent Cross-Session Memory

**Repository:** https://github.com/tickernelz/opencode-mem

A persistent memory system for AI coding workflows that enables long-term context retention across sessions using a local vector database. Features automatic user profile learning, smart deduplication, and semantic recall.

#### Prerequisites

- [Bun](https://bun.sh/) (recommended runtime)
- A compatible plugin or extension environment

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

  // Use any provider already authenticated in the host environment (no separate API key needed)
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
[ ] Add the CONSTITUTION.md read instruction to your project instructions mechanism
[ ] Install the plugins, tools, and skills you want to use (see section 2)
```

### Suggested stack

```
[ ] Install Superpowers (spec-driven development + TDD)
[ ] Install @nextlevelbuilder/ui-ux-pro-max-skill (if the project has a UI)
[ ] Install Agent Browser (if the project needs browser automation or web interaction testing)
[ ] Install Code Review (requires authenticated gh CLI)
[ ] Install Security Guidance
[ ] Install OpenCode-Mem (cross-session memory)
```

---

## 4. References

| Resource | Link |
|----------|------|
| Superpowers | https://github.com/obra/superpowers |
| UI UX Pro Max Skill | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill |
| Agent Browser | https://github.com/vercel-labs/agent-browser/tree/main |
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

- [ ] **Evaluation feedback mechanism** — The paper highlights that an effective harness requires a robust feedback loop to evaluate the quality of implemented code (correctness, adherence to spec, and maintainability) and use those signals to improve subsequent iterations.
