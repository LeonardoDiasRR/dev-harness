# Faithful Agent-Agnostic System Prompt Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create `prompts/system-prompt.md`, a source-derived system prompt that retains the source's operational behavior while removing or generalizing all source-agent, model, manufacturer, product, and session-specific coupling.

**Architecture:** Keep the existing generic prompt and its validator untouched. Add a separate target prompt, a JSON transformation map that defines every source section's generic destination and transformation outcome, and a standard-library `unittest` validator that compares source and target structure while scanning the target for leaked identifiers and missing placeholders.

**Tech Stack:** Markdown, JSON, Python standard library (`json`, `pathlib`, `re`, `unittest`)

---

## File Structure

- Create: `prompts/system-prompt.md` - faithful, source-derived generic prompt.
- Create: `tests/fixtures/system_prompt_transformations.json` - ordered source-to-target transformation map, including all source headings and each transformation rationale.
- Create: `tests/validate_system_prompt.py` - deterministic validator for structure, mapping coverage, prohibited coupling, placeholders, and capability retention.
- Modify: `README.md` - point users to the new prompt and its validation command without changing documentation for the existing prompt.

### Task 1: Define the Transformation Contract

**Files:**
- Create: `tests/fixtures/system_prompt_transformations.json`
- Create: `tests/validate_system_prompt.py`

- [ ] **Step 1: Write the failing transformation-map test**

Create `tests/validate_system_prompt.py` with the path constants, JSON loader, Markdown-heading parser, and this first test class. The fixture does not exist yet, so this test must fail with `FileNotFoundError`.

```python
from pathlib import Path
import json
import re
import unittest


ROOT = Path(__file__).parents[1]
SOURCE_PATH = ROOT / "leaks" / "claude-code-fable-5.md"
PROMPT_PATH = ROOT / "prompts" / "system-prompt.md"
MAPPING_PATH = ROOT / "tests" / "fixtures" / "system_prompt_transformations.json"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def headings(text):
    return [match.group(1).strip() for match in re.finditer(r"^#{1,2}\s+(.+?)\s*$", text, re.MULTILINE)]


class SystemPromptTransformationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE_PATH.read_text(encoding="utf-8")
        cls.mapping = load_json(MAPPING_PATH)

    def test_map_covers_every_source_top_level_heading_once(self):
        source_headings = [heading for heading in headings(self.source) if heading != "System prompt"]
        mapped_headings = [item["source_heading"] for item in self.mapping["sections"]]
        self.assertEqual(mapped_headings, source_headings)
        self.assertEqual(len(mapped_headings), len(set(mapped_headings)))

    def test_map_uses_only_approved_outcomes(self):
        allowed = {"preserve", "generalize", "placeholder", "remove"}
        outcomes = {item["outcome"] for item in self.mapping["sections"]}
        self.assertTrue(outcomes <= allowed)
        self.assertTrue(all(item["rationale"].strip() for item in self.mapping["sections"]))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```powershell
