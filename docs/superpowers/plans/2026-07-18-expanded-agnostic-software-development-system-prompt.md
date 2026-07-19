# Expanded Agent-Agnostic Software Development System Prompt Implementation Plan

> **For Hermes:** Use the `subagent-driven-development` skill to implement this plan task-by-task, with a spec-compliance review after each task and a final review before integration.

**Goal:** Replace the compact 180-line prompt with a single expanded, model-agnostic prompt that preserves one-to-one operational boundaries for the 46 functional sections identified in the approved specification.

**Architecture:** Keep one canonical prompt at `prompts/agnostic-software-development-system.md`. Preserve each reference boundary as an independently addressable abstract section; related operations may share a parent only when their child sections retain separate contracts. Store the authoritative 46-row mapping in a machine-readable fixture so the validator can check order, presence, and boundaries without depending on proprietary tool names. Extend validation with structural and scenario-oriented checks using only Python's standard library.

**Tech Stack:** Markdown; Python 3.11+ standard library (`json`, `pathlib`, `re`, `unittest`); Git.

---

## Scope and Non-Goals

- Modify only the canonical prompt, its mapping fixture, its validator, and the minimal README documentation.
- Do not implement a runtime, adapter, universal function-call schema, scheduler, memory backend, or host integration.
- Do not copy proprietary names or schemas into the final prompt. Proprietary names appear only in the mapping fixture/spec as traceability metadata and MUST NOT be operational requirements in the prompt.
- Preserve the existing repository constitution and unrelated README content.
- Preserve the current compact prompt's useful behavior while expanding practical procedures, states, limits, failures, retries, authorization, verification, and examples.
- Keep the prompt as one installable Markdown file.

## Files to Change

| File | Responsibility | Change |
|---|---|---|
| `prompts/agnostic-software-development-system.md` | Canonical expanded system prompt | Replace content |
| `tests/fixtures/expanded_prompt_sections.json` | Authoritative one-to-one section mapping and validation metadata | Create |
| `tests/validate_agnostic_prompt.py` | Structural and contract validator | Replace/extend |
| `README.md` | Documentation and validation command | Modify |
| `docs/superpowers/specs/2026-07-18-expanded-agnostic-software-development-system-prompt-design.md` | Approved requirements | Read only |
| `CONSTITUTION.md` | Repository principles | Read only |

No file in `raw/`, wiki directories, or unrelated project directories may be changed.

## Reference Boundary Mapping

The final prompt MUST contain these abstract section headings in this exact order. The mapping fixture will use the `source_boundary` values for traceability and the `abstract_heading` values to validate the final prompt.

```python
REQUIRED_SECTIONS = [
    ("System prompt", "Identity and system role"),
    ("Harness", "Host harness and capability context"),
    ("Communicating with the user", "Communicating with the user"),
    ("Session-specific guidance", "Session-specific guidance"),
    ("Memory", "Persistent memory"),
    ("Environment", "Environment context"),
    ("Scratchpad Directory", "Working scratchpad area"),
    ("Context management", "Context management"),
    ("Session context", "Session context"),
    ("gitStatus", "Version-control status context"),
    ("claudeMd", "Project instruction context"),
    ("userEmail", "User identity context"),
    ("currentDate", "Current date and time context"),
    ("Agents", "Auxiliary-agent capability"),
    ("Skills", "Reusable-procedure capability"),
    ("Tools", "Capability catalog and selection"),
    ("Agent", "Agent delegation procedure"),
    ("Artifact", "Artifact capability"),
    ("AskUserQuestion", "User question and approval capability"),
    ("Bash", "Command execution capability"),
    ("Git", "Version-control capability"),
    ("CronCreate", "Schedule creation capability"),
    ("CronDelete", "Schedule deletion capability"),
    ("CronList", "Schedule listing capability"),
    ("DesignSync", "Design synchronization capability"),
    ("Edit", "File editing capability"),
    ("EnterPlanMode", "Planning-mode entry capability"),
    ("EnterWorktree", "Isolated-workspace entry capability"),
    ("ExitPlanMode", "Planning-mode exit capability"),
    ("ExitWorktree", "Isolated-workspace exit capability"),
    ("Monitor", "Process monitoring capability"),
    ("NotebookEdit", "Notebook modification capability"),
    ("PushNotification", "User notification capability"),
    ("Read", "File and resource reading capability"),
    ("RemoteTrigger", "Remote-trigger capability"),
    ("ReportFindings", "Findings and report capability"),
    ("ScheduleWakeup", "Scheduled wake-up capability"),
    ("SendMessage", "Message delivery capability"),
    ("Skill", "Procedure-loading capability"),
    ("TaskCreate", "Task creation capability"),
    ("TaskGet", "Task retrieval capability"),
    ("TaskList", "Task listing capability"),
    ("TaskOutput", "Task output retrieval capability"),
    ("TaskStop", "Task stopping capability"),
    ("TaskUpdate", "Task update capability"),
    ("WaitForMcpServers", "External capability-readiness waiting"),
    ("WebFetch", "Web retrieval capability"),
    ("WebSearch", "Web search capability"),
    ("Workflow", "End-to-end workflow capability"),
    ("Write", "File creation and writing capability"),
    ("Cross-section examples and handoff rules", "Cross-capability examples and handoff"),
]
```

