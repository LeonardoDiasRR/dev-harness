# Correct Source-Derived Agent-Agnostic System Prompt Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Correct `prompts/system-prompt.md` so it preserves every source section and useful operational rule while containing no source-agent, model, manufacturer, runtime, service, path, protocol, or leaked-session coupling.

**Architecture:** Treat `leaks/claude-code-fable-5.md` as the structural and semantic source of truth and `tests/fixtures/system_prompt_transformations.json` as the explicit rename/removal contract. Strengthen `tests/validate_system_prompt.py` before each content batch, then edit the target in source order so every failure becomes a regression check. Keep one prompt artifact and one validator; do not add a generator, runtime, dependency, or parallel prompt implementation.

**Tech Stack:** Markdown, JSON, Python standard library (`json`, `pathlib`, `re`, `unittest`)

---

## File Structure

- Modify: `prompts/system-prompt.md` - replace lexical anonymization with valid semantic abstraction.
- Modify: `tests/fixtures/system_prompt_transformations.json` - record subsection renames, required runtime placeholders, prohibited coupling, and portable concepts that must survive.
- Modify: `tests/validate_system_prompt.py` - validate exact structure, semantic coverage, data removal, placeholders, and absence of proprietary contracts.
- Modify: `README.md` - describe the stronger semantic validation accurately.

The existing `prompts/software-development-system-prompt.md`, `tests/validate_agnostic_prompt.py`, and expanded-prompt fixtures are outside this correction and must not be modified. The already-missing `prompts/agnostic-software-development-system.md` is unrelated user work and must not be restored or deleted by this plan.

### Task 1: Make Structural Fidelity Exact

**Files:**
- Modify: `tests/fixtures/system_prompt_transformations.json`
- Modify: `tests/validate_system_prompt.py`
- Modify: `prompts/system-prompt.md:1-20,983-1006,1745-1749`

- [ ] **Step 1: Extend the transformation fixture for source subheadings**

Add this top-level object after `source_preamble` in `tests/fixtures/system_prompt_transformations.json`:

```json
"subheading_renames": {
  "Rules for use of the EndConversation tool:": "Rules for conversation termination:",
  "Using the EndConversation tool": "Using conversation termination",
  "SendMessage": "Message delivery"
},
```

This records the three level-three headings that still expose source tool names. Do not add an entry for `Global operating rules`; it has no source counterpart and must be removed.

- [ ] **Step 2: Write failing exact-hierarchy tests**

Add a heading parser that preserves level and order:

```python
def heading_tree(text):
    return [
        (len(match.group(1)), match.group(2).strip())
        for match in re.finditer(r"^(#{1,3})\s+(.+?)\s*$", text, re.MULTILINE)
    ]
```

Add these tests to `SystemPromptTransformationTests`:

```python
    def test_target_has_no_unmapped_headings(self):
        section_renames = {
            row["source_heading"]: row["target_heading"]
            for row in self.mapping["sections"]
        }
        subsection_renames = self.mapping["subheading_renames"]
        expected = []
        for level, title in heading_tree(self.source):
            if level <= 2:
                title = section_renames.get(title, title)
            else:
                title = subsection_renames.get(title, title)
            expected.append((level, title))
        self.assertEqual(heading_tree(self.prompt), expected)

    def test_target_preserves_source_heading_count(self):
        self.assertEqual(len(heading_tree(self.source)), 99)
        self.assertEqual(len(heading_tree(self.prompt)), 99)
```

- [ ] **Step 3: Run the tests and observe the structural failure**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"; python -m unittest tests/validate_system_prompt.py -v
```

Expected: failure showing the extra `Global operating rules` heading and the three unmapped source-specific subheadings.

- [ ] **Step 4: Restore exact structural correspondence**

Delete `## Global operating rules` and its five bullets from `prompts/system-prompt.md:9-15`. Do not discard those concepts blindly: the source already contains their narrower equivalents in authorization, context, Git, failure, and completion sections; preserve those original locations.

Rename:

```markdown
### Rules for conversation termination:
### Using conversation termination
### Message delivery
```

- [ ] **Step 5: Verify exact hierarchy**

Run the same unittest command. Expected: both new structural tests pass with 99 source and 99 target headings in identical hierarchy and order after mapped renames.

### Task 2: Detect All Known Leakage and Mechanical-Replacement Defects

**Files:**
- Modify: `tests/fixtures/system_prompt_transformations.json`
- Modify: `tests/validate_system_prompt.py`

