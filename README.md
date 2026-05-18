# Coding Harness — Setup Guide

This guide describes how to assemble a development harness for AI coding workflows, composed of plugins, tools, and skills covering spec-driven development, frontend design, browser automation, database best practices, code review, security, and persistent memory.

The harness is **agent-agnostic**: every plugin, tool, skill, and the core `CONSTITUTION.md` work with any assistant, CLI, editor integration, or coding environment — Claude Code, Codex, Cursor, OpenCode, Gemini CLI, Copilot, Windsurf, Cline, and others.

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

## 2. Plugins, Tools, Skills and MCPs

All items in this section are **environment-agnostic** — they work in Claude Code, Codex, Cursor, OpenCode, Gemini CLI, Copilot, Windsurf, Cline, and other AI coding tools. Installation commands shown follow each tool's own conventions; adapt the syntax to your environment as needed.

### 2.1 Superpowers — Spec-Driven Development

**Type:** Skill suite  
**Repository:** https://github.com/obra/superpowers

A complete software development methodology for AI-assisted coding, including spec validation, detailed planning, strict TDD, and structured multi-step execution.

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

#### Recommended workflow

| Step | Skill | Description |
|------|-------|-------------|
| 1 | `brainstorming` | Refines the idea into a validated spec |
| 2 | `using-git-worktrees` | Creates an isolated branch and workspace |
| 3 | `writing-plans` | Generates a granular task plan |
| 4 | `subagent-driven-development` | Executes tasks with two-stage review |
| 5 | `test-driven-development` | RED → GREEN → REFACTOR cycle |
| 6 | `requesting-code-review` | Runs review before advancing |
| 7 | `finishing-a-development-branch` | Merge, open a PR, or discard |

These skills may be triggered automatically or manually depending on the environment in which they are installed.

---

### 2.2 UI UX Pro Max Skill — Production-Ready Interfaces

**Type:** Skill  
**Repository:** https://github.com/nextlevelbuilder/ui-ux-pro-max-skill

A UI/UX-focused skill for generating polished, production-ready interfaces with strong visual hierarchy, better layouts, and more refined user experience decisions.

#### Installation

```
/plugin install @nextlevelbuilder/ui-ux-pro-max-skill
```

#### Typical usage

Describe the interface you want to build using prompts such as:

```
"Create a dashboard for a music streaming app"
"Build a landing page for an AI security startup"
"Design a settings panel with dark mode"
```

---

### 2.3 Agent Browser — Browser Automation for AI Agents

**Type:** Plugin / tool  
**Repository:** https://github.com/vercel-labs/agent-browser/tree/main

A browser automation tool that enables AI agents to navigate pages, interact with web interfaces, and perform browser-based workflows for testing, research, and task execution.

#### Installation

Follow the installation and setup instructions in the repository:

```
https://github.com/vercel-labs/agent-browser/tree/main
```

#### Typical usage

Use it when your workflow requires actions such as:

```
"Open the app in a browser and validate the main flow"
"Navigate through a signup form and inspect UI behavior"
"Use browser automation to verify a dashboard interaction"
```

---

### 2.4 Supabase Postgres Best Practices — Database Performance and Schema Guidance

**Type:** Skill  
**Repository:** https://github.com/supabase/agent-skills/tree/3e7771598f3a03d29533208dd7b5a50bdfc8860f/skills/supabase-postgres-best-practices

A Postgres optimization and database design skill maintained by Supabase. It provides practical guidance for query performance, indexing, connection management, security and RLS, schema design, locking, monitoring, and Postgres-specific optimization patterns.

#### Installation

Reference the skill in your environment using:

```
@supabase/agent-skills/files/skills/supabase-postgres-best-practices
```

#### Typical usage

Use this skill when your workflow involves tasks such as:

```
"Optimize this Postgres query and suggest indexes"
"Review this schema for Supabase and Postgres best practices"
"Improve RLS performance and database access patterns"
```

---

### 2.5 Code Review — Automated Pull Request Review

**Type:** Plugin  
**Repository:** https://github.com/anthropics/claude-code/blob/main/plugins/code-review/README.md

A pull request review plugin that runs multiple review passes in parallel to audit guideline compliance, bugs, and git history, while using confidence scoring to reduce false positives.

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

#### Typical usage

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

### 2.6 Security Guidance — Secure Code Generation