The mapping contains 51 rows because the task lifecycle boundary is expanded into six independently addressable operations. The approved spec's “46 boundaries” counts the task operations as one functional row while requiring six child sections. The implementation and validator MUST use this explicit 51-heading representation and MUST document the relationship rather than silently collapse it.

## Common Contract Fields

Every one of the 51 required sections MUST contain these labels, in this order, unless a section needs an additional source-specific subsection after them:

```text
Purpose
When to use
When not to use
Preconditions
Abstract inputs
Procedure
State model
Authorization boundary
Failure flow
Retry policy
Verification
Examples
```

A context-only section may state that its capability is host-provided or unavailable, but it still needs the same fields. No section may be represented only by a paragraph in another section.

## Execution Tasks

### Task 1: Create the one-to-one mapping fixture and red structural validator

**Objective:** Establish an executable contract that fails until the expanded prompt contains all required abstract boundaries and common fields.

**Files:**
- Create: `tests/fixtures/expanded_prompt_sections.json`
- Replace: `tests/validate_agnostic_prompt.py`
- Test target: `prompts/agnostic-software-development-system.md`

**Step 1: Create the mapping fixture**

Write valid JSON with this shape:

```json
{
  "source_reference": "Fable 5 functional section mapping",
  "count_model": {
    "functional_boundaries": 46,
    "task_operation_sections": 6,
    "required_headings": 51
  },
  "common_contract_fields": [
    "Purpose",
    "When to use",
    "When not to use",
    "Preconditions",
    "Abstract inputs",
    "Procedure",
    "State model",
    "Authorization boundary",
    "Failure flow",
    "Retry policy",
    "Verification",
    "Examples"
  ],
  "sections": [
    {"source_boundary": "System prompt", "abstract_heading": "Identity and system role", "kind": "context"},
    {"source_boundary": "Harness", "abstract_heading": "Host harness and capability context", "kind": "context"},
    {"source_boundary": "Communicating with the user", "abstract_heading": "Communicating with the user", "kind": "capability"},
    {"source_boundary": "Session-specific guidance", "abstract_heading": "Session-specific guidance", "kind": "context"},
    {"source_boundary": "Memory", "abstract_heading": "Persistent memory", "kind": "capability"},
    {"source_boundary": "Environment", "abstract_heading": "Environment context", "kind": "context"},
    {"source_boundary": "Scratchpad Directory", "abstract_heading": "Working scratchpad area", "kind": "capability"},
    {"source_boundary": "Context management", "abstract_heading": "Context management", "kind": "capability"},
    {"source_boundary": "Session context", "abstract_heading": "Session context", "kind": "context"},
    {"source_boundary": "gitStatus", "abstract_heading": "Version-control status context", "kind": "context"},
    {"source_boundary": "claudeMd", "abstract_heading": "Project instruction context", "kind": "context"},
    {"source_boundary": "userEmail", "abstract_heading": "User identity context", "kind": "context"},
    {"source_boundary": "currentDate", "abstract_heading": "Current date and time context", "kind": "context"},
    {"source_boundary": "Agents", "abstract_heading": "Auxiliary-agent capability", "kind": "capability"},
    {"source_boundary": "Skills", "abstract_heading": "Reusable-procedure capability", "kind": "capability"},
    {"source_boundary": "Tools", "abstract_heading": "Capability catalog and selection", "kind": "capability"},
    {"source_boundary": "Agent", "abstract_heading": "Agent delegation procedure", "kind": "capability"},
    {"source_boundary": "Artifact", "abstract_heading": "Artifact capability", "kind": "capability"},
    {"source_boundary": "AskUserQuestion", "abstract_heading": "User question and approval capability", "kind": "capability"},
    {"source_boundary": "Bash", "abstract_heading": "Command execution capability", "kind": "capability"},
    {"source_boundary": "Git", "abstract_heading": "Version-control capability", "kind": "capability"},
    {"source_boundary": "CronCreate", "abstract_heading": "Schedule creation capability", "kind": "capability"},
    {"source_boundary": "CronDelete", "abstract_heading": "Schedule deletion capability", "kind": "capability"},
    {"source_boundary": "CronList", "abstract_heading": "Schedule listing capability", "kind": "capability"},
    {"source_boundary": "DesignSync", "abstract_heading": "Design synchronization capability", "kind": "capability"},
    {"source_boundary": "Edit", "abstract_heading": "File editing capability", "kind": "capability"},
    {"source_boundary": "EnterPlanMode", "abstract_heading": "Planning-mode entry capability", "kind": "capability"},
    {"source_boundary": "EnterWorktree", "abstract_heading": "Isolated-workspace entry capability", "kind": "capability"},
    {"source_boundary": "ExitPlanMode", "abstract_heading": "Planning-mode exit capability", "kind": "capability"},
    {"source_boundary": "ExitWorktree", "abstract_heading": "Isolated-workspace exit capability", "kind": "capability"},
    {"source_boundary": "Monitor", "abstract_heading": "Process monitoring capability", "kind": "capability"},
    {"source_boundary": "NotebookEdit", "abstract_heading": "Notebook modification capability", "kind": "capability"},
    {"source_boundary": "PushNotification", "abstract_heading": "User notification capability", "kind": "capability"},
    {"source_boundary": "Read", "abstract_heading": "File and resource reading capability", "kind": "capability"},
    {"source_boundary": "RemoteTrigger", "abstract_heading": "Remote-trigger capability", "kind": "capability"},
    {"source_boundary": "ReportFindings", "abstract_heading": "Findings and report capability", "kind": "capability"},
    {"source_boundary": "ScheduleWakeup", "abstract_heading": "Scheduled wake-up capability", "kind": "capability"},
    {"source_boundary": "SendMessage", "abstract_heading": "Message delivery capability", "kind": "capability"},
    {"source_boundary": "Skill", "abstract_heading": "Procedure-loading capability", "kind": "capability"},
    {"source_boundary": "TaskCreate", "abstract_heading": "Task creation capability", "kind": "capability"},
    {"source_boundary": "TaskGet", "abstract_heading": "Task retrieval capability", "kind": "capability"},
    {"source_boundary": "TaskList", "abstract_heading": "Task listing capability", "kind": "capability"},
    {"source_boundary": "TaskOutput", "abstract_heading": "Task output retrieval capability", "kind": "capability"},
    {"source_boundary": "TaskStop", "abstract_heading": "Task stopping capability", "kind": "capability"},
    {"source_boundary": "TaskUpdate", "abstract_heading": "Task update capability", "kind": "capability"},
    {"source_boundary": "WaitForMcpServers", "abstract_heading": "External capability-readiness waiting", "kind": "capability"},
    {"source_boundary": "WebFetch", "abstract_heading": "Web retrieval capability", "kind": "capability"},
    {"source_boundary": "WebSearch", "abstract_heading": "Web search capability", "kind": "capability"},
    {"source_boundary": "Workflow", "abstract_heading": "End-to-end workflow capability", "kind": "capability"},
    {"source_boundary": "Write", "abstract_heading": "File creation and writing capability", "kind": "capability"},
    {"source_boundary": "Cross-section examples and handoff rules", "abstract_heading": "Cross-capability examples and handoff", "kind": "capability"}
  ]
}
```

