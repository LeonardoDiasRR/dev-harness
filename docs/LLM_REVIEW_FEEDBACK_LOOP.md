# LLM Agent Review Feedback Loop

## Purpose

This document defines a mandatory, generic process for reviewing implementations in any project. Its goal is to capture systematic errors, correct root causes, and continuously improve coding quality for LLM agents.

## Mandatory Process

### Step 1 - Read the Required Guides

**Before any review**, read:

1. `CONSTITUTION.md` - non-negotiable project principles and enforcement priority
2. `docs/LLM_ENGINEERING_PLAYBOOK.md` - generic coding and review standards
3. `docs/LLM_PROJECT_GUIDE.md` - project-specific rules, when present
4. `docs/PHASE{N}_*.md` - plan and report for the phase being reviewed, when applicable

### Step 2 - Extract Claims

List every claim made by the implementing agent:

| # | Claim | Source Document |
|---|-------|-----------------|
| 1 | "Endpoint X exists" | PHASE{N}_REPORT.md |
| 2 | "Checkbox Y persists to the backend" | PHASE{N}_REPORT.md |
| ... | ... | ... |

### Step 3 - Verify Each Claim

For each claim, verify:

1. **Code:** Does the real code contain the endpoint or functionality?
2. **Tests:** Is there a test for the claimed behavior?
3. **Documentation:** Does the report reflect the real state?
4. **Runtime:** Was runtime behavior tested, or only unit-tested?

### Step 4 - Classify Each Finding

Use one of these classifications:

- **CONFIRMED** - the claim is true and verified
- **PARTIAL** - partially true, for example frontend works but backend does not
- **FALSE CLAIM** - the claim is false, for example it says data persists but it does not
- **MISSING TEST** - behavior exists but has no test
- **MISSING RUNTIME VALIDATION** - only unit-tested, with no integration/runtime validation
- **BACKEND GAP** - backend does not implement what the plan requires
- **FRONTEND GAP** - frontend does not implement what the plan requires
- **DOC GAP** - documentation is incorrect or incomplete
- **RELEASE/TAG GAP** - tag does not point to HEAD, push is incomplete, or commit is missing

### Step 5 - Record Each Error

For each error found, record:

```text
ERROR #{number}: {short_title}
- Agent claimed: {what the LLM said}
- Reality: {what actually happens}
- Root cause: {why the error happened}
- Correct rule: {which guide rule was violated}
- Test that would have caught it: {which test would catch the error}
```

### Step 6 - Correct Confirmed Defects

If a code defect is confirmed:

1. Apply the smallest safe code fix possible
2. Add or update tests
3. Rerun quality gates: linter, formatter, tests
4. Do not refactor unrelated code

### Step 7 - Update the Phase Report

Update `docs/PHASE{N}_*.md` with:

- Review findings
- Fixes applied
- Accepted gaps with justification

### Step 8 - Update Guides

If a reusable lesson is found:

1. If the lesson applies to **any project**, update `docs/LLM_ENGINEERING_PLAYBOOK.md`
2. If the lesson is **specific to this project**, update `docs/LLM_PROJECT_GUIDE.md`
3. If the lesson is a **new class of error**, add it to the appropriate guide as a new section
4. Never leave reusable lessons undocumented

### Step 9 - Separate Commits

```bash
git add docs/LLM_ENGINEERING_PLAYBOOK.md
git commit -m "docs(llm): add lesson from phase {N} review: {title}"

git add docs/LLM_PROJECT_GUIDE.md
git commit -m "docs(llm): add project-specific lesson from phase {N} review"

git add docs/PHASE{N}_*.md
git commit -m "docs(phase{N}): update review findings"
```

### Step 10 - Generate a Review Report

Use `docs/templates/LLM_REVIEW_REPORT_TEMPLATE.md` to generate the report, when the review is phase-based or the project provides that template.

## Detailed Classifications

### CONFIRMED

The claim is true. Code exists, tests pass, and runtime is verified when applicable.

Example: "POST /resource grants permission" - the endpoint exists, the handler calls the service, the service applies the policy, and a test covers it.

### PARTIAL

The claim is partially true.

Example: "Permission checkbox works" - the frontend renders and changes state, but does not call the backend.

### FALSE CLAIM

The claim is false.

Example: "Permissions persist after refresh" - state exists only in React, not in the database.

### MISSING TEST

Behavior exists but has no test.

Example: policy is implemented but has no unit test.

### MISSING RUNTIME VALIDATION

Unit tests pass, but nothing was tested at runtime or through integration.

Example: all permission unit tests pass, but no integration test verifies real persistence.

### BACKEND GAP

The backend does not implement what the plan or request requires.

Example: the plan requires DELETE /permissions/{action}, but the endpoint does not exist.

### FRONTEND GAP

The frontend does not implement what the plan or request requires.

Example: the plan requires a "Share" column, but the action list does not include it.

### DOC GAP

Documentation is incorrect, outdated, or incomplete.

Example: the report says "X passed", but the real number is different.

### RELEASE/TAG GAP

The tag does not point to HEAD, push is incomplete, or a commit is missing.

Example: the tag was created before the final documentation commit.

## When to Stop

Stop the review when:

1. All claims have been verified
2. All errors have been classified
3. Critical fixes have been applied
4. The review report has been generated when applicable
5. Reusable lessons have been added to the guides

## Integration with the Phase Cycle

Each phase review must:

1. Follow this process
2. Generate a report at `docs/PHASE{N}_REVIEW.md`
3. Update `docs/LLM_ENGINEERING_PLAYBOOK.md` for generic lessons
4. Update `docs/LLM_PROJECT_GUIDE.md` for project-specific lessons
5. Commit separately
6. Reference the review in the PR or merge notes

## Quality Metrics

Track over time:

| Metric | Goal |
|--------|------|
| False claims per phase | Decreasing trend |
| Missing tests per phase | Decreasing trend |
| Lessons added to playbook | Cumulative, generic |
| Lessons added to project guide | Cumulative, project-specific |
| Recurring errors | Reduce repeated types |

If the same error category appears in 3 or more phases, create a specific section in the appropriate guide.