- [ ] **Step 1: Add explicit prohibited-coupling patterns to the fixture**

Add this top-level array:

```json
"prohibited_target_patterns": [
  "(?i)\\bthe agent(?:-code-guide|-api| agent sdk| tag| design)\\b",
  "(?i)\\bthe host agent\\b",
  "(?i)\\bFleetView\\b",
  "client\\.beta\\.messages\\.tool_runner",
  "window\\.the agent",
  "(?:^|[/~])\\.the agent(?:/|$)",
  "(?i)/install-slack-app",
  "(?i)\\bultracode\\b",
  "<<autonomous-loop(?:-dynamic)?>>",
  "(?i)(?:^|[^a-z])/workflows\\b",
  "(?i)(?:^|[^a-z])/loop\\b",
  "(?i)\\b(?:CronCreate|ScheduleWakeup|AskUserQuestion|EnterPlanMode|ExitPlanMode|EnterWorktree|ExitWorktree|EndConversation|SendMessage|WaitForMcpServers)\\b",
  "(?i)\\b(?:Read|Write|Edit|Monitor|Artifact|Workflow|Skill|Agent|TaskStop|TaskGet|TaskList|TaskUpdate) tool\\b",
  "(?i)\\bJuly 2026\\b",
  "(?i)\\bUS-only\\b",
  "/v1/code/triggers",
  "(?i)\\b1-hour provider prompt-cache TTL\\b",
  "(?i)\\b5-minute TTL\\b"
],
```

These patterns intentionally target source contracts and malformed replacements, not ordinary generic uses of words such as “agent,” “read,” or “workflow.”

- [ ] **Step 2: Add concrete session-data patterns**

Add:

```json
"prohibited_session_patterns": [
  "(?m)^\\s*[MADRU?]{1,2}\\s+src/",
  "(?m)^\\s*[MADRU?]{1,2}\\s+README\\.md$",
  "(?m)^\\s*R\\s+config\\.yaml -> config/settings\\.yaml$",
  "(?m)^\\s*\\?\\?\\s+(?:notes\\.txt|\\.env\\.local)$",
  "(?i)\\bDarwin 25\\.5\\.0\\b",
  "(?i)/Users/asgeirtj/",
  "(?i)asgeirtj@gmail\\.com",
  "(?i)\\b2026-07-16\\b"
],
```

- [ ] **Step 3: Write failing scanner tests**

Add:

```python
    def assert_no_patterns(self, key):
        matches = {
            pattern: re.findall(pattern, self.prompt)
            for pattern in self.mapping[key]
            if re.search(pattern, self.prompt)
        }
        self.assertFalse(matches, f"prohibited target content: {matches}")

    def test_target_has_no_source_runtime_coupling(self):
        self.assert_no_patterns("prohibited_target_patterns")

    def test_target_has_no_concrete_session_data(self):
        self.assert_no_patterns("prohibited_session_patterns")
```

- [ ] **Step 4: Run the tests and capture failures before editing content**

Run the validator. Expected: failures for malformed `.the agent` paths, pseudo-product names, source tool references, workflow/wake-up sentinels, date/region/runtime values, and concrete Git paths.

### Task 3: Correct Identity, Environment, Session Context, Agents, and Procedures

**Files:**
- Modify: `prompts/system-prompt.md:1-197`
- Modify: `tests/fixtures/system_prompt_transformations.json`
- Test: `tests/validate_system_prompt.py`

- [ ] **Step 1: Add required early-section concepts to the fixture**

Add:

```json
"required_section_concepts": {
  "Environment context": [
    "<project-directory>", "<is-git-repository>", "<platform>", "<shell>",
    "<operating-system-version>", "<model-runtime>", "<knowledge-cutoff>"
  ],
  "Version-control status": [
    "<current-branch>", "<default-branch>", "<git-user>",
    "<working-tree-status>", "<working-tree-details>", "<recent-commits>"
  ],
  "Project instructions": [
    "global user instructions", "all projects", "project instructions",
    "checked into the codebase", "<global-instructions>", "<project-instructions>"
  ],
  "User context": ["email address", "<user-email>"],
  "Current date and time": ["<current-date>"],
  "Auxiliary agents": ["host-exposed agent types", "available capabilities"],
  "Reusable procedures": ["host-exposed procedures", "do not invent procedure names"]
}
```

- [ ] **Step 2: Add a reusable section extractor and concept test**