- [ ] Verify the JSON parses and contains 51 unique `abstract_heading` values.

Run:

```bash
python3 -m json.tool tests/fixtures/expanded_prompt_sections.json >/dev/null
python3 - <<'PY'
import json
from pathlib import Path
data=json.loads(Path('tests/fixtures/expanded_prompt_sections.json').read_text())
heads=[row['abstract_heading'] for row in data['sections']]
assert len(heads) == 51
assert len(set(heads)) == 51
assert data['count_model']['functional_boundaries'] == 46
assert data['count_model']['task_operation_sections'] == 6
print('mapping: 51 unique headings; 46 functional boundaries + 6 task operations')
PY
```

Expected: the JSON parses and the summary prints exactly once.

**Step 2: Write the failing validator**

Implement `tests/validate_agnostic_prompt.py` with these central constants and helpers:

```python
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).parents[1]
PROMPT_PATH = ROOT / 'prompts' / 'agnostic-software-development-system.md'
MAPPING_PATH = ROOT / 'tests' / 'fixtures' / 'expanded_prompt_sections.json'


def load_data():
    return json.loads(MAPPING_PATH.read_text(encoding='utf-8'))


def markdown_headings(text):
    return [match.group(1).strip() for match in re.finditer(r'^#{2,3}\s+(.+?)\s*$', text, re.MULTILINE)]


def section_text(text, heading, next_heading=None):
    start = re.search(rf'^##\s+{re.escape(heading)}\s*$', text, re.MULTILINE)
    if not start:
        return ''
    tail = text[start.end():]
    if next_heading:
        end = re.search(rf'^##\s+{re.escape(next_heading)}\s*$', tail, re.MULTILINE)
        return tail[:end.start()] if end else tail
    return tail


class ExpandedPromptContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_data()
        cls.prompt = PROMPT_PATH.read_text(encoding='utf-8')
        cls.headings = markdown_headings(cls.prompt)
        cls.lower = cls.prompt.lower()

    def test_prompt_is_present_and_expanded(self):
        self.assertTrue(PROMPT_PATH.is_file())
        self.assertGreaterEqual(len(self.prompt.splitlines()), 600)

    def test_required_headings_exist_in_order(self):
        expected = [row['abstract_heading'] for row in self.data['sections']]
        positions = [self.headings.index(heading) for heading in expected]
        self.assertEqual(positions, sorted(positions))
        missing = [heading for heading in expected if heading not in self.headings]
        self.assertFalse(missing, f'missing abstract sections: {missing}')

    def test_each_section_has_common_contract(self):
        fields = self.data['common_contract_fields']
        missing = {}
        for row in self.data['sections']:
            body = section_text(self.prompt, row['abstract_heading']).lower()
            absent = [field for field in fields if field.lower() not in body]
            if absent:
                missing[row['abstract_heading']] = absent
        self.assertFalse(missing, f'missing contract fields: {missing}')

    def test_task_operations_are_separate(self):
        task_heads = [row['abstract_heading'] for row in self.data['sections'] if row['source_boundary'].startswith('Task')]
        self.assertEqual(len(task_heads), 6)
        for heading in task_heads:
            self.assertIn(heading, self.headings)

    def test_no_source_specific_operational_coupling(self):
        forbidden = ('claude code', 'anthropic', 'openai', 'gpt-', 'fable 5', '/home/', '/users/', '@gmail.com', 'zsh')
        found = [value for value in forbidden if value in self.lower]
        self.assertFalse(found, f'forbidden identifiers in prompt: {found}')

    def test_no_gender_or_unresolved_policy_content(self):
        forbidden = ('gender-neutral pronoun', 'pronoun default', 'gender inference', 'infer pronouns', 'they/them default')
        found = [value for value in forbidden if value in self.lower]
        self.assertFalse(found, f'forbidden policy terms: {found}')
        self.assertNotRegex(self.prompt, r'(?im)\b(?:TBD|TODO|FIXME)\b')

    def test_required_state_and_completion_boundaries_exist(self):
        for phrase in ('unavailable', 'denied', 'failed', 'timed out', 'partially completed', 'unknown', 'authorization boundary', 'retry policy', 'verification'):
            self.assertIn(phrase, self.lower)
        self.assertIn('local completion', self.lower)
        self.assertIn('external completion', self.lower)


if __name__ == '__main__':
    unittest.main()
```

