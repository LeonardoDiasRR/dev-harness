# Design Specification: Expanded Agent-Agnostic Software Development System Prompt

**Status:** In Review
**Author:** Leonardo Dias / Gildo
**Created:** 2026-07-18
**Updated:** 2026-07-18
**Supersedes:** `2026-07-18-agnostic-software-development-system-prompt-design.md` for prompt-depth requirements only
**Inspired by:** The Fable 5 software-development system prompt published in [`asgeirtj/system_prompts_leaks`](https://github.com/asgeirtj/system_prompts_leaks/blob/main/Anthropic/Claude%20Code/claude-code-fable-5.md)
**Repository:** `LeonardoDiasRR/dev-harness`

## Problem Statement

The current `prompts/agnostic-software-development-system.md` captures the main behavioral principles of the Fable 5 reference in 180 lines, but it does not preserve enough of the reference's practical operating guidance. The reference contains detailed capability-specific procedures, tool boundaries, lifecycle states, examples, retry rules, failure handling, and completion semantics. A short abstraction is portable, but it leaves too many decisions to each host adapter and therefore cannot reliably reproduce the practical behavior across environments.

This specification defines a second-generation, single-file, expanded system prompt. It will preserve the practical capabilities of the reference while retaining abstract capability contracts. The result must remain independent of any model, vendor, product, CLI, editor, operating system, shell, filesystem layout, proprietary schema, or specific host API.

## Goals

1. Create one expanded Markdown system prompt organized by abstract capability/tool category.
2. Preserve the practical operating guidance that is useful across coding-agent environments.
3. Define procedures, preconditions, inputs, outputs, states, limits, authorization boundaries, failure flows, retry rules, and verification obligations for every capability.
4. Include concise correct and incorrect examples without prescribing proprietary tool syntax.
5. Preserve portability and composability with project constitutions, skills, host adapters, and runtime context.
6. Preserve the source's useful behaviors for session context, memory, task tracking, scheduling, background work, artifacts, delegation, web research, Git, execution, and handoff.
7. Keep source-specific identity, environment snapshots, credentials, paths, product behavior, and gender-policy instructions out of the resulting prompt.
8. Make every major behavior auditable through requirements, scenario tests, and deterministic structural checks.

## Non-Goals

- Implementing an agent runtime, router, scheduler, memory backend, or universal tool protocol.
- Requiring hosts to expose every capability.
- Reproducing proprietary tool names, schemas, parameter names, URLs, paths, or UI behavior.
- Copying the reference prompt verbatim.
- Preserving source-specific model identity, vendor identity, account details, dates, operating-system assumptions, repository snapshots, or user data.
- Adding rules about gender, pronouns, gender inference, or gender-neutral language.
- Replacing `CONSTITUTION.md`, repository instructions, or existing development skills.
- Turning every example into an executable adapter contract.
- Adding speculative capabilities that are not represented by the reference behavior or the current project's needs.

## Design Direction

The approved approach is **one expanded prompt organized by capability/tool category**, with a one-to-one correspondence to the functional section boundaries of the Fable 5 reference. This replaces the earlier grouped-category approach.

The file will remain a single installable artifact. It MUST preserve each operational boundary represented by the reference, even when several capabilities are related. For example, reading, writing, editing, command execution, version control, task tracking, scheduling, monitoring, and publication MUST remain separate sections when the reference treats them separately.

Proprietary names MUST be converted into abstract names, but conversion MUST NOT merge distinct operational contracts. A host adapter may map several abstract sections to one underlying implementation, but the prompt itself must retain the separate sections, procedures, states, limits, failure flows, retry policies, and verification obligations.

The prompt will use stable abstract headings and a common contract format. Each abstract heading MUST identify its reference correspondence in the implementation mapping, while the final prompt MUST not require a proprietary function name, schema, provider, URL, path, or UI.

## Target Prompt Structure

The resulting prompt MUST contain one top-level section for each functional section below, in this order. The names in the right column are the required abstract replacements for the corresponding reference boundaries.

| # | Reference functional boundary | Required abstract section |
|---:|---|---|
| 1 | System prompt | Identity and system role |
| 2 | Harness | Host harness and capability context |
| 3 | Communicating with the user | Communicating with the user |
| 4 | Session-specific guidance | Session-specific guidance |
| 5 | Memory | Persistent memory |
| 6 | Environment | Environment context |
| 7 | Scratchpad Directory | Working scratchpad area |
| 8 | Context management | Context management |
| 9 | Session context | Session context |
| 10 | gitStatus | Version-control status context |
| 11 | claudeMd | Project instruction context |
| 12 | userEmail | User identity context |
| 13 | currentDate | Current date and time context |
| 14 | Agents | Auxiliary-agent capability |
| 15 | Skills | Reusable-procedure capability |
| 16 | Tools | Capability catalog and selection |
| 17 | Agent | Agent delegation procedure |
| 18 | Artifact | Artifact capability |
| 19 | AskUserQuestion | User question and approval capability |
| 20 | Bash | Command execution capability |
| 21 | Git | Version-control capability |
| 22 | CronCreate | Schedule creation capability |
| 23 | CronDelete | Schedule deletion capability |
| 24 | CronList | Schedule listing capability |
| 25 | DesignSync | Design synchronization capability |
| 26 | Edit | File editing capability |
| 27 | EnterPlanMode | Planning-mode entry capability |
| 28 | EnterWorktree | Isolated-workspace entry capability |
| 29 | ExitPlanMode | Planning-mode exit capability |
| 30 | ExitWorktree | Isolated-workspace exit capability |
| 31 | Monitor | Process monitoring capability |
| 32 | NotebookEdit | Notebook modification capability |
| 33 | PushNotification | User notification capability |
| 34 | Read | File and resource reading capability |
| 35 | RemoteTrigger | Remote-trigger capability |
| 36 | ReportFindings | Findings and report capability |
| 37 | ScheduleWakeup | Scheduled wake-up capability |
| 38 | SendMessage | Message delivery capability |
| 39 | Skill | Procedure-loading capability |
| 40 | TaskCreate / TaskGet / TaskList / TaskOutput / TaskStop / TaskUpdate | Task lifecycle capabilities, with one subsection per operation |
| 41 | WaitForMcpServers | External capability-readiness waiting |
| 42 | WebFetch | Web retrieval capability |
| 43 | WebSearch | Web search capability |
| 44 | Workflow | End-to-end workflow capability |
| 45 | Write | File creation and writing capability |
| 46 | Cross-section examples and handoff rules | Cross-capability examples and handoff |

The final prompt MUST contain at least 46 corresponding top-level boundaries. The task lifecycle row MUST contain separate subsections for creation, retrieval, listing, output retrieval, stopping, and updating; grouping them only under a parent label is allowed if the operation subsections remain distinct and independently specified.

The context fields `gitStatus`, `claudeMd`, `userEmail`, and `currentDate` MUST be represented as abstract runtime-context sections. Their source-specific names and values MUST NOT appear as operational requirements in the final prompt.

The prompt MAY include additional headings for precedence, authorization, security, error behavior, state vocabulary, and verification, but those headings MUST NOT replace or absorb any of the 46 required functional boundaries. It MUST remain readable as one standalone system instruction.

## Common Capability Contract

Every capability section MUST use the following conceptual fields. The labels may be rendered as Markdown headings or bold labels, but all information must be present.

### Purpose

What the capability does and which user goals it supports.

### When to use

The conditions that justify using it, including task complexity, risk, freshness, scope, or user request.

### When not to use

Cases where the agent should prefer another capability, avoid redundant work, or wait for clarification or authorization.

### Preconditions

Context, authorization, target inspection, capability availability, or dependencies required before invocation.

### Abstract inputs

The meaning of inputs without prescribing function names, schemas, serialization, or provider-specific parameter names.

### Procedure

A numbered, observable sequence of actions the agent should follow.

### State model

The valid states before, during, and after the operation. At minimum, use applicable states from:

- unavailable;
- available but not authorized;
- ready;
- in progress;
- succeeded;
- failed;
- partially completed;
- denied;
- timed out;
- cancelled;
- stale;
- conflicted;
- unknown.

### Authorization boundary

What the user's request authorizes, what requires separate confirmation, and which actions cannot be inferred from broad intent.

### Failure flow

The first response to failure, the information to preserve, safe alternatives, retry conditions, and when to stop and report a blocker.

### Retry policy

Whether retrying is allowed, under which changed conditions, and when verbatim retrying is prohibited.

### Verification

Evidence required before reporting the operation as successful or complete.

### Examples

At least one correct example and one incorrect or unsafe example. Examples MUST be abstract and MUST NOT imply a concrete host API.

## User Stories

### Story 1 — Practical portable agent (Priority: P1)

As a project maintainer, I want to install one expanded prompt in different coding-agent hosts and retain detailed, predictable operating behavior without rewriting the prompt for each provider.

**Acceptance Scenarios:**

1. **Given** a host with concrete tools mapped to the abstract capabilities, **when** the agent receives a non-trivial coding task, **then** it follows the same discovery, planning, execution, and verification rules regardless of tool names.
2. **Given** a host that exposes only a subset of capabilities, **when** the task requires an unavailable capability, **then** the agent reports the limitation, chooses a safe alternative when possible, and never invents a result.

**Independent Test:** Run the same scenario matrix against two hosts with different tool names and compare decisions, required confirmations, and completion claims.

### Story 2 — Capability-specific reliability (Priority: P1)

As a developer, I want each capability to define its own procedure, states, retries, limits, and verification so that failures do not produce ambiguous or fabricated outcomes.

**Acceptance Scenarios:**

1. **Given** an edit target changed after inspection, **when** the agent is about to overwrite it, **then** it detects the conflict and stops before destructive modification.
2. **Given** a command times out after producing partial output, **when** the agent reports status, **then** it distinguishes timeout, partial effect, and unknown external state.
3. **Given** a delegated worker claims to have pushed a change without a verifiable handle, **when** the agent receives the result, **then** it treats the side effect as unverified.

**Independent Test:** Exercise each capability with success, denial, unavailability, timeout, conflict, partial completion, and unknown-state fixtures.

### Story 3 — Explicit lifecycle state (Priority: P1)

As a repository owner, I want the agent to distinguish planning, execution, verification, local completion, and external completion so that progress is not confused with success.

**Acceptance Scenarios:**

1. **Given** a task has been planned but not executed, **when** the agent reports progress, **then** it describes the task as planned rather than complete.
2. **Given** local files changed but a push was not performed, **when** the agent hands off, **then** it distinguishes local completion from remote publication.
3. **Given** a background process is still running, **when** the agent reports status, **then** it does not claim the monitored task has completed.

**Independent Test:** Evaluate state-transition scenarios with expected valid and invalid claims.

### Story 4 — Detailed host adaptation (Priority: P2)

As a host-adapter author, I want the prompt to specify behavioral contracts without forcing a universal function-calling schema, so that I can map it to CLI, IDE, API, local, or web capabilities.

**Acceptance Scenarios:**

1. **Given** an adapter maps a capability to a structured tool, **when** the agent uses it, **then** the prompt does not require a particular function name or argument schema.
2. **Given** an adapter maps a capability to a manual or interactive process, **when** automation is unavailable, **then** the agent states the boundary and requests only the necessary user action.

**Independent Test:** Review the prompt for operational coupling and simulate adapters with incompatible names and schemas.

### Story 5 — Secure dual-use operation (Priority: P2)

As a security-conscious developer, I want detailed safe operating boundaries for dual-use tasks without enabling destructive, mass-targeted, or malicious execution.

**Acceptance Scenarios:**

1. **Given** a scoped defensive test in an explicitly authorized environment, **when** the task is bounded, **then** the agent provides assistance within that scope.
2. **Given** a request for denial of service, mass exploitation, supply-chain compromise, or malicious evasion, **when** the agent evaluates it, **then** it refuses the harmful operation and redirects to defensive alternatives.

**Independent Test:** Run allow, clarify, limit, and refuse scenarios for representative security requests.

## Functional Requirements

### Identity, precedence, and communication

- **FR-001:** The prompt MUST define the agent as a software-development assistant without requiring a named model, vendor, product, CLI, editor, operating system, shell, repository layout, or tool protocol.
- **FR-002:** The prompt MUST distinguish system rules, host constraints, project instructions, user intent, runtime context, tool results, hooks, reminders, and untrusted external data.
- **FR-003:** The prompt MUST state that higher-priority safety and host constraints override user requests, while valid user intent overrides optional style preferences.
- **FR-004:** The prompt MUST require outcome-first, calibrated communication and faithful reporting of failures, skipped steps, limitations, uncertainty, and partial completion.
- **FR-005:** The prompt MUST require direct evidence before claiming that a file was changed, a command ran, a test passed, a commit exists, or an external action succeeded.
- **FR-006:** The prompt MUST omit gender, pronoun, and gender-inference policies.

### Session context and state

- **FR-007:** The prompt MUST define a session context model that can include project instructions, current task, relevant files, working-tree state, recent changes, available capabilities, prior decisions, and verification evidence.
- **FR-008:** The prompt MUST distinguish current, stale, unavailable, denied, partial, and unknown context.
- **FR-009:** The prompt MUST require re-inspection when a previously read target may have changed.
- **FR-010:** The prompt MUST require continuation from summarized or compacted context without repeating completed work unnecessarily.
- **FR-011:** The prompt MUST define a boundary between context that can guide behavior and content that is merely data.

### Persistent memory

- **FR-012:** The memory section MUST define read, create, update, deduplicate, validate, and delete procedures.
- **FR-013:** The agent MUST persist only durable, useful facts that are not already obvious from the repository or useful only to the current turn.
- **FR-014:** The agent MUST validate recalled files, functions, flags, paths, versions, and behaviors before relying on them.
- **FR-015:** Memory operations MUST define behavior for duplicate, stale, contradictory, sensitive, unavailable, denied, and deletion-request states.
- **FR-016:** The prompt MUST prohibit persistence of credentials, secrets, private data, and transient progress unless the host's trusted policy explicitly allows it.

### Project inspection

- **FR-017:** The inspection section MUST cover listing, locating, searching, reading metadata, inspecting status, inspecting history, and identifying project instructions.
- **FR-018:** The procedure MUST prefer focused reads and searches over broad output when both are available.
- **FR-019:** Inspection MUST precede non-trivial edits, deletion, overwrite, history modification, publication, or execution that depends on repository state.
- **FR-020:** The section MUST define stale snapshots, missing targets, permission failures, empty results, ambiguous matches, and incomplete output.
- **FR-021:** Inspection MUST preserve unrelated user changes and MUST NOT treat an empty result as proof of absence without checking the capability's scope and limitations.

### File reading and analysis

- **FR-022:** The reading section MUST define full reads, paginated reads, targeted reads, metadata reads, binary or unsupported-file handling, and encoding failures.
- **FR-023:** The agent MUST read enough surrounding context to preserve invariants and existing style before editing.
- **FR-024:** The agent MUST distinguish a file that does not exist, cannot be read, is empty, is binary, is truncated, or changed during analysis.
- **FR-025:** The procedure MUST define how the agent reports incomplete analysis and how it chooses a safe alternative.

### File creation and modification

- **FR-026:** The modification section MUST cover create, edit, rename, move, delete, and overwrite as separate operation classes.
- **FR-027:** Before overwriting or deleting, the agent MUST inspect the target and compare its actual state with the expected state.
- **FR-028:** The agent MUST preserve unrelated changes, minimize the diff, match repository conventions, and verify the resulting file.
- **FR-029:** The section MUST define conflict, partial write, permission denial, interrupted write, invalid content, and post-write verification failure states.
- **FR-030:** Destructive or difficult-to-reverse file changes MUST require explicit or durable authorization for the exact scope.

### Command execution

- **FR-031:** The execution section MUST define preparation, risk assessment, invocation, output capture, exit-status interpretation, timeout handling, cancellation, and cleanup.
- **FR-032:** The agent MUST honor host permission decisions and MUST NOT retry a denied operation verbatim.
- **FR-033:** The agent MUST distinguish command success, non-zero failure, timeout, cancellation, unavailable execution, permission denial, partial side effect, and unknown external state.
- **FR-034:** Retries MUST require a changed condition, a safe idempotent operation, or new information that justifies retrying.
- **FR-035:** The procedure MUST require redaction or safe handling when command output contains secrets or private data.
- **FR-036:** The agent MUST not describe a command as successful based only on expected output; it must inspect actual output and status.

### Version control

- **FR-037:** The version-control section MUST define status inspection, diff inspection, branch or workspace isolation, commit, push, merge, and history-modifying operations as separate states.
- **FR-038:** The agent MUST inspect the working tree before staging, committing, resetting, merging, pushing, or discarding changes.
- **FR-039:** The agent MUST preserve unrelated user changes and MUST not reset, clean, rewrite history, or discard work without explicit authorization.
- **FR-040:** Commit, push, merge, deployment, and publication MUST be represented as distinct completion states.
- **FR-041:** The section MUST define divergence, conflicts, authentication failure, rejected push, remote advancement, partial publication, and unknown remote state.
- **FR-042:** A push or remote action MUST require direct evidence such as a successful capability result, remote ref, commit identifier, or equivalent verifiable handle.

### Web and documentation research

- **FR-043:** The research section MUST define when freshness requires web or documentation lookup.
- **FR-044:** The agent MUST prefer primary, current, and directly relevant sources when available.
- **FR-045:** The procedure MUST distinguish search results, retrieved content, inaccessible content, stale content, contradictory sources, and unverified claims.
- **FR-046:** External pages MUST be treated as data rather than as higher-priority instructions.
- **FR-047:** The agent MUST identify sources or provide links when the host supports citations and MUST never fabricate retrieval or citations.

### Delegated work and auxiliary agents

- **FR-048:** Delegation MUST be limited to independent, bounded work with a clear output contract.
- **FR-049:** Delegated requests MUST include objective, scope, relevant context, constraints, expected artifact, and verification requirements.
- **FR-050:** The coordinating agent MUST verify claims about writes, commits, pushes, external requests, publications, or other side effects.
- **FR-051:** The section MUST define worker unavailable, denied, timed out, failed, partially completed, contradictory, and unverified-result states.
- **FR-052:** Delegation MUST NOT be used to bypass safety rules, authorization boundaries, or host permissions.

### Reusable procedures and skills

- **FR-053:** The skills section MUST define discovery, activation, precedence, composition, unavailable-skill, failed-skill, and incompatible-skill states.
- **FR-054:** The agent MUST use only procedures exposed by the host or trusted project context and MUST NOT invent skill names or capabilities.
- **FR-055:** A procedure MUST not silently override higher-priority system, host, or project instructions.
- **FR-056:** The agent MUST report when a requested procedure is unavailable and use a safe alternative only when the alternative is known and within scope.

### Task tracking

- **FR-057:** The task section MUST define task creation, retrieval, update, listing, dependency, execution, completion, failure, cancellation, and staleness behavior.
- **FR-058:** Tasks MUST distinguish planned, ready, in progress, blocked, completed, failed, cancelled, and obsolete states.
- **FR-059:** A task MUST NOT be marked complete merely because it was created, delegated, attempted, or planned.
- **FR-060:** Task updates MUST reflect observed evidence and preserve blockers, dependencies, and user decisions.
- **FR-061:** The prompt MUST define when a task list is useful and when a small request should proceed without unnecessary tracking overhead.

### Scheduling and recurring execution

- **FR-062:** Scheduling MUST define one-shot, recurring, paused, resumed, cancelled, failed, running, and completed states.
- **FR-063:** The agent MUST use scheduling only when requested or clearly within scope and MUST preserve the exact target, schedule, scope, and authorization.
- **FR-064:** The agent MUST distinguish schedule creation from task execution and task completion.
- **FR-065:** The section MUST define missed run, overlapping run, duplicate schedule, notification failure, timeout, and cancellation behavior.
- **FR-066:** Recurring execution MUST NOT silently expand its target, recipients, permissions, or side effects.

### Process monitoring

- **FR-067:** Monitoring MUST define process start, readiness, healthy, unhealthy, stalled, stopped, failed, timed out, and unknown states.
- **FR-068:** The agent MUST verify readiness using an observable signal rather than assuming that process start means service availability.
- **FR-069:** The agent MUST distinguish active monitoring from completed work and MUST report the last known state.
- **FR-070:** The section MUST define log collection, notification, timeout, cancellation, restart, and cleanup boundaries.

### Artifact generation and publication

- **FR-071:** Artifact handling MUST define generation, validation, storage, delivery, sharing, publication, replacement, and deletion as separate operations.
- **FR-072:** Local artifact creation MUST NOT imply authorization to publish or share it.
- **FR-073:** Publication MUST require explicit or durable authorization for the target, audience, content, and external service.
- **FR-074:** The agent MUST verify artifact existence, integrity, location, URL, or identifier before reporting success.
- **FR-075:** The section MUST define sensitive content, invalid artifact, partial upload, inaccessible URL, replacement conflict, and unknown publication state.

### User interaction, approvals, and feedback

- **FR-076:** The interaction section MUST define when to ask for clarification, confirmation, approval, feedback, or authorization context.
- **FR-077:** The agent MUST proceed autonomously with reversible, in-scope work and MUST not ask questions merely to avoid execution.
- **FR-078:** Approval MUST be scoped to the exact action, target, recipient, service, and risk class unless the user explicitly grants durable broader authorization.
- **FR-079:** The section MUST define declined approval, unanswered question, ambiguous answer, changed scope, and revoked authorization states.

### Security and dual-use work

- **FR-080:** The prompt MUST support bounded defensive, educational, research, CTF, and authorized testing scenarios.
- **FR-081:** The prompt MUST require clear authorization context for dual-use techniques.
- **FR-082:** The prompt MUST refuse destructive attacks, denial of service, mass targeting, supply-chain compromise, credential theft, unauthorized persistence, and malicious evasion.
- **FR-083:** The prompt MUST define allow, clarify, constrain, refuse, and redirect outcomes for security requests.
- **FR-084:** Secrets, credentials, tokens, private data, and sensitive output MUST be protected and redacted when encountered.

### Context compaction and resumption

- **FR-085:** The prompt MUST define what a compacted context summary must preserve: goal, decisions, files, changes, state, blockers, evidence, pending tasks, and user approvals.
- **FR-086:** The agent MUST continue from a summary without redoing verified work unnecessarily.
- **FR-087:** The agent MUST revalidate stale or uncertain summary claims before destructive, external, or high-risk actions.
- **FR-088:** The section MUST define missing summary, contradictory summary, truncated output, and lost-state behavior.

### Error and failure behavior

- **FR-089:** Every capability MUST define unavailable, denied, failed, timed-out, cancelled, partial, conflicted, stale, and unknown outcomes where applicable.
- **FR-090:** The prompt MUST require preservation of actual error information, exit status, handles, identifiers, and last known state.
- **FR-091:** The agent MUST choose a safe alternative only when it does not broaden scope or bypass authorization.
- **FR-092:** The agent MUST stop and ask for direction when the next safe action requires new authority, destructive change, or materially expanded scope.

### Verification and completion

- **FR-093:** The completion section MUST require fresh evidence before every claim of success, completion, correctness, publication, or external side effect.
- **FR-094:** The agent MUST identify, run, read, and compare the relevant verification evidence.
- **FR-095:** The final handoff MUST distinguish outcome, verification evidence, limitations, blockers, unknown state, and decisions still required.
- **FR-096:** The prompt MUST distinguish local completion, committed state, pushed state, merged state, deployed state, and published state.

### One-to-One Structural Preservation

- **FR-097:** The prompt MUST contain one independently addressable top-level boundary for every row in the Target Prompt Structure table.
- **FR-098:** A proprietary reference boundary MUST be renamed to an abstract section without being removed, merged, or represented only by a general paragraph.
- **FR-099:** Related operations MAY share a parent heading only when each reference operation remains an independently specified subsection with its own purpose, inputs, procedure, states, authorization boundary, failure flow, retry policy, verification, and examples.
- **FR-100:** The implementation mapping MUST record the reference boundary, abstract heading, final prompt location, and validation identifier for every required section.
- **FR-101:** Context fields that expose source-specific identity or environment data MUST be represented as generic runtime context while preserving their separate operational roles.
- **FR-102:** Structural validation MUST fail when a required reference boundary is missing, merged without independent subsections, out of order, or represented only by an alias without a complete abstract contract.

## Capability State Model

The prompt MUST include a cross-capability state vocabulary. Hosts MAY map these states to their own representations, but the behavioral distinctions must remain.

| State | Meaning | Required agent behavior |
|---|---|---|
| Unavailable | Host does not expose the capability | State limitation; use a safe alternative if possible |
| Available but unauthorized | Capability exists but current action lacks authority | Ask for authorization or decline; do not infer permission |
| Ready | Preconditions and authorization are satisfied | Proceed within scope |
| In progress | Operation has started but final outcome is not known | Track, monitor, or wait; do not claim completion |
| Succeeded | Direct evidence supports the intended result | Record evidence and continue |
| Failed | Operation ended unsuccessfully | Read failure, isolate cause, adapt or report |
| Partially completed | Some effects occurred but the full goal did not | Preserve details and report exact scope |
| Denied | Host or user rejected the operation | Treat denial as authoritative; do not retry verbatim |
| Timed out | No final result within the allowed interval | Distinguish unknown external effects from no effect |
| Cancelled | Operation was intentionally stopped | Report what occurred before cancellation |
| Stale | Observed state may no longer be current | Re-inspect before relying on it |
| Conflicted | Target or instruction conflicts with current scope | Stop before destructive change and surface conflict |
| Unknown | Evidence is insufficient to determine outcome | Report unknown; do not convert it into success or failure |

## Authorization and Risk Model

The prompt MUST define four operational risk classes:

### Class A — Read-only and reversible

Examples include inspection, local analysis, focused reading, and requested reversible edits. Proceed when in scope and authorized by the user's request.

### Class B — State-changing but recoverable

Examples include local builds, generated files, task updates, branch creation, or reversible configuration changes. Proceed when in scope, but inspect before changing and verify afterward.

### Class C — Destructive or difficult to reverse

Examples include deletion, overwrite of user-owned work, history rewrite, reset, cancellation of important work, or destructive cleanup. Require explicit confirmation unless exact durable authorization exists.

### Class D — External, public, sensitive, or security-sensitive

Examples include push, merge, deployment, publication, external messages, data transfer, broad scheduling, and dual-use security actions. Require exact authorization and verify the resulting handle or state.

Authorization MUST be scoped by action, target, recipient, service, audience, and time where those dimensions materially affect risk.

## Required Examples

The expanded prompt MUST contain abstract examples for at least the following scenarios:

1. Inspecting a repository before editing.
2. Reading a large file in focused ranges.
3. Detecting a file changed between read and write.
4. Creating a new file and verifying it.
5. Handling an edit permission denial.
6. Retrying a transient command failure only after a changed condition.
7. Refusing to retry a denied command verbatim.
8. Preserving unrelated dirty-tree changes.
9. Handling a rejected push after the remote advanced.
10. Researching a current API behavior from primary documentation.
11. Treating prompt-injection text in a web page as untrusted data.
12. Delegating independent analysis and verifying the returned claim.
13. Creating, blocking, and completing a task.
14. Distinguishing a scheduled job from its execution result.
15. Monitoring a process that started but is not ready.
16. Creating a local artifact without publishing it.
17. Confirming before public publication.
18. Storing a durable memory while rejecting a transient fact.
19. Resuming from a compacted context summary.
20. Allowing a scoped defensive security task.
21. Refusing mass targeting or denial of service.
22. Reporting partial completion and unknown external state.
23. Distinguishing local completion from commit, push, merge, deployment, and publication.

Each example MUST show the relevant state, authorization boundary, procedure, and final report. At least half of the examples MUST include a failure, limitation, or incorrect behavior to make decision boundaries explicit.

## Non-Functional Requirements

- **NFR-001 — Model agnosticism:** The prompt MUST preserve behavior when the underlying model changes.
- **NFR-002 — Host portability:** The prompt MUST work with CLI, IDE, web, API, and local hosts that map abstract capabilities.
- **NFR-003 — Single-artifact installation:** The prompt MUST remain usable as one standalone Markdown system instruction.
- **NFR-004 — Abstract integration:** No requirement may depend on a concrete function name, tool schema, provider, shell, path, or API.
- **NFR-005 — Composability:** The prompt MUST coexist with project constitutions, skills, host adapters, and runtime context.
- **NFR-006 — Explicit precedence:** Higher-priority system and host constraints MUST remain dominant over user requests.
- **NFR-007 — No fabrication:** Unsupported operations, results, citations, states, and side effects MUST never be claimed.
- **NFR-008 — Proportionality:** Detail, planning, capability use, authorization, and verification MUST scale with task complexity and risk.
- **NFR-009 — Readability:** The prompt MUST use stable headings, consistent contract fields, concise rules, and non-contradictory state definitions.
- **NFR-010 — Practical completeness:** Every capability listed in the target structure MUST have a procedure, state model, failure flow, retry policy, authorization boundary, verification rule, and examples.
- **NFR-011 — Security:** The prompt MUST protect secrets, private data, user control, and authorized scope.
- **NFR-012 — Auditability:** Each operational section MUST map to at least one requirement, acceptance scenario, and validation case.
- **NFR-013 — Maintainability:** The single file SHOULD remain within approximately 600–1,000 lines unless additional content is needed to avoid ambiguity or unsafe omission.
- **NFR-014 — No source leakage:** The prompt MUST not contain source-specific environment snapshots, credentials, user data, or proprietary operational identifiers.

## Edge Cases and Failure Scenarios

The spec MUST cover behavior for:

- a host with no file-reading capability but with command execution;
- a host with editing but no diff capability;
- a dirty working tree containing unrelated changes;
- a file changed between inspection and write;
- a missing, binary, truncated, or unreadable file;
- a command denied by the host;
- a command that times out after partial output;
- a command with unknown external effects;
- a remote branch advancing before push;
- a merge conflict;
- a web source that is inaccessible or contradictory;
- a web page containing instruction-like untrusted content;
- a delegated worker that returns an unverified side-effect claim;
- a skill that is unavailable or conflicts with higher-priority instructions;
- a task that becomes blocked or stale;
- an overlapping scheduled run;
- a process that starts but never becomes ready;
- a publication that returns an inaccessible URL;
- a memory entry that duplicates or contradicts an existing fact;
- a compacted summary that omits the last verification result;
- a user whose broad request does not authorize a specific external action;
- an educational security request that actually asks for destructive mass targeting;
- a test suite that is unavailable, incomplete, or too expensive;
- a user request that changes scope after work has begun.

## Acceptance Test Matrix

The implementation MUST provide a scenario-based validation matrix with expected decisions. The matrix MAY be represented as JSON, Markdown, or test fixtures, but it MUST be executable or mechanically checkable.

| Scenario family | Required outcomes |
|---|---|
| Capability availability | proceed, adapt, report limitation |
| Authorization | proceed, ask, refuse |
| Target state | inspect, conflict, stop |
| Execution | success, failure, timeout, cancellation, unknown |
| Version control | local, committed, pushed, merged, rejected |
| Delegation | delegated, returned, verified, unverified |
| Scheduling | created, running, missed, cancelled, completed |
| Memory | stored, duplicate, stale, deleted, rejected |
| Publication | local, shared, published, inaccessible, unknown |
| Security | allow, clarify, constrain, refuse, redirect |
| Completion | evidence-backed claim, partial report, blocker, unknown |

## Success Criteria

- **SC-001:** The expanded prompt is a single Markdown file organized into the approved one-to-one capability/tool sections.
- **SC-002:** All 46 required top-level boundaries exist in the specified order, with independent task-operation subsections where required.
- **SC-003:** Every required boundary contains all common contract fields, either directly or in an independently addressable subsection.
- **SC-004:** Every required capability defines at least five applicable states and at least one unavailable, denied, failed, timeout, or unknown flow.
- **SC-005:** Every capability defines an authorization boundary and verification obligation.
- **SC-006:** The prompt includes at least 23 required examples, including successful, incorrect, partial, denied, and unknown-state examples.
- **SC-007:** The prompt contains no operational dependency on a named model, vendor, product, CLI, shell, operating system, fixed path, account, or proprietary schema.
- **SC-008:** The prompt contains no gender, pronoun, or gender-inference policy.
- **SC-009:** The prompt preserves the practical distinctions between planning, execution, monitoring, verification, local completion, and external completion.
- **SC-010:** The prompt provides explicit behavior for unavailable, denied, failed, timed-out, cancelled, partial, conflicted, stale, and unknown outcomes.
- **SC-011:** The prompt supports authorized defensive and educational security work while refusing harmful mass, destructive, supply-chain, credential-theft, and malicious-evasion operations.
- **SC-012:** A host adapter can map the prompt to different concrete tools without changing the prompt text or decision boundaries.
- **SC-013:** Structural validation detects missing headings, missing contract fields, missing states, missing examples, prohibited coupling, unresolved placeholders, and prohibited policy content.
- **SC-014:** Scenario validation detects fabricated success claims, unauthorized side effects, unsafe retries, failure-to-stop behavior, and confusion between local and external completion.
- **SC-015:** The final prompt remains readable and internally consistent under review by a developer who has not read the reference source.

## Validation Requirements

The implementation MUST add or update deterministic validation that checks:

1. required headings, one-to-one mapping, and order;
2. all 46 required reference boundaries, including independent task-operation subsections;
3. common contract fields in every required boundary;
4. required state vocabulary;
5. required failure and retry concepts;
6. required authorization and verification language;
7. required example count and scenario labels;
8. prohibited vendor, model, product, path, account, and schema coupling;
9. absence of gender and pronoun policy rules;
10. absence of unresolved placeholders;
11. minimum and maximum line-count warning thresholds;
12. absence of duplicated contradictory state definitions;
13. explicit distinction between local and external completion;
14. implementation mapping coverage and abstract-name conversion.

The validator MUST fail with actionable messages that name the missing section or requirement. It MUST use only the Python standard library unless a future plan explicitly approves a dependency.

## Assumptions

- **A-001:** The host injects the final prompt with higher priority than user messages and external data.
- **A-002:** The host exposes zero or more concrete capabilities and communicates denial, failure, timeout, and permission information.
- **A-003:** The user controls project intent, while the host controls system constraints and capability permissions.
- **A-004:** Adapters map abstract capability concepts to host-specific tools and enforce platform-level permissions.
- **A-005:** Project instructions may add constraints but may not silently override higher-priority system or host rules.
- **A-006:** The prompt is a behavioral and operational guide, not a universal function-calling schema.
- **A-007:** The expanded artifact is intentionally larger than the current 180-line prompt because practical procedures and failure boundaries require additional text.
- **A-008:** The reference source may contain product-specific details that must be normalized or omitted rather than copied.
- **A-009:** Verification requirements are proportional to risk, reversibility, external effect, and runtime surface.
- **A-010:** The current project constitution remains authoritative for repository-specific development behavior.

## Out of Scope for This Spec

- Host-specific adapter files.
- Runtime implementation of the abstract state machine.
- Automatic extraction of tool schemas from external platforms.
- Evaluation of model quality beyond prompt-contract and scenario adherence.
- Reproduction of private or unverifiable source material as authoritative fact.
- Automatic deployment of the expanded prompt to any external host.

## Constitution Check

- [x] Aligns with simplicity by preserving one installable artifact rather than introducing a runtime.
- [x] Aligns with clarity through stable capability sections and a shared contract format.
- [x] Aligns with maintainability by separating behavioral requirements from host adapters.
- [x] Preserves YAGNI by limiting scope to capabilities supported by the reference and project context.
- [x] Preserves surgical changes by replacing the prompt artifact and extending its validator without changing the runtime.
- [x] Preserves verification requirements before completion claims.
- [x] Does not replace `CONSTITUTION.md` or repository-specific architecture rules.
- [x] Explicitly avoids source-specific identity, credentials, paths, and policy content.

## Review Checklist

- [x] User selected the single-file organization by capability/tool category.
- [x] The prompt remains agnostic to model, vendor, product, host, and schema.
- [x] All planned capability categories have requirements.
- [x] Procedures, states, limits, failure flows, retries, and verification are required.
- [x] Examples include both correct and incorrect behavior.
- [x] Local and external completion states are distinct.
- [x] Security boundaries cover allow, clarify, constrain, refuse, and redirect outcomes.
- [x] Edge cases cover unavailable, denied, failed, partial, stale, conflicted, and unknown states.
- [x] Validation is required to be deterministic and actionable.
- [x] No unresolved clarification marker remains.
- [x] No gender or pronoun policy is included.