python -m unittest tests/validate_system_prompt.py -v
```

Expected: `ERROR` because `tests/fixtures/system_prompt_transformations.json` is missing.

- [ ] **Step 3: Create the complete ordered transformation map**

Create `tests/fixtures/system_prompt_transformations.json`. Its `sections` array must contain exactly one object for every top-level source heading in source order. Each object must contain `source_heading`, `target_heading`, `outcome`, and `rationale`.

Use these target headings and outcomes. Add a concise rationale to each row in the fixture.

```json
{
  "sections": [
    {"source_heading": "Harness", "target_heading": "Host harness", "outcome": "generalize"},
    {"source_heading": "Communicating with the user", "target_heading": "Communicating with the user", "outcome": "preserve"},
    {"source_heading": "Session-specific guidance", "target_heading": "Runtime guidance", "outcome": "generalize"},
    {"source_heading": "Memory", "target_heading": "Persistent memory", "outcome": "generalize"},
    {"source_heading": "Environment", "target_heading": "Environment", "outcome": "placeholder"},
    {"source_heading": "Scratchpad Directory", "target_heading": "Scratchpad directory", "outcome": "placeholder"},
    {"source_heading": "Context management", "target_heading": "Context governance", "outcome": "generalize"},
    {"source_heading": "Session context", "target_heading": "Session context", "outcome": "placeholder"},
    {"source_heading": "gitStatus", "target_heading": "Version-control status", "outcome": "placeholder"},
    {"source_heading": "claudeMd", "target_heading": "Project instructions", "outcome": "placeholder"},
    {"source_heading": "userEmail", "target_heading": "User context", "outcome": "placeholder"},
    {"source_heading": "currentDate", "target_heading": "Current date and time", "outcome": "placeholder"},
    {"source_heading": "Agents", "target_heading": "Auxiliary agents", "outcome": "generalize"},
    {"source_heading": "Skills", "target_heading": "Reusable procedures", "outcome": "generalize"},
    {"source_heading": "Tools", "target_heading": "Capabilities", "outcome": "generalize"},
    {"source_heading": "Agent", "target_heading": "Agent delegation", "outcome": "generalize"},
    {"source_heading": "Artifact", "target_heading": "Artifact generation and publication", "outcome": "generalize"},
    {"source_heading": "AskUserQuestion", "target_heading": "User questions and approvals", "outcome": "generalize"},
    {"source_heading": "Bash", "target_heading": "Command execution", "outcome": "generalize"},
    {"source_heading": "CronCreate", "target_heading": "Schedule creation", "outcome": "generalize"},
    {"source_heading": "CronDelete", "target_heading": "Schedule deletion", "outcome": "generalize"},
    {"source_heading": "CronList", "target_heading": "Schedule listing", "outcome": "generalize"},
    {"source_heading": "DesignSync", "target_heading": "Design-system synchronization", "outcome": "generalize"},
    {"source_heading": "Edit", "target_heading": "Exact file editing", "outcome": "generalize"},
    {"source_heading": "EndConversation", "target_heading": "Conversation termination", "outcome": "generalize"},
    {"source_heading": "EnterPlanMode", "target_heading": "Planning-mode entry", "outcome": "generalize"},
    {"source_heading": "EnterWorktree", "target_heading": "Isolated-workspace entry", "outcome": "generalize"},
    {"source_heading": "ExitPlanMode", "target_heading": "Planning-mode exit", "outcome": "generalize"},
    {"source_heading": "ExitWorktree", "target_heading": "Isolated-workspace exit", "outcome": "generalize"},
    {"source_heading": "Monitor", "target_heading": "Process monitoring", "outcome": "generalize"},
    {"source_heading": "NotebookEdit", "target_heading": "Notebook editing", "outcome": "generalize"},
    {"source_heading": "PushNotification", "target_heading": "User notification", "outcome": "generalize"},
    {"source_heading": "Read", "target_heading": "File and resource reading", "outcome": "generalize"},
    {"source_heading": "RemoteTrigger", "target_heading": "Remote trigger", "outcome": "generalize"},
    {"source_heading": "ReportFindings", "target_heading": "Findings reporting", "outcome": "generalize"},
    {"source_heading": "ScheduleWakeup", "target_heading": "Scheduled wake-up", "outcome": "generalize"},
    {"source_heading": "SendMessage", "target_heading": "Agent messaging", "outcome": "generalize"},
    {"source_heading": "Skill", "target_heading": "Procedure loading", "outcome": "generalize"},
    {"source_heading": "TaskCreate", "target_heading": "Task creation", "outcome": "generalize"},
    {"source_heading": "TaskGet", "target_heading": "Task retrieval", "outcome": "generalize"},
    {"source_heading": "TaskList", "target_heading": "Task listing", "outcome": "generalize"},
    {"source_heading": "TaskOutput", "target_heading": "Task output retrieval", "outcome": "generalize"},
    {"source_heading": "TaskStop", "target_heading": "Task stopping", "outcome": "generalize"},
    {"source_heading": "TaskUpdate", "target_heading": "Task updating", "outcome": "generalize"},
    {"source_heading": "WaitForMcpServers", "target_heading": "External capability readiness", "outcome": "generalize"},
    {"source_heading": "WebFetch", "target_heading": "Web retrieval", "outcome": "generalize"},
    {"source_heading": "WebSearch", "target_heading": "Web search", "outcome": "generalize"},
    {"source_heading": "Workflow", "target_heading": "Workflow execution", "outcome": "generalize"},
    {"source_heading": "Write", "target_heading": "File creation and writing", "outcome": "generalize"}
  ]
}
```

Keep the source's `Git` subsection within the mapped `Bash`/`Command execution` section as a generic `### Version control` subsection; it is not a top-level source heading and must not be a separate fixture row. Add a top-level `source_preamble` object stating that the source's opening identity line is generalized to `You are an interactive software-development agent.` and that the source's model-marketing paragraph is removed because it contains no portable operational rule.