- [ ] Run the validator before expanding the prompt:

```bash
python3 -m unittest tests/validate_agnostic_prompt.py -v
```

Expected: FAIL because the current 180-line prompt lacks the 51 abstract sections and contract fields. Do not weaken the validator to make the existing prompt pass.

- [ ] Commit the fixture and red validator:

```bash
git add tests/fixtures/expanded_prompt_sections.json tests/validate_agnostic_prompt.py
git commit -m "test: define one-to-one expanded prompt contract"
```

### Task 2: Write sections 1–13 — identity, host context, memory, and session state

**Objective:** Implement the first 13 mapped boundaries without leaking source-specific values.

**Files:**
- Modify: `prompts/agnostic-software-development-system.md`
- Read: `CONSTITUTION.md`
- Reference: `tests/fixtures/expanded_prompt_sections.json`

**Step 1: Replace the prompt header and identity**

Start with `# Agent-Agnostic Software Development System` and define the agent as a software-development assistant. State that the prompt is independent of model, provider, product, CLI, operating system, shell, path, repository layout, and schema.

Create the first section as `## Identity and system role`. It MUST include all common contract fields and explain mission, scope, non-fabrication, and the distinction between behavior and runtime context.

**Step 2: Add host and communication boundaries**

Add these exact abstract headings in order:

```markdown
## Host harness and capability context
## Communicating with the user
## Session-specific guidance
```

Keep them independently addressable. Cover capability discovery, host limits, outcome-first communication, calibrated detail, user-facing progress, source attribution, faithful failure reporting, and session-specific instructions that do not override higher-priority rules.

**Step 3: Add memory and environment boundaries**

Add:

```markdown
## Persistent memory
## Environment context
## Working scratchpad area
```

The memory section MUST define read, create, deduplicate, update, validate, delete, stale, sensitive, unavailable, and denied flows. The environment section MUST treat host-provided facts as scoped runtime context. The scratchpad section MUST distinguish temporary working artifacts from project artifacts and define cleanup, persistence, and publication limits.

**Step 4: Add context and runtime-field boundaries**

Add:

```markdown
## Context management
## Session context
## Version-control status context
## Project instruction context
## User identity context
## Current date and time context
```

Represent source fields generically. Do not include source-specific names or values as operational instructions in the prompt. Each section must define unavailable, stale, and conflicting-context behavior.

**Step 5: Run focused structural validation**

```bash
python3 -m unittest tests.validate_agnostic_prompt.ExpandedPromptContractTests.test_required_headings_exist_in_order -v
python3 -m unittest tests.validate_agnostic_prompt.ExpandedPromptContractTests.test_each_section_has_common_contract -v
```

Expected: both tests pass for the first 13 sections but the complete suite still fails for later sections.

**Step 6: Commit**

```bash
git add prompts/agnostic-software-development-system.md
git commit -m "feat: add expanded prompt context boundaries"
```

### Task 3: Write sections 14–26 — agents, tools, user interaction, execution, Git, scheduling, and design

**Objective:** Preserve independent operational boundaries for auxiliary agents and the first concrete capability families.

**Files:**
- Modify: `prompts/agnostic-software-development-system.md`

**Step 1: Add auxiliary and reusable-capability sections**

Add, in order:

```markdown
## Auxiliary-agent capability
## Reusable-procedure capability
## Capability catalog and selection
## Agent delegation procedure
## Artifact capability
## User question and approval capability
```

Keep `Auxiliary-agent capability` separate from `Agent delegation procedure`. The former describes host availability and agent categories; the latter defines delegation procedure, context handoff, result verification, timeout, and unverified side-effect claims.

Keep `Artifact capability` separate from publication details that may appear in examples. Keep user questions and approvals separate from autonomous execution.

**Step 2: Add command, version-control, scheduling, and design sections**

Add, in order:

```markdown
## Command execution capability
## Version-control capability
## Schedule creation capability
## Schedule deletion capability
## Schedule listing capability
## Design synchronization capability
## File editing capability
```

Each section gets its own complete contract. In particular:

- command execution: preparation, risk assessment, output, status, timeout, cancellation, denied call, safe retry, partial side effect;
- version control: status, diff, branch/workspace, commit, push, merge, divergence, conflict, remote advancement, external completion;
- schedule creation/deletion/listing: separate inputs, authorization, duplicate schedule behavior, cancellation, unknown scheduler state;
- design synchronization: local design state, external synchronization, conflict, stale target, verification;
- file editing: target pre-read, minimal edit, overwrite/delete boundaries, conflict, partial write, post-write verification.

**Step 3: Verify boundaries**

```bash
python3 -m unittest tests.validate_agnostic_prompt.ExpandedPromptContractTests.test_required_headings_exist_in_order -v
python3 -m unittest tests.validate_agnostic_prompt.ExpandedPromptContractTests.test_task_operations_are_separate -v
```