```python
def section_body(text, heading):
    match = re.search(rf"^([#]{{1,2}})\s+{re.escape(heading)}\s*$", text, re.MULTILINE)
    if not match:
        return ""
    level = len(match.group(1))
    tail = text[match.end():]
    end = re.search(rf"^#{{1,{level}}}\s+", tail, re.MULTILINE)
    return tail[:end.start()] if end else tail


    def test_required_portable_concepts_survive(self):
        missing = {}
        for heading, concepts in self.mapping["required_section_concepts"].items():
            body = section_body(self.prompt, heading).lower()
            absent = [concept for concept in concepts if concept.lower() not in body]
            if absent:
                missing[heading] = absent
        self.assertFalse(missing, f"missing portable concepts: {missing}")
```

- [ ] **Step 3: Replace leaked context and preserve provenance**

In `Version-control status`, replace lines containing individual files with exactly:

```markdown
Status: `<working-tree-status>`
`<working-tree-details>`

Recent commits: `<recent-commits>`
```

In `Project instructions`, restore the source distinctions without product filenames:

```markdown
Contents of `<global-instructions-file>` (the user's private global user instructions for all projects):

Contents of `<project-instructions-file>` (project instructions checked into the codebase):
```

In `User context`, use:

```markdown
The user's email address is `<user-email>`.
```

- [ ] **Step 4: Replace catalog snapshots with capability-shaped runtime context**

The source catalogs are session snapshots, not universal built-ins. Preserve their role and decision rules using this structure:

```markdown
# Auxiliary agents

Available host-exposed agent types are listed in `<available-agent-types>`. Each entry provides its purpose and available capabilities.

- Use the most specific available type whose declared purpose matches the task.
- Use the general-purpose type only when no specialized type fits.
- Use a read-only exploration type for broad repository searches that require conclusions rather than file dumps.
- Before continuing a named auxiliary agent, check whether an existing session can be resumed.
- Never invent an agent type, capability, model override, or registry entry.

# Reusable procedures

Available host-exposed procedures are listed in `<available-procedures>` with their trigger descriptions.

- Load a procedure before acting when the task matches its declared trigger.
- Use only procedures exposed by trusted host or project context.
- Do not invent procedure names, slash commands, configuration paths, or installation commands.
- If a procedure is unavailable, state the limitation and use a known safe alternative only when it preserves scope.
```

This removes `FleetView`, SDK methods, Slack installation commands, malformed paths, and pseudo-product names while preserving catalog selection behavior.

- [ ] **Step 5: Preserve portable model/runtime behavior without model identity**

Keep environment fields as placeholders. Express the source's portable guidance as:

```markdown
- Model identity and identifiers are supplied through `<model-runtime>`; do not hard-code a provider or model family.
- When building model-backed applications and no project requirement selects a model, use the latest capable model exposed by the configured provider.
- If the host exposes a fast-output mode, treat it as an execution mode rather than assuming it selects a smaller model.
```

- [ ] **Step 6: Run the validator**

Expected: early-section concept tests pass; remaining leakage failures are limited to later capability sections.

### Task 4: Abstract Core Capability Contracts Through Isolated Workspaces

**Files:**
- Modify: `prompts/system-prompt.md:199-1291`
- Modify: `tests/fixtures/system_prompt_transformations.json`
- Test: `tests/validate_system_prompt.py`

- [ ] **Step 1: Add cross-reference vocabulary rules**

Add to the fixture:

```json
"abstract_capability_terms": {
  "Agent delegation": "agent-delegation capability",
  "Artifact generation and publication": "artifact capability",
  "User questions and approvals": "structured-question capability",
  "Command execution": "command-execution capability",
  "Schedule creation": "schedule-creation capability",
  "Schedule deletion": "schedule-deletion capability",
  "Schedule listing": "schedule-listing capability",
  "Design-system synchronization": "design-synchronization capability",
  "Exact file editing": "file-editing capability",
  "Conversation termination": "conversation-termination capability",
  "Planning-mode entry": "planning capability",
  "Isolated-workspace entry": "isolated-workspace capability",
  "Planning-mode exit": "planning handoff",
  "Isolated-workspace exit": "isolated-workspace cleanup"
}
```

- [ ] **Step 2: Add a capability-term test**

```python
    def test_abstract_capability_sections_name_their_contract(self):
        missing = {}
        for heading, term in self.mapping["abstract_capability_terms"].items():
            body = section_body(self.prompt, heading).lower()
            if term.lower() not in body:
                missing[heading] = term
        self.assertFalse(missing, f"missing abstract capability terms: {missing}")
```