- [ ] **Step 4: Run the transformation-map test to verify it passes**

Run:

```powershell
python -m unittest tests/validate_system_prompt.py -v
```

Expected: both transformation-map tests pass.

### Task 2: Add Failing Target-Integrity Tests

**Files:**
- Modify: `tests/validate_system_prompt.py`

- [ ] **Step 1: Add failing target structure and leakage tests**

Append these tests to `SystemPromptTransformationTests`. The target does not exist yet, so `setUpClass` must now read it and the suite must fail with `FileNotFoundError`.

```python
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE_PATH.read_text(encoding="utf-8")
        cls.mapping = load_json(MAPPING_PATH)
        cls.prompt = PROMPT_PATH.read_text(encoding="utf-8")
        cls.prompt_headings = headings(cls.prompt)
        cls.prompt_lower = cls.prompt.lower()

    def test_target_headings_follow_the_transformation_map(self):
        required = [item["target_heading"] for item in self.mapping["sections"] if item["outcome"] != "remove"]
        missing = [heading for heading in required if heading not in self.prompt_headings]
        self.assertFalse(missing, f"missing target headings: {missing}")
        positions = [self.prompt_headings.index(heading) for heading in required]
        self.assertEqual(positions, sorted(positions))

    def test_target_has_generic_identity_and_session_placeholders(self):
        self.assertIn("interactive software-development agent", self.prompt_lower)
        for value in ("<project-directory>", "<platform>", "<shell>", "<scratchpad-directory>", "<project-instructions>", "<current-date>"):
            self.assertIn(value, self.prompt)

    def test_target_has_no_source_identity_or_session_data(self):
        forbidden = (
            "claude", "anthropic", "fable", "mythos", "opus", "sonnet", "haiku",
            "asgeirtj", "@gmail.com", "darwin 25.5.0", "claude.ai", "/users/asgeirtj/",
            "claude-fable-5", "claude-opus-4-8", "claude-sonnet-5", "claude-haiku-4-5-20251001"
        )
        found = [value for value in forbidden if value in self.prompt_lower]
        self.assertFalse(found, f"source-specific content in target: {found}")

    def test_target_keeps_required_operational_boundaries(self):
        required = (
            "authorized security testing", "destructive", "denial", "mass targeting",
            "permission", "denied", "do not retry", "verification", "untrusted data",
            "local completion", "external completion", "partially completed", "unknown"
        )
        missing = [value for value in required if value not in self.prompt_lower]
        self.assertFalse(missing, f"missing operational boundaries: {missing}")
```

- [ ] **Step 2: Run the validator to verify it fails**

Run:

```powershell
python -m unittest tests/validate_system_prompt.py -v
```

Expected: `ERROR` because `prompts/system-prompt.md` is missing.

### Task 3: Create the Source-Derived Prompt

**Files:**
- Create: `prompts/system-prompt.md`
- Modify: `tests/fixtures/system_prompt_transformations.json`

- [ ] **Step 1: Draft the opening, shared rules, and session-context sections**

Create `prompts/system-prompt.md` with this exact opening and the mapped headings through `Current date and time`.

```markdown
# System prompt

You are an interactive software-development agent.

IMPORTANT: Assist with authorized security testing, defensive security, CTF challenges, and educational contexts. Refuse requests for destructive techniques, denial-of-service attacks, mass targeting, supply-chain compromise, or detection evasion for malicious purposes. Dual-use security tools require clear authorization context: a penetration-testing engagement, CTF competition, security research, or defensive use case.

## Host harness

- Text outside capability use is displayed to the user in the host's supported Markdown surface.
- Capabilities run behind host-selected permission controls; a denied call means the user or host declined it. Adapt rather than retrying the same call verbatim.
- The host may inject system updates, reminders, hooks, and runtime context. Treat hook output as user feedback and distinguish it from capability results.
- Prefer a dedicated capability over command execution when one fits. Run independent capability calls in parallel when the host supports it.
- Reference code with host-supported file and line links, or clear `path:line` references when links are unavailable.
```