Expected: required headings through `File editing capability` pass, while later headings remain pending.

**Step 4: Commit**

```bash
git add prompts/agnostic-software-development-system.md
git commit -m "feat: add expanded execution and scheduling capabilities"
```

### Task 4: Write sections 27–39 — planning, workspaces, monitoring, notebooks, notifications, reading, triggers, findings, wakeups, messages, and skills

**Objective:** Preserve separate lifecycle and interaction boundaries that were previously grouped into broad categories.

**Files:**
- Modify: `prompts/agnostic-software-development-system.md`

**Step 1: Add planning and workspace transitions**

Add, in order:

```markdown
## Planning-mode entry capability
## Isolated-workspace entry capability
## Planning-mode exit capability
## Isolated-workspace exit capability
```

Define entry preconditions, when planning is proportional, when implementation should proceed, approval boundaries, worktree creation and selection, exit verification, cleanup, branch state, and behavior when the host cannot isolate a workspace. Do not make planning a substitute for execution.

**Step 2: Add observation and file/resource capabilities**

Add:

```markdown
## Process monitoring capability
## Notebook modification capability
## User notification capability
## File and resource reading capability
```

Keep monitoring separate from execution and task completion. Keep notebook modification separate from ordinary file editing and define cell/input/output state, execution status, stale output, and partial result handling. Keep notifications separate from message delivery and require a meaningful notification target. Reading MUST define full, paginated, targeted, binary, truncated, and encoding-failure flows.

**Step 3: Add remote and reporting capabilities**

Add:

```markdown
## Remote-trigger capability
## Findings and report capability
## Scheduled wake-up capability
## Message delivery capability
## Procedure-loading capability
```

Define remote-trigger authorization and target boundaries; report generation versus report publication; wake-up scheduling versus task execution; message content, recipient, delivery, failure, and sensitive data; procedure discovery, activation, precedence, incompatibility, and unavailable skill behavior.

**Step 4: Verify boundaries and contract fields**

```bash
python3 -m unittest tests.validate_agnostic_prompt.ExpandedPromptContractTests.test_required_headings_exist_in_order -v
python3 -m unittest tests.validate_agnostic_prompt.ExpandedPromptContractTests.test_each_section_has_common_contract -v
```

Expected: sections through `Procedure-loading capability` pass their structural checks.

**Step 5: Commit**

```bash
git add prompts/agnostic-software-development-system.md
git commit -m "feat: add expanded planning monitoring and interaction capabilities"
```

### Task 5: Write sections 40–46 — task lifecycle, external readiness, web, workflow, writing, and handoff

**Objective:** Preserve every task operation as its own section and complete the final operational boundaries.

**Files:**
- Modify: `prompts/agnostic-software-development-system.md`

**Step 1: Add six independent task sections**

Add these exact headings in order:

```markdown
## Task creation capability
## Task retrieval capability
## Task listing capability
## Task output retrieval capability
## Task stopping capability
## Task update capability
```

For each operation, define purpose, when to use/not use, inputs, state transitions, dependencies, authorization, failure, retry, verification, and correct/incorrect examples. The sections MUST not be merged into a single `Task lifecycle` contract.

- Creation: define useful task fields, initial state, dependencies, and duplicate handling.
- Retrieval: distinguish missing, stale, current, and inaccessible task state.
- Listing: define scope, ordering, filtering, empty results, and stale entries.
- Output retrieval: distinguish running, complete, failed, partial, and unverified output.
- Stopping: define authorization, cancellation state, already-finished task, and unknown cancellation effect.
- Update: define valid transitions, stale updates, dependency changes, and evidence requirements.

**Step 2: Add final capability sections**

Add, in order:

```markdown
## External capability-readiness waiting
## Web retrieval capability
## Web search capability
## End-to-end workflow capability
## File creation and writing capability
## Cross-capability examples and handoff
```

Keep web search separate from web retrieval. Keep workflow as the cross-capability orchestration procedure, not as a replacement for individual contracts. Keep file creation/writing separate from editing. The final handoff section MUST distinguish local, committed, pushed, merged, deployed, and published states.

**Step 3: Add required examples**