**Type:** Plugin / guidance  
**Repository:** https://github.com/anthropics/claude-code/tree/main/plugins/security-guidance

A security-oriented plugin that helps apply secure coding best practices during implementation and review workflows.

#### Installation

```
/plugin install security-guidance@claude-plugins-official
```

#### Typical usage

This guidance is typically applied automatically during implementation and review workflows.

---

### 2.7 OpenCode-Mem — Persistent Cross-Session Memory

**Type:** Plugin / memory system  
**Repository:** https://github.com/tickernelz/opencode-mem

A persistent memory system for AI coding workflows that enables long-term context retention across sessions using a local vector database. It includes automatic user profile learning, smart deduplication, and semantic recall.

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

#### Typical usage

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

### 2.8 RTK — CLI Proxy for LLM Token Optimization

**Type:** CLI tool / proxy  
**Repository:** https://github.com/rtk-ai/rtk

A high-performance CLI proxy that intercepts and filters command output before it reaches the LLM context, reducing token consumption by 60–90% on common dev commands (`git`, `cat`, `grep`, `cargo test`, `pytest`, etc.). Single Rust binary, zero dependencies, <10ms overhead.

#### Installation

**Homebrew (macOS/Linux):**
```bash
brew install rtk
```

**Quick install (Linux/macOS):**
```bash
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
```

**Cargo:**
```bash
cargo install --git https://github.com/rtk-ai/rtk
```

**Windows:** Download the zip from [releases](https://github.com/rtk-ai/rtk/releases), extract `rtk.exe` to a directory in your PATH.

#### Quick start

```bash
rtk init -g              # Install hook for Claude Code / Copilot
rtk init -g --opencode   # OpenCode plugin
rtk gain                 # Show token savings stats
```

After installing, restart your AI tool. The hook automatically rewrites Bash commands (e.g. `git status` → `rtk git status`), delivering compact output without manual intervention.

---

### 2.9 Playwright MCP — Browser Automation via Model Context Protocol

**Type:** MCP server  
**Repository:** https://github.com/microsoft/playwright-mcp/tree/main

An MCP server maintained by Microsoft that gives AI agents browser automation capabilities through Playwright, enabling page navigation, interaction, inspection, and end-to-end workflow validation from MCP-compatible coding environments.

#### Installation

Install or register the MCP server according to your environment's MCP configuration format. The server can be run directly with `npx`:

```bash
npx @playwright/mcp@latest
```

Example MCP server configuration:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

#### Typical usage

Use it when your workflow requires browser-based actions such as:

```
"Open the app and verify the signup flow"
"Inspect this page and identify accessibility issues"
"Click through the dashboard and validate the main user journey"
```

---

## 3. Per-project setup checklist

```
[ ] Copy CONSTITUTION.md to the project root
[ ] Add the CONSTITUTION.md read instruction to your project instructions mechanism
[ ] Install the plugins, tools, skills, and MCPs you want to use (see section 2)
```

### Suggested stack

```
[ ] Install Superpowers (spec-driven development + TDD)
[ ] Install @nextlevelbuilder/ui-ux-pro-max-skill (if the project has a UI)
[ ] Install Agent Browser (if the project needs browser automation or web interaction testing)
[ ] Install Supabase Postgres Best Practices (if the project uses Supabase or Postgres)
[ ] Install Code Review (requires authenticated gh CLI)
[ ] Install Security Guidance
[ ] Install OpenCode-Mem (cross-session memory)
[ ] Install Playwright MCP (if the project needs browser automation through MCP)
```

---

## 4. References

| Resource | Link |
|----------|------|
| Superpowers | https://github.com/obra/superpowers |
| UI UX Pro Max Skill | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill |
| Agent Browser | https://github.com/vercel-labs/agent-browser/tree/main |
| Supabase Postgres Best Practices | https://github.com/supabase/agent-skills/tree/3e7771598f3a03d29533208dd7b5a50bdfc8860f/skills/supabase-postgres-best-practices |
| Code Review Plugin | https://github.com/anthropics/claude-code/blob/main/plugins/code-review/README.md |
| Security Guidance Plugin | https://github.com/anthropics/claude-code/tree/main/plugins/security-guidance |
| OpenCode-Mem | https://github.com/tickernelz/opencode-mem |
| Playwright MCP | https://github.com/microsoft/playwright-mcp/tree/main |
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