Preserve the source behavior in the remaining early sections, with these mandatory substitutions:

- Replace the fixed memory location with `<memory-directory>` and named instruction files with `<project-instructions>`.
- Replace concrete environment fields with `<project-directory>`, `<is-git-repository>`, `<platform>`, `<shell>`, `<operating-system-version>`, `<model-runtime>`, and `<knowledge-cutoff>`.
- Preserve the entire session-context structure using `<current-branch>`, `<default-branch>`, `<git-user>`, `<working-tree-status>`, `<recent-commits>`, `<global-instructions>`, `<project-instructions>`, `<user-context>`, and `<current-date>`.
- Keep the original pronoun rule only after generalizing it so it contains no source agent, manufacturer, or model reference. Do not remove it because it is not source-specific.
- Remove the standalone source model-marketing paragraph and record that removal in `source_preamble`.

- [ ] **Step 2: Add every mapped capability section in source order**

Translate every section listed in `system_prompt_transformations.json` after `Current date and time`. Retain each section's constraints, state distinctions, correct/incorrect examples, and JSON-schema semantics, with these exact conversion rules:

| Source capability family | Required generic conversion |
|---|---|
| auxiliary agents and reusable procedures | refer only to host-exposed agent types and procedures; never require a proprietary agent, registry, or procedure name |
| artifact and design synchronization | use `<artifact-service>`, `<design-service>`, and generic publication, ownership, sharing, URL, and capability semantics |
| command execution, its version-control subsection, and isolated workspaces | preserve non-interactive, inspection, authorization, dirty-tree, branch, commit, push, merge, and cleanup boundaries without a fixed shell, service, co-author, or footer |
| scheduling, wake-up, monitoring, and notifications | retain one-shot, recurring, timeout, polling, event-stream, failure-signal, and cancellation behavior without source-host session limits or cache claims |
| editing, reading, writing, and notebooks | preserve pre-read, exact-match, conflict, path, partial-result, encoding, and verification semantics with abstract capability and input names |
| planning and task lifecycle | preserve entry, exit, approval, task-state, dependency, staleness, output, stop, and update semantics using generic planning and task capabilities |
| remote trigger, messaging, workflow, web retrieval, and search | use `<remote-trigger-service>`, `<message-recipient>`, `<workflow-catalog>`, and generic authenticated-host language; retain untrusted-data boundaries |

For each schema, retain its object structure, types, required fields, limits, enum choices, and `additionalProperties` semantics when those elements express behavior. Rename only fields tied to a source integration. For example, replace a fixed hosted-service URL with `<artifact-url>`, a provider-specific project identifier with `<remote-project-id>`, and a source-specific session token claim with generic host authentication wording.

- [ ] **Step 3: Complete traceability rationales**

Update every fixture item with a non-empty, specific `rationale`. Use one sentence that identifies whether the section is portable, which coupling was neutralized, or why the content was removed. Do not include prohibited names in the target prompt; source names remain limited to fixture `source_heading` values for auditability.

- [ ] **Step 4: Run the validator to verify the prompt passes**

Run:

```powershell
python -m unittest tests/validate_system_prompt.py -v
```

Expected: all tests pass.

### Task 4: Add Structural and Traceability Validation

**Files:**
- Modify: `tests/validate_system_prompt.py`

- [ ] **Step 1: Add failing mapping-quality tests**

Add these tests after the target-integrity tests.