Include at least 23 abstract examples from the spec. Each example MUST show relevant state, authorization, procedure, and report. Include incorrect examples for denied retries, unverified delegation, unauthorized publication, prompt injection, destructive security requests, and fabricated completion.

**Step 4: Run the full validator**

```bash
python3 -m unittest tests/validate_agnostic_prompt.py -v
```

Expected: all structural tests pass. If a field is missing, fix the prompt section rather than relaxing the validator.

**Step 5: Commit**

```bash
git add prompts/agnostic-software-development-system.md
git commit -m "feat: complete expanded prompt capability boundaries"
```

### Task 6: Add scenario validation for states, failures, authorization, and completion

**Objective:** Make the important behavioral boundaries mechanically checkable rather than relying only on heading presence.

**Files:**
- Modify: `tests/validate_agnostic_prompt.py`
- Create: `tests/fixtures/expanded_prompt_scenarios.json`

**Step 1: Create scenario fixtures**

Create JSON records with this shape:

```json
[
  {
    "id": "write-conflict",
    "prompt_signal": "target changed after inspection",
    "required_terms": ["inspect", "conflict", "stop", "overwrite"],
    "forbidden_claims": ["write succeeded"],
    "expected_decision": "stop-and-surface-conflict"
  },
  {
    "id": "denied-command",
    "prompt_signal": "host denies command",
    "required_terms": ["denied", "do not retry", "adapt"],
    "forbidden_claims": ["retry verbatim"],
    "expected_decision": "adapt-or-report"
  },
  {
    "id": "unverified-publication",
    "prompt_signal": "publication lacks verifiable handle",
    "required_terms": ["publication", "verify", "unknown"],
    "forbidden_claims": ["published successfully"],
    "expected_decision": "report-unknown"
  },
  {
    "id": "defensive-security",
    "prompt_signal": "scoped authorized defensive test",
    "required_terms": ["authorized", "bounded", "defensive"],
    "forbidden_claims": [],
    "expected_decision": "allow-within-scope"
  },
  {
    "id": "malicious-mass-targeting",
    "prompt_signal": "mass targeting or denial of service",
    "required_terms": ["refuse", "denial", "mass", "redirect"],
    "forbidden_claims": ["execute attack"],
    "expected_decision": "refuse-and-redirect"
  }
]
```

Add records covering unavailable capability, timeout with partial output, remote divergence, delegated unverified side effect, stale memory, cancelled task, process not ready, local artifact without publication, and compacted-context resumption.

**Step 2: Add scenario checks**

Add a validator method that loads the fixture and asserts each required term exists in the prompt and each forbidden claim does not appear as an instruction. The test MUST report the scenario ID when it fails.

**Step 3: Add explicit state coverage checks**

For every mapping row, assert that its section body contains `State model`, `Failure flow`, `Retry policy`, `Authorization boundary`, and `Verification`. Assert the prompt contains all cross-capability states from the spec.

**Step 4: Run focused scenario tests**

```bash
python3 -m unittest tests.validate_agnostic_prompt.ExpandedPromptContractTests -v
```

Expected: all structural and scenario tests pass.

**Step 5: Commit**

```bash
git add tests/fixtures/expanded_prompt_scenarios.json tests/validate_agnostic_prompt.py
git commit -m "test: validate expanded prompt failure and state scenarios"
```

### Task 7: Update README and complete the acceptance gate

**Objective:** Document the expanded prompt, mapping fixture, validator command, and one-to-one section guarantee.

**Files:**
- Modify: `README.md`

**Step 1: Update the prompt documentation**

Replace the existing prompt description with text that states:

```markdown
## Agent-Agnostic Software Development Prompt

The canonical prompt is [`prompts/agnostic-software-development-system.md`](prompts/agnostic-software-development-system.md). It is a single expanded system instruction that preserves one-to-one operational boundaries from the reference capability model while converting proprietary names into abstract host capabilities.

The mapping and contract tests are in [`tests/fixtures/expanded_prompt_sections.json`](tests/fixtures/expanded_prompt_sections.json) and [`tests/validate_agnostic_prompt.py`](tests/validate_agnostic_prompt.py).

Validate it with:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests/validate_agnostic_prompt.py -v
```
```

Do not document proprietary tool names as required runtime interfaces. The README may mention that the mapping is traceability metadata.

**Step 2: Run the complete acceptance gate**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests/validate_agnostic_prompt.py -v
git diff --check
python3 -m json.tool tests/fixtures/expanded_prompt_sections.json >/dev/null
python3 -m json.tool tests/fixtures/expanded_prompt_scenarios.json >/dev/null
```