- [ ] **Step 3: Generalize all named cross-references in this range**

Apply these semantic conversions consistently in prose and examples:

| Source reference | Portable replacement |
|---|---|
| `Agent` | agent-delegation capability |
| `SendMessage` | agent-messaging capability |
| `Artifact` | artifact capability |
| `AskUserQuestion` | structured-question capability |
| `Bash` | command-execution capability |
| `Monitor` | process-monitoring capability |
| `CronCreate` / `CronDelete` / `CronList` | schedule creation/deletion/listing operation |
| `Read` / `Edit` / `Write` | file-reading/editing/writing capability |
| `EnterPlanMode` / `ExitPlanMode` | planning entry/handoff capability |
| `EnterWorktree` / `ExitWorktree` | isolated-workspace entry/cleanup capability |
| `.claude/...`-style paths | `<host-config-directory>/...` or `<isolated-workspace-root>/...` |
| hosted artifact/design URLs | `<artifact-service-url>` / `<design-service-url>` |

Do not rename ordinary verbs inside examples. Rename only tool/API references and schema descriptions.

- [ ] **Step 4: Remove dangling attribution rules**

Delete both empty lines at current `prompts/system-prompt.md:535-536`:

```markdown
- End git commit messages with:
- End PR bodies with:
```

They were source-only attribution requirements and have no portable equivalent.

- [ ] **Step 5: Generalize schemas without inventing host enums**

For provider-specific model overrides, replace invented enum values such as `standard`, `advanced`, `compact`, and `the configured model` with a host-provided string contract:

```json
"model": {
  "description": "Optional host-exposed model identifier. Omit it to inherit the current runtime model.",
  "type": "string"
}
```

For proprietary service identifiers and URLs, keep string type, requiredness, limits, and operation semantics, but rename descriptions to `<service-id>` or `<service-url>` concepts. Preserve security and conflict behavior.

- [ ] **Step 6: Verify the corrected first capability range**

Run the validator. Expected: no prohibited patterns from lines 199-1291 and all abstract capability-term tests pass.

### Task 5: Abstract Monitoring, Files, Remote Work, Messaging, and Task Lifecycle

**Files:**
- Modify: `prompts/system-prompt.md:1294-2196`
- Modify: `tests/fixtures/system_prompt_transformations.json`
- Test: `tests/validate_system_prompt.py`

- [ ] **Step 1: Extend abstract capability terms for the second range**

Add these entries to `abstract_capability_terms`:

```json
"Process monitoring": "process-monitoring capability",
"Notebook editing": "notebook-editing capability",
"User notification": "notification capability",
"File and resource reading": "file-reading capability",
"Remote trigger": "remote-trigger capability",
"Findings reporting": "findings-reporting capability",
"Scheduled wake-up": "scheduled-wake-up capability",
"Agent messaging": "agent-messaging capability",
"Procedure loading": "procedure-loading capability",
"Task creation": "task-management capability",
"Task retrieval": "task-management capability",
"Task listing": "task-management capability",
"Task output retrieval": "task-management capability",
"Task stopping": "task-management capability",
"Task updating": "task-management capability"
```

- [ ] **Step 2: Generalize monitoring and file operations**

Preserve event streaming, buffering, terminal-state coverage, WebSocket behavior, timeout, cancellation, pre-read, exact cell editing, ranged reads, PDF limits, notebook handling, and post-write guarantees. Replace named tools with the abstract terms from the fixture.

Replace source-host delivery assumptions such as terminal-to-phone “Remote Control” with:

```markdown
If the host exposes an out-of-band notification channel, use it only for events the user would act on immediately. A skipped or unavailable delivery is not an operation failure; report it accurately.
```

- [ ] **Step 3: Generalize remote trigger transport**

Remove fixed `/v1/code/triggers` endpoints and HTTP method paths. Preserve the five operations as abstract actions:

```markdown
Supported operations are list, get, create, update, and run. The host adapter supplies transport, authentication, service identifiers, and URLs. Never expose credentials or infer an endpoint.
```

Keep the schema's action enum, identifier pattern, body requirements, and partial-update semantics.

- [ ] **Step 4: Generalize scheduled wake-up**

Replace `/loop`, sentinels, `CronCreate`, named wake-up calls, cache TTLs, telemetry, and fixed provider limits with:

