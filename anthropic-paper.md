The article ["Harness design for long-running application development"](https://www.anthropic.com/engineering/harness-design-long-running-apps) by [Anthropic](https://www.anthropic.com) describes how the company dramatically improved Claude's ability to autonomously develop complete applications over several consecutive hours, especially for frontend and full-stack engineering tasks. ([Anthropic][1])

## Core idea

The paper argues that the performance of AI agents depends not only on the LLM model itself, but primarily on the **"harness"** — the architecture and orchestration surrounding the model:

* prompts,
* tools,
* memory,
* division of responsibilities,
* state persistence,
* evaluation cycles,
* session handoffs.

The analogy used is:

> the model is the engine; the harness is the car.

In other words, even highly capable models will fail at long-running tasks if the surrounding structure is poor. ([Working Reference][2])

---

# Problems they identified

## 1. Poor self-evaluation

An agent that creates something tends to believe the result is good, even when it is not.

Examples:

* visually weak frontend,
* functional bugs,
* inconsistent UX,
* incomplete features.

Anthropic concluded that:

* having the same agent generate and evaluate produces poor results;
* separating these responsibilities significantly improves quality.

([Anthropic][1])

---

## 2. Context collapse in long-running tasks

In long sessions:

* context grows too large,
* the agent "forgets" its objectives,
* it starts taking shortcuts,
* it silently redefines what "done" means.

They implicitly refer to this as:

* "context anxiety"
* context degradation.

The solution was not simply to summarize context ("compaction"), but to:

* periodically restart sessions,
* use persistent structured artifacts,
* break work into smaller steps.

([Anthropic][3])

---

# Proposed architecture

Anthropic built an architecture inspired by GANs (Generator vs. Discriminator).

It evolved into a three-agent system:

| Agent     | Role                  |
| --------- | --------------------- |
| Planner   | Plans the project     |
| Generator | Implements the code   |
| Evaluator | Tests and critiques   |

([Anthropic][1])

---

# Role of each agent

## Planner

Receives:

* product idea,
* goal,
* requirements.

Produces:

* structured specification,
* feature list,
* milestones,
* completion criteria.

Important:

* it does NOT go deep into implementation details;
* avoids contaminating the Generator with premature wrong decisions.

---

## Generator

Implements:

* frontend,
* backend,
* APIs,
* components,
* integration.

Works incrementally:

* feature by feature,
* sprint by sprint.

Also produces:

* handoff artifacts,
* logs,
* persistent state.

---

## Evaluator

This is the key differentiator.

It:

* runs the application,
* uses a real browser (Playwright),
* interacts with the UI,
* tests behavior,
* evaluates design,
* checks for bugs.

Criteria used:

* visual quality,
* originality,
* functionality,
* craft.

It produces detailed feedback for the Generator to iterate on.

([Anthropic][1])

---

# Key insight: context reset > infinite summarization

One of the most interesting findings:

Anthropic realized that continuously maintaining a massive context degraded performance.

They shifted to:

* ending sessions,
* restarting with a clean context,
* continuing using only structured artifacts.

This worked better than trying to summarize the entire conversation indefinitely.

([TeamDay.ai][4])

---

# Persistent structures

They emphasize the importance of persistent files such as:

* feature lists,
* specs,
* logs,
* checkpoints,
* project state.

This closely resembles:

* `AGENTS.md`
* `TASKS.md`
* `DESIGN.md`
* `MAP.md`

The idea is:

* the agent should never rely solely on the chat's contextual memory;
* the project itself carries the persistent cognitive state.

([Anthropic][3])

---

# Results

According to Anthropic:

## Without a sophisticated harness

* ~20 minutes
* ~$9
* broken application
* incomplete features

## With the Planner + Generator + Evaluator architecture

* up to 6 hours
* ~$200
* fully functional application
* significantly better UX

([TeamDay.ai][4])

---

# Paper conclusions

The article suggests that the future of agents lies not only in:

* larger models,
* giant context windows.

But in:

* harness engineering,
* persistent memory,
* role separation,
* independent evaluation,
* structured artifacts,
* iterative cycles.

Anthropic also notes that as models improve:

* some parts of the harness may simplify,
* but more complex tasks become possible.

([Working Reference][2])

---

# What this means in practice

The paper essentially validates several current trends:

* Claude Code
* OpenCode
* Cursor
* planner/executor agents
* persistent project memory
* `AGENTS.md`
* handoff files
* evaluation loops
* multi-agent execution
* Playwright as an automated evaluator
* long-running agents

And reinforces an important idea:

> "Long-running agents" are not just large prompts.
>
> They are cognitive operating systems built around the model.

[1]: https://www.anthropic.com/engineering/harness-design-long-running-apps "Harness design for long-running application development"
[2]: https://www.working-ref.com/en/reference/anthropic-harness-design-philosophy-evolution "Anthropic's Harness Design Philosophy — From Multi-Agent ..."
[3]: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents "Effective harnesses for long-running agents"
[4]: https://www.teamday.ai/ai/anthropic-harness-design-long-running-apps "Anthropic's GAN-Inspired Harness for Autonomous"