Expected: all tests pass, both JSON files parse, and `git diff --check` produces no output.

**Step 3: Run portability and policy scans against the prompt only**

```bash
if rg -n -i 'claude code|anthropic|openai|gpt-|fable 5|mythos 5|/Users/|/home/|@gmail.com|<project-dir>|<scratchpad-dir>|zsh' prompts/agnostic-software-development-system.md; then exit 1; else true; fi
if rg -n -i 'pronoun default|gender-neutral pronoun|infer pronouns|gender inference|they/them default' prompts/agnostic-software-development-system.md; then exit 1; else true; fi
```

Expected: both commands produce no output and exit successfully.

**Step 4: Verify exact section mapping**

Run a small Python check that loads the fixture, extracts `##` headings, asserts all 51 abstract headings exist in order, and prints:

```text
mapping validation: 46 functional boundaries + 6 independent task sections = 51 headings
```

**Step 5: Review requirements against the spec**

Confirm coverage for:

- FR-001–FR-102, including FR-097–FR-102 one-to-one preservation;
- NFR-001–NFR-014;
- SC-001–SC-015;
- all 23 required examples;
- all edge cases and failure scenarios;
- every row in the target mapping.

**Step 6: Commit documentation**

```bash
git add README.md prompts/agnostic-software-development-system.md tests/
git commit -m "docs: document expanded agnostic prompt validation"
```

**Step 7: Final status**

```bash
git status --short --branch
git log --oneline -8
```

Expected: no tracked or untracked implementation artifacts outside the planned files, and all prompt validation commands pass.

## Verification Matrix

| Spec area | Implementation evidence |
|---|---|
| One-to-one section preservation | Mapping fixture, ordered-heading validator, FR-097–FR-102 |
| Abstract names | Prompt portability scan and fixture's `abstract_heading` values |
| Common contracts | Per-section field validator |
| States and failures | State vocabulary checks and scenario fixtures |
| Authorization | Risk-boundary sections and scenario decisions |
| Retries | Per-section retry policy and denied-operation scenarios |
| Practical procedures | 51 sections with numbered procedure fields |
| Examples | 23 required examples and incorrect-behavior cases |
| Security | Allow, clarify, constrain, refuse, redirect scenarios |
| Completion | Fresh verification and local/external completion checks |
| Host portability | No operational coupling scan |
| Maintainability | One file, stable headings, standard-library validator |

## Risks and Mitigations

- **Risk: one-to-one preservation produces a very large prompt.** Mitigation: keep one file but use a common contract format, concise examples, and a 600–1,000 line target with a warning rather than an artificial hard cap.
- **Risk: source-specific names leak into the final prompt.** Mitigation: keep source names only in the fixture's traceability metadata and scan the prompt file independently.
- **Risk: grouped task operations regress.** Mitigation: six explicit task headings, unique mapping rows, and an order test.
- **Risk: context-only sections become empty boilerplate.** Mitigation: require the full common contract in every section and define unavailable/stale/conflict behavior for context.
- **Risk: validation checks wording rather than behavior.** Mitigation: combine structural checks with scenario fixtures for denial, partial completion, unknown state, authorization, and security decisions.
- **Risk: requirements drift between spec, fixture, and prompt.** Mitigation: treat the fixture as the executable section contract and review it against the Target Prompt Structure table before implementation.
- **Risk: transient test caches dirty the repository.** Mitigation: run tests with `PYTHONDONTWRITEBYTECODE=1` and report any remaining generated artifacts rather than using destructive cleanup without authorization.

## Self-Review Checklist

- [x] Exact files and responsibilities are defined.
- [x] The prompt remains a single artifact.
- [x] All 51 independently addressable headings are listed.
- [x] The 46-functional-boundary versus six-task-operation count is explicit.
- [x] Proprietary names are traceability metadata only; abstract headings are the final interface.
- [x] Every task includes verification and a commit.
- [x] Structural and scenario validation are both covered.
- [x] The plan addresses FR-001–FR-102, NFR-001–NFR-014, and SC-001–SC-015.
- [x] No unresolved placeholder is required.
- [x] No runtime or host adapter is introduced.
- [x] README documentation is included.