```markdown
Use the scheduled-wake-up capability only when the user has requested iterative autonomous work and the host exposes resumable scheduling.

- Pass the original iteration goal as the resume payload.
- Use a host-provided autonomous payload marker only when the host documents one; never invent it.
- Stop by cancelling the next wake-up through the same capability.
- Match delays to the external state being observed. Prefer event-driven completion for host-tracked work and use a bounded fallback only for missed notifications.
- Read minimum, maximum, cache, and persistence limits from runtime context rather than hard-coding them.
```

Change schema descriptions to host-defined timing limits while preserving `delay`, `reason`, `payload`, and `stop` semantics.

- [ ] **Step 5: Generalize messaging, procedures, and task internals**

Preserve recipient, summary, message, procedure discovery, task states, dependencies, blocking, stale-task behavior, output retrieval, cancellation, and completion evidence. Remove fixed recipients, raw agent-ID formats, `.output` symlink details, JSONL transcript assumptions, `/tasks`, `local_agent`, `remote_agent`, and agent-team `name@team` conventions.

Use:

```markdown
Recipients and task identifiers are opaque host-provided values. Do not infer their format. Background output may be returned directly or through a host-provided handle; use the documented retrieval capability and do not inspect internal transcript storage.
```

- [ ] **Step 6: Run the validator**

Expected: no named runtime APIs or malformed paths remain through `Task updating`; portable state and lifecycle rules remain present.

### Task 6: Abstract External Readiness, Web Capabilities, and Workflow Execution

**Files:**
- Modify: `prompts/system-prompt.md:2199-2515`
- Modify: `tests/fixtures/system_prompt_transformations.json`
- Test: `tests/validate_system_prompt.py`

- [ ] **Step 1: Extend abstract terms for the final range**

Add:

```json
"External capability readiness": "external-capability readiness operation",
"Web retrieval": "web-retrieval capability",
"Web search": "web-search capability",
"Workflow execution": "workflow-execution capability"
```

- [ ] **Step 2: Generalize external readiness**

Replace MCP-specific server and tool-list language with pending external capability providers. Preserve specific-provider selection, wait-all behavior, `ready=true/false`, authentication-required, connection failure, and disabled outcomes. Keep `servers` only as an abstract provider-name array or rename it consistently to `providers` in both properties and required lists.

- [ ] **Step 3: Correct web retrieval and search runtime assumptions**

Replace the artifact exception with:

```markdown
Authenticated or private URLs require a host-exposed authenticated retrieval capability. Do not assume that generic retrieval carries credentials, follows login redirects, or can access a particular artifact service.
```

Remove `gh`, `WebFetch`, SPA-shell, Cloudflare, fixed 15-minute caching, “US-only,” and “July 2026.” Preserve HTTPS preference, redirect handling, domain filters, current-date use through `<current-date>`, and source-link reporting.

- [ ] **Step 4: Separate portable workflow semantics from source runtime mechanics**

Retain:

- explicit user opt-in for expensive multi-agent orchestration;
- scoped fan-out and hybrid inline/workflow discovery;
- pipeline versus barrier semantics;
- structured metadata and arguments;
- deterministic stages, error isolation, budgets, concurrency limits supplied by the host;
- adversarial verification, diverse perspectives, loop-until-dry, completeness review;
- resumability when the host supplies run and transcript handles.

Remove or generalize:

- `/workflows`, `ultracode`, system-reminder activation names;
- `Workflow`, `Agent`, `Skill`, `ToolSearch`, `TaskStop`, `Write/Edit` tool names;
- `+500k` directives and fixed 16/1000/4096 limits;
- fixed session directories, journals, run-ID patterns, internal cache behavior;
- `.the agent/workflows/`, `<transcriptDir>`, and source-specific function signatures.

Use abstract script hooks named `delegate`, `pipeline`, `parallel`, `phase`, and `report_progress`. State explicitly that exact hook names and schemas are supplied by the host adapter; examples are conceptual, not mandatory APIs.

- [ ] **Step 5: Add final-range portable concept checks**

Add to `required_section_concepts`:

```json
"External capability readiness": ["ready", "authentication", "failed", "disabled"],
"Web retrieval": ["authenticated retrieval", "redirect", "https", "private urls"],
"Web search": ["<current-date>", "allowed domains", "blocked domains", "sources"],
"Workflow execution": ["explicit opt-in", "pipeline", "barrier", "verification", "resume", "host-provided limits"]
```