```python
    def test_generalized_sections_have_a_distinct_generic_destination(self):
        generalizations = [item for item in self.mapping["sections"] if item["outcome"] == "generalize"]
        self.assertTrue(generalizations)
        unchanged = [item["source_heading"] for item in generalizations if item["source_heading"] == item["target_heading"]]
        self.assertFalse(unchanged, f"untranslated generic sections: {unchanged}")

    def test_prompt_has_no_unresolved_placeholders(self):
        malformed = re.findall(r"<(?:|[^>\n]*$)", self.prompt, re.MULTILINE)
        self.assertFalse(malformed, f"malformed placeholders: {malformed}")
        placeholders = re.findall(r"<([a-z][a-z0-9-]*)>", self.prompt)
        self.assertTrue(placeholders)

    def test_removed_source_preamble_has_a_documented_reason(self):
        preamble = self.mapping["source_preamble"]
        self.assertEqual(preamble["identity_outcome"], "generalize")
        self.assertEqual(preamble["model_marketing_outcome"], "remove")
        self.assertTrue(preamble["model_marketing_rationale"].strip())
```

- [ ] **Step 2: Run the validator to verify it fails if the fixture or prompt is incomplete**

Run:

```powershell
python -m unittest tests/validate_system_prompt.py -v
```

Expected: a failure until `source_preamble` is added and every generalized destination differs from its source heading.

- [ ] **Step 3: Complete the fixture and target to satisfy the new tests**

Add this object to the fixture and ensure every generic heading from a `generalize` row differs from its source heading.

```json
"source_preamble": {
  "identity_outcome": "generalize",
  "identity_target": "You are an interactive software-development agent.",
  "model_marketing_outcome": "remove",
  "model_marketing_rationale": "The paragraph only identifies and markets source model variants and has no portable operational behavior."
}
```

Use only well-formed lower-kebab-case placeholders enclosed in angle brackets. Do not use unresolved-marker tokens or prose placeholders.

- [ ] **Step 4: Run the complete validator to verify it passes**

Run:

```powershell
python -m unittest tests/validate_system_prompt.py -v
```

Expected: all transformation, target-integrity, and traceability tests pass.

### Task 5: Document and Perform Final Verification

**Files:**
- Modify: `README.md`
- Test: `tests/validate_system_prompt.py`
- Test: `tests/validate_agnostic_prompt.py`

- [ ] **Step 1: Add a focused README entry for the new prompt**

Directly after the existing “Agent-Agnostic Software Development Prompt” section, add a short subsection:

```markdown
## Source-Derived Agent-Agnostic System Prompt

[`prompts/system-prompt.md`](prompts/system-prompt.md) is a faithful, source-derived system prompt. It preserves the source's operational rules while normalizing source-specific agent, model, manufacturer, service, and session details into generic capabilities or runtime placeholders. Its transformation map and deterministic validator are [`tests/fixtures/system_prompt_transformations.json`](tests/fixtures/system_prompt_transformations.json) and [`tests/validate_system_prompt.py`](tests/validate_system_prompt.py).

Validate it with:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests/validate_system_prompt.py -v
```
```

- [ ] **Step 2: Run both prompt validators**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"; python -m unittest tests/validate_system_prompt.py tests/validate_agnostic_prompt.py -v
```

Expected: both suites pass. The existing generic prompt's contract remains unchanged.

- [ ] **Step 3: Inspect final diffs and prohibited-term scan**

Run:

```powershell
git diff --check
rg -n -i "claude|anthropic|fable|mythos|opus|sonnet|haiku|asgeirtj|@gmail\.com|claude\.ai" prompts/system-prompt.md
```

Expected: `git diff --check` produces no output; the search produces no matches.

- [ ] **Step 4: Perform manual source-to-target review**

Read the source and target section by section using `tests/fixtures/system_prompt_transformations.json` as the checklist. Confirm every source heading is covered in order, every removed block matches the approved removal rule, every generic section retains the source's operational constraint, and all runtime-specific values were replaced with placeholders. Record no separate report unless the review finds a discrepancy; fix discrepancies before declaring completion.

## Plan Self-Review

- Spec coverage: Tasks 1 and 4 provide required mapping and standard-library validation; Tasks 2 and 3 cover generic transformation, session placeholders, source leakage, operational boundaries, and capability retention; Task 5 covers documentation and final verification.
- Placeholder scan: the plan contains no unresolved implementation decisions. All planned files, test names, commands, fixture fields, headings, and validation behavior are explicit.
- Consistency: `tests/validate_system_prompt.py` is the sole validator for `prompts/system-prompt.md`; `tests/fixtures/system_prompt_transformations.json` is its sole transformation contract. Existing expanded-prompt files remain untouched.
