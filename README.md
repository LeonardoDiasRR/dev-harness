# Coding Harness — Setup Guide

This guide describes how to assemble a development harness for AI coding workflows, composed of plugins, tools, and skills covering spec-driven development, frontend design, browser automation, database best practices, security, and persistent memory.

The harness is **agent-agnostic**: every plugin, tool, skill, and the core `CONSTITUTION.md` work with any assistant, CLI, editor integration, or coding environment — Claude Code, Codex, Cursor, OpenCode, Gemini CLI, Copilot, Windsurf, Cline, and others.

---

## Prerequisites

- An AI coding environment (for example: CLI assistants, editor integrations, or agent-based coding tools)
- [GitHub CLI](https://cli.github.com/) (`gh`) installed and authenticated
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

## 2. OpenCode Agent

The `agents/` directory contains the definition of the **Coder** primary agent for OpenCode.

### Coder — Primary Agent

[`agents/coder.md`](agents/coder.md) defines a `primary`-mode autonomous software-development agent: implementing features, refactoring, debugging, writing tests, planning non-trivial changes, delegating multi-step work to subagents, and producing verified, quality-focused code. It also handles authorized security testing and defensive workflows, and maintains persistent memory across sessions. It references a shared system prompt at `~/.config/opencode/agent/system-prompt.md`.

A primary agent is the main assistant you interact with directly — switch between primaries with **Tab** during a session.

#### Installation

Copy the agent definition to the OpenCode global agents directory:

```bash
mkdir -p ~/.config/opencode/agent
cp agents/coder.md ~/.config/opencode/agent/coder.md
```

Restart OpenCode. The **Coder** agent will appear as a selectable primary agent. Press **Tab** to cycle through available primary agents.

The agent file uses frontmatter (`mode: primary`, `description`, `color`) and an optional body referencing the system prompt. See the [OpenCode agents documentation](https://opencode.ai/docs/pt-br/agents/) for all available options (`model`, `temperature`, `tools`, `permission`, `steps`, etc.).

---

## 3. Plugins, Tools, Skills and MCPs

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

### 2.3 agent-browser — Browser Automation CLI for AI Agents

**Type:** CLI tool + skill  
**Repository:** https://github.com/vercel-labs/agent-browser  
**Website:** https://agent-browser.dev

A browser automation CLI built for AI agents by Vercel Labs. 100% native Rust: a CLI talks to a native daemon that drives Chrome directly over CDP — no Playwright or Puppeteer dependency. It returns compact accessibility-tree snapshots with ref-based element targeting (`@e1`, `@e2`), keeping LLM context usage low (~200–400 tokens vs thousands for a full DOM dump) while giving deterministic element selection. 50+ commands cover navigation, forms, screenshots, network, storage, tabs, frames, sessions, and debugging.

#### Installation

**Global install (recommended):**
```bash
npm install -g agent-browser
agent-browser install   # Download Chrome from Chrome for Testing (first time only)
```

**Homebrew (macOS):**
```bash
brew install agent-browser
agent-browser install
```

**Quick start (no install):**
```bash
npx agent-browser open example.com
```

**Skill for AI coding assistants:**
```bash
npx skills add vercel-labs/agent-browser
```

This works with Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, OpenCode, Windsurf, and others. Do not copy `SKILL.md` from `node_modules` — always install from the repository so it stays up to date.

#### AI agent setup

Add to your project or global instructions file (`AGENTS.md` / `CLAUDE.md`):

```markdown
## Browser Automation

Use `agent-browser` for web automation. Run `agent-browser --help` for all commands.

Core workflow:
1. `agent-browser open <url>` - Navigate to page
2. `agent-browser snapshot -i` - Get interactive elements with refs (@e1, @e2)
```

#### Typical usage

```bash
agent-browser open example.com      # Navigate to a page
agent-browser snapshot -i           # Interactive elements with refs
# - heading "Example Domain" [ref=e1]
# - link "More information..." [ref=e2]
agent-browser click @e2             # Click by ref
agent-browser fill @e3 "text"       # Fill a form field
agent-browser screenshot page.png   # Capture a screenshot
```

Or trigger it from your agent with prompts such as:

```
"Open the app and verify the signup flow"
"Inspect this page and identify accessibility issues"
"Click through the dashboard and validate the main user journey"
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

### 2.5 Security Guidance — Secure Code Generation

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

### 2.6 OpenCode-Mem — Persistent Cross-Session Memory

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

---

### 2.7 RTK — CLI Proxy for LLM Token Optimization

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

### 2.8 Context7 — Up-to-Date Code Documentation for LLMs

**Type:** MCP server / CLI + Skills  
**Repository:** https://github.com/upstash/context7  
**Website:** https://context7.com

Context7 provides **up-to-date, version-specific** documentation and code examples straight from the source into your AI agent's prompt. It solves three common problems: outdated code examples from old training data, hallucinated APIs that don't exist, and generic answers for old package versions.

It works in **two modes**:

| Mode | Description |
|------|-------------|
| **CLI + Skills** | Installs a skill that guides your agent to fetch docs using `ctx7` CLI commands (no MCP required) |
| **MCP** | Registers a Context7 MCP server so your agent can call documentation tools natively |

#### Installation (quick setup)

```shell
npx ctx7 setup
```

- Authenticates via OAuth, generates an API key, installs the skill
- Choose between **CLI + Skills** or **MCP** mode during setup
- Use `--cursor`, `--claude`, or `--opencode` to target a specific agent

#### Manual MCP configuration (for other MCP clients)

Use the server URL `https://mcp.context7.com/mcp` and pass your API key via the `CONTEXT7_API_KEY` header.  
[Full client-specific setup guide →](https://context7.com/docs/resources/all-clients)

#### Available tools

**CLI Commands:**

| Command | Description |
|---------|-------------|
| `ctx7 library <name> <query>` | Searches the Context7 index by library name and returns matching libraries with their IDs |
| `ctx7 docs <libraryId> <query>` | Retrieves documentation for a library (e.g., `/mongodb/docs`, `/vercel/next.js`) |

**MCP Tools:**

| Tool | Parameters | Description |
|------|------------|-------------|
| `resolve-library-id` | `query`, `libraryName` | Resolves a general library name into a Context7-compatible library ID |
| `query-docs` | `libraryId`, `query` | Retrieves documentation for a specific library |

#### Typical usage

Add a `use context7` instruction to your prompts:

```adblock
Create a Next.js middleware that checks for a valid JWT in cookies
and redirects unauthenticated users to `/login`. use context7
```

```adblock
Configure a Cloudflare Worker script to cache
JSON API responses for five minutes. use context7
```

#### Important tips

- **Specify a library ID:** Use `use library /supabase/supabase` to skip library-matching
- **Specify a version:** E.g., "How do I set up Next.js 14 middleware?" — Context7 automatically matches the appropriate version
- **Add a rule:** For automatic trigger without explicit `use context7`, add a rule to your environment's instructions file (e.g., `CLAUDE.md`, `.cursorrules`)

```
Always use Context7 when I need library/API documentation, code generation, setup or configuration steps without me having to explicitly ask.
```

#### Removal

```shell
npx ctx7 remove
```

If globally installed via `npm install -g ctx7`, uninstall separately: `npm uninstall -g ctx7`.

---

### 2.10 Ponytail — Minimalist Coding Plugin

**Type:** Plugin / skill suite  
**Repository:** https://github.com/DietrichGebert/ponytail

Ponytail keeps AI coding workflows focused on the smallest correct change: delete before adding, reuse existing code, prefer standard library and native platform features, and avoid speculative abstractions.

#### Installation

Install from the package registry supported by your coding environment, or follow the repository instructions:

```
/plugin install @dietrichgebert/ponytail
```

#### Typical usage

Use it when you want the agent to avoid over-engineering:

```
"Use ponytail mode and implement the simplest working fix"
"Review this PR for over-engineering"
"Audit this repo for code we can delete"
```

---

### 2.11 code-review-graph — Local Code Intelligence Graph for Token-Efficient Reviews

**Type:** MCP server / CLI  
**Repository:** https://github.com/tirth8205/code-review-graph  
**Website:** https://code-review-graph.com

AI coding tools often re-read large parts of the codebase on every task. `code-review-graph` fixes that: it builds a persistent structural map of your code with Tree-sitter (functions, classes, imports as nodes; calls, inheritance, test coverage as edges), keeps it updated incrementally, and serves compact context over MCP so the assistant reads only the files a change actually touches. Local-first (SQLite graph), with blast-radius analysis, risk-scored reviews, benchmarks showing ~8x average token reduction on reviews, and optional semantic search via vector embeddings.

#### Installation

Requires Python 3.10+ (installing [uv](https://docs.astral.sh/uv/) is recommended):

```bash
pip install code-review-graph          # or: pipx install code-review-graph
code-review-graph install              # detect installed AI coding tools and configure each one
code-review-graph build                # parse the codebase
```

`install` detects which AI coding tools you have (Claude Code, Codex, Cursor, Windsurf, Zed, Continue, OpenCode, Gemini CLI, GitHub Copilot, and others), writes an MCP server entry for each, installs hooks and skills where supported, and adds graph instructions to the platform's rules file. Restart your tool after installing.

The initial build takes ~10 seconds for a 500-file project. After that, the graph updates automatically on every file edit and git commit (editor hooks, git pre-commit hook, or watch mode).

The same analysis also runs as a composite GitHub Action for risk-scored PR reviews in CI:

```yaml
- uses: tirth8205/code-review-graph@v2
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

#### Typical usage

Open your project and ask your AI assistant:

```
"Build the code review graph for this project"
"Review this change and show the blast radius"
"What files do I need to read to safely refactor this function?"
```

Key CLI commands:

| Command | Description |
|---------|-------------|
| `code-review-graph build` | Parse the codebase into the graph |
| `code-review-graph update` | Incremental update after changes |
| `code-review-graph query` | Query the graph directly |
| `code-review-graph watch` | Watch mode — keep the graph updated |
| `code-review-graph visualize` | Interactive D3.js force-directed graph |
| `code-review-graph eval` | Run evaluation benchmarks |
| `code-review-graph serve` | Start the MCP server |

---

### 2.12 ub-mode — Disciplined Engineering Principles for Code Changes

**Type:** Skill  
**Repository:** https://github.com/unclebob/ub-mode

A skill that enforces a fixed sequence on every code change: **First Make it Work**, then **Make it Right**, then **Follow Practice**. It reduces Uncle Bob's `poteto-mode` rules to a checklist an agent can apply, and pairs them with deterministic quality gates.

The working phase covers the laziness protocol (one decision in one place, smallest edit that solves the problem), foundational thinking, TDD, redesign from first principles, attacking the premise when two fixes fail the same gate, subtracting before adding, and building the lever.

The correcting phase requires root-cause fixes, verifiable work units, behaviour-level tests, and three gate tools: **Crapper** (CRAP score per function below 10), **Dryer** (duplication below 0.8 similarity) and **Mutator** (kill surviving mutants, delete dead code).

The practice phase covers keeping a log, guarding the context window, worktree cleanup, and small ordered commits.

#### Installation

Copy `SKILL.md` into your agent's skills directory as `ub-mode/SKILL.md`, then invoke `/ub-mode`:

```bash
mkdir -p ~/.hermes/skills/ub-mode
curl -fsSL https://raw.githubusercontent.com/unclebob/ub-mode/master/SKILL.md \
  -o ~/.hermes/skills/ub-mode/SKILL.md
```

Equivalent paths for other tools: `~/.claude/skills/ub-mode/SKILL.md`, `~/.cursor/skills/ub-mode/SKILL.md`, `~/.grok/skills/ub-mode/SKILL.md`.

#### Companion tools

| Tool | Gate it enforces |
|------|------------------|
| [crapper](https://github.com/unclebob/crapper) | Cyclomatic complexity, coverage and CRAP score per function (`CRAP < 10`) |
| [dryer](https://github.com/unclebob/dryer) | Structural duplication (fails at `>= 0.8` similarity) |
| [mutator](https://github.com/unclebob/mutator) | Mutation testing: uncovered code and surviving mutants |
| [uml-viewer](https://github.com/unclebob/uml-viewer) | Components, coverage, CRAP, mutation score and dependency direction |

#### Typical usage

```
/ub-mode
```

Then make the request as usual. The skill applies the three phases to the change and stops at the gate that fails.

---

## 4. Per-project setup checklist

```
[ ] Copy CONSTITUTION.md to the project root
[ ] Add the CONSTITUTION.md read instruction to your project instructions mechanism
[ ] Install the Coder primary agent for OpenCode (see section 2)
[ ] Install the plugins, tools, skills, and MCPs you want to use (see section 3)
```

### Suggested stack

```
[ ] Install Coder primary agent for OpenCode
[ ] Install Superpowers (spec-driven development + TDD)
[ ] Install @nextlevelbuilder/ui-ux-pro-max-skill (if the project has a UI)
[ ] Install agent-browser (if the project needs browser automation)
[ ] Install Supabase Postgres Best Practices (if the project uses Supabase or Postgres)
[ ] Install Security Guidance
[ ] Install OpenCode-Mem (cross-session memory)
[ ] Install Context7 (up-to-date library/API documentation for LLMs)
[ ] Install DOX (self-documenting AGENTS.md framework for precise project context)
[ ] Install Ponytail (minimal changes and over-engineering review)
[ ] Install code-review-graph (token-efficient code review via local code intelligence graph)
```

---

## 5. References

| Resource | Link |
|----------|------|
| Superpowers | https://github.com/obra/superpowers |
| UI UX Pro Max Skill | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill |
| Supabase Postgres Best Practices | https://github.com/supabase/agent-skills/tree/3e7771598f3a03d29533208dd7b5a50bdfc8860f/skills/supabase-postgres-best-practices |
| Security Guidance Plugin | https://github.com/anthropics/claude-code/tree/main/plugins/security-guidance |
| OpenCode-Mem | https://github.com/tickernelz/opencode-mem |
| Context7 | https://github.com/upstash/context7 |
| DOX | https://github.com/agent0ai/dox |
| Ponytail | https://github.com/DietrichGebert/ponytail |
| agent-browser | https://github.com/vercel-labs/agent-browser |
| code-review-graph | https://github.com/tirth8205/code-review-graph |
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