- [ ] **Step 6: Run the validator**

Expected: all structural, prohibited-pattern, abstract-term, session-data, and semantic-concept tests pass.

### Task 7: Validate Full Semantic Fidelity and Documentation

**Files:**
- Modify: `tests/validate_system_prompt.py`
- Modify: `README.md`
- Test: `prompts/system-prompt.md`

- [ ] **Step 1: Add assertions for known accidental omissions and malformed placeholders**

Add:

```python
    def test_no_dangling_attribution_directives(self):
        self.assertNotIn("End git commit messages with:", self.prompt)
        self.assertNotIn("End PR bodies with:", self.prompt)

    def test_runtime_placeholders_use_lower_kebab_case(self):
        known_bad = ("<transcriptDir>", "<task-notification>", "<project-dir>", "<scratchpad-dir>")
        found = [value for value in known_bad if value in self.prompt]
        self.assertFalse(found, f"non-canonical runtime placeholders: {found}")

    def test_target_contains_no_mechanical_replacement_artifacts(self):
        artifacts = ("the the ", "a the agent", "this the agent", ".the agent", "the agent-")
        found = [value for value in artifacts if value in self.prompt_lower]
        self.assertFalse(found, f"mechanical replacement artifacts: {found}")
```

- [ ] **Step 2: Run both available validators independently**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"; python -m unittest tests/validate_system_prompt.py -v
```

Expected: all source-derived prompt tests pass.

Run the existing expanded-prompt validator only if its target file exists:

```powershell
if (Test-Path -LiteralPath "prompts/agnostic-software-development-system.md") {
  python -m unittest tests/validate_agnostic_prompt.py -v
} else {
  "Skipped existing expanded-prompt validator: its unrelated target file is absent."
}
```

Expected in the current worktree: an explicit skip message, not a false claim that the unrelated suite passed.

- [ ] **Step 3: Perform deterministic final scans**

Run:

```powershell
git diff --check
rg -n -i "claude|anthropic|fable|mythos|opus|sonnet|haiku|asgeirtj|@gmail\.com|claude\.ai|FleetView|the agent|\.the agent|ultracode|autonomous-loop|July 2026|US-only" prompts/system-prompt.md
```

Expected: `git diff --check` has no errors and the prohibited scan returns no matches.

- [ ] **Step 4: Conduct a manual section-by-section semantic review**

Use `tests/fixtures/system_prompt_transformations.json` as the checklist and compare every one of the 49 mapped top-level source boundaries plus all 49 source subsections. For each boundary, confirm:

1. same relative order and heading level;
2. mapped generic title;
3. useful procedure, constraints, state distinctions, limits, examples, and schema semantics preserved;
4. no source-agent, model, manufacturer, service, path, runtime, or session value remains;
5. no new rule was introduced unless it is the direct portable restatement of a source rule.

If a section fails any item, correct it and rerun the validator before continuing. Do not produce a separate generated comparison artifact; the fixture and tests are the durable audit record.

- [ ] **Step 5: Update README validation wording**

Replace the current short validator description with:

```markdown
The validator checks exact source-to-target heading hierarchy, transformation-map coverage, portable concept preservation, runtime placeholders, session-data removal, malformed replacement artifacts, and prohibited source-specific tool, service, model, path, protocol, and environment coupling.
```

- [ ] **Step 6: Inspect only intended changes**

Run:

```powershell
git status --short
git diff -- prompts/system-prompt.md tests/fixtures/system_prompt_transformations.json tests/validate_system_prompt.py README.md
```

Expected: only the four planned files are part of this correction. Existing unrelated worktree changes remain untouched.

## Plan Self-Review

- Spec coverage: Task 1 restores exact 99-heading structure. Tasks 2 and 7 strengthen regression detection. Tasks 3-6 cover every source range and every audit finding. Task 7 verifies semantic parity and updates documentation.
- Audit coverage: concrete Git data, malformed paths and JavaScript identifiers, pseudo-product names, source capability references, model behavior, attribution remnants, instruction provenance, user-email structure, design integration, wake-up/cache policy, monitoring, remote triggers, task internals, external readiness, web date/region assumptions, workflow internals, and noncanonical placeholders all have explicit correction steps.
- Scope: no generator, runtime, dependency, second prompt, or unrelated restoration is introduced.
- Git policy: this plan contains no commit, push, merge, or branch-modification step because the user requested a plan and did not authorize repository publication actions.
