---
name: writing-specs
description: "Use when you have a feature idea, user request, or product requirement that needs to be structured into a formal specification before implementation. Covers spec writing, requirement clarification, acceptance criteria definition, and success metrics — following Spec-Driven Development (SDD) methodology inspired by GitHub's Spec Kit."
---

# Writing Specifications (Spec-Driven Development)

> **Inspired by:** GitHub Spec Kit (`github/spec-kit`) — Spec-Driven Development methodology.

## Overview

Write **formal specifications** that capture **what** to build and **why** before any code is written. A spec is the single source of truth that bridges product intent and technical implementation. It focuses exclusively on the problem domain — the **HOW** (tech stack, architecture, implementation plan) belongs to the `writing-plans` skill.

**Core principle:** Separate WHAT/WHY (spec) from HOW (plan) to prevent scope drift, ambiguous requirements, and wasted implementation cycles.

**Announce at start:** "I'm using the writing-specs skill to create the feature specification."

**Save specs to:** `specs/<YYYY-MM-DD>-<feature-name>/spec.md`

## The SDD Workflow

```
Ideation → Constitution Check → Specify → Clarify → Plan → Tasks → Implement
   ↑                                              ↓
   └────────────── Iterate ───────────────────────┘
```

### Phases (this skill covers phase 1-3):

| Phase | Skill | Artifact | Focus |
|-------|-------|----------|-------|
| 1. **Constitution Check** | writing-specs | constitution check | Project principles & constraints |
| 2. **Specify** | writing-specs | `spec.md` | WHAT & WHY |
| 3. **Clarify** | writing-specs | clarifications | Resolve ambiguities |
| 4. **Plan** | writing-plans | `plan.md` | HOW (tech stack, architecture) |
| 5. **Tasks** | writing-plans or subagent-driven-development | `tasks.md` | WHO & WHERE |
| 6. **Implement** | subagent-driven-development | code | EXECUTION |

---

## Constitution Check

Before writing a spec, check if the project has a **constitution** — a set of non-negotiable principles and constraints (e.g., CONSTITUTION.md). If one exists, verify the feature idea doesn't violate it:

**Gates:**
- [ ] Does the feature align with the project's stated principles?
- [ ] Does the feature violate any "MUST NOT" rules in the constitution?
- [ ] Is there a simpler approach that satisfies the same need? (KISS/YAGNI check)
- [ ] Does this feature duplicate existing functionality? (DRY check)

**If the constitution check fails**, flag the violation and suggest alternatives before proceeding.

---

## Spec Template

```markdown
# Feature Specification: [FEATURE NAME]

**Status:** Draft | In Review | Approved | Superseded
**Author:** [Name]
**Created:** [YYYY-MM-DD]
**Updated:** [YYYY-MM-DD]
**Inspired by:** [User request, bug report, product requirement, etc.]

## Problem Statement

[Describe the problem or opportunity in one paragraph. What pain point does this address? Why does it matter? Focus on the user need, not the solution.]

## User Stories

> **IMPORTANT:** Prioritize user stories as P1 (MVP), P2 (important), P3 (nice-to-have).
> Each story must be independently testable — implementing just P1 should deliver value.

### Story 1 — [Brief Title] (Priority: P1)

[Describe what the user wants to accomplish in plain language]

**Why P1:** [Explain why this is essential for the MVP]

**Acceptance Scenarios:**

1. **Given** [initial context], **When** [user action], **Then** [expected outcome]
2. **Given** [initial context], **When** [user action], **Then** [expected outcome]

**Independent Test:** [How to verify this story works in isolation — e.g., "Can be tested by visiting /dashboard and seeing the widget render with mock data"]

---

### Story 2 — [Brief Title] (Priority: P2)

[Describe]

**Why P2:** [Explain why this is important but not blocking]

**Acceptance Scenarios:**

1. **Given** [initial context], **When** [user action], **Then** [expected outcome]

**Independent Test:** [How to verify this independently]

---

### Story 3 — [Brief Title] (Priority: P3)

[Describe]

**Why P3:** [Explain why this is a future enhancement]

**Acceptance Scenarios:**

1. **Given** [initial context], **When** [user action], **Then** [expected outcome]

**Independent Test:** [How to verify this independently]

## Functional Requirements

> **ACTION:** Mark any requirement with unclear details as `[NEEDS CLARIFICATION: specific question]`.

- **FR-001:** System MUST [specific capability]
- **FR-002:** System MUST [specific capability]
- **FR-003:** Users MUST be able to [key interaction]
- **FR-004:** System MUST [data requirement]
- **FR-005:** System MUST [behavioral requirement]
- **FR-006:** System MUST [NEEDS CLARIFICATION: what happens when X occurs?]

## Non-Functional Requirements

> Constraints on the system's operation, not its features.

- **NFR-001:** [Performance target, e.g., "Page loads in under 2 seconds"]
- **NFR-002:** [Security constraint, e.g., "All API calls require authentication"]
- **NFR-003:** [Reliability, e.g., "System handles 1000 concurrent users"]
- **NFR-004:** [Compliance, e.g., "GDPR compliant data handling"]

## Key Entities

> Domain concepts this feature introduces or modifies. Describe at the business level — no implementation details.

| Entity | Description | Relationships |
|--------|-------------|---------------|
| [Entity 1] | [What it represents in the business domain] | [Related entities] |
| [Entity 2] | [What it represents] | [Related entities] |

## Success Criteria

> Measurable, technology-agnostic outcomes. How do we know this shipped correctly?

- **SC-001:** [Metric, e.g., "Users can complete the primary flow in under 3 steps"]
- **SC-002:** [Metric, e.g., "Zero P1 bugs reported in first week post-launch"]
- **SC-003:** [Metric, e.g., "95% of users successfully complete the task on first attempt"]

## Edge Cases & Error Scenarios

> What happens at the boundaries? Think about failure modes.

- [ ] What happens when [boundary condition, e.g., "user submits empty form"]?
- [ ] How does the system handle [error scenario, e.g., "network timeout during save"]?
- [ ] What if [race condition, e.g., "two users edit the same resource simultaneously"]?
- [ ] What about [boundary value, e.g., "maximum file size exceeded"]?

## Assumptions

> Explicit assumptions that constrain the spec. Documenting assumptions prevents surprises during planning.

- **A-001:** [Assumption, e.g., "Users have a modern browser (ES2020+)"]
- **A-002:** [Assumption, e.g., "Mobile support is out of scope for v1"]
- **A-003:** [Dependency, e.g., "Existing auth system will be reused"]
- **A-004:** [Assumption, e.g., "Third-party API response time < 500ms"]

## Questions & Clarifications

> Every `[NEEDS CLARIFICATION]` marker from above collected here. Present these to the user/stakeholder in a batched question before proceeding.

1. FR-006: What should happen when [specific scenario]?
2. Story 2: Is [specific behavior] correct?
3. A-004: Is the response time assumption accurate?

## Review Checklist

- [ ] All `[NEEDS CLARIFICATION]` markers resolved
- [ ] User stories are prioritized (P1/P2/P3)
- [ ] Each P1 story has a clear independent test
- [ ] Acceptance scenarios use Given/When/Then format
- [ ] Functional requirements are specific and testable
- [ ] Success criteria are measurable
- [ ] Edge cases and failure modes documented
- [ ] Assumptions are explicit and reasonable
- [ ] Constitution check passed (if applicable)
```

---

## Clarify Phase

After writing the spec draft, the spec likely contains `[NEEDS CLARIFICATION]` markers. Before creating the plan:

1. **Batch all questions** into a single message — do not ask one at a time
2. Present each question beside the requirement it came from
3. Propose a reasonable default when possible: "I assumed [X], but please confirm"

**Example:**

> Before I proceed to planning, I have 3 clarifications:
>
> 1. **FR-006:** What should happen when the payment gateway times out? I assumed a retry-with-backoff strategy.
> 2. **Story 2:** Are batch operations expected to have a progress bar, or is background processing sufficient?
> 3. **A-004:** The third-party SLA states 2s p95 — is 500ms the target for cached responses?

## Spec Review & Approval

Before handing off to `writing-plans`, ensure:

- [ ] **Complete:** No `[NEEDS CLARIFICATION]` markers remain
- [ ] **Specific:** Each requirement is specific enough to test
- [ ] **Prioritized:** User stories have clear P1/P2/P3
- [ ] **Aligned:** Does not violate the project constitution
- [ ] **Reviewed:** Stakeholder has reviewed and approved

## Handoff to Plan

After spec approval, hand off to `writing-plans`:

> "Spec complete and saved to `specs/<feature>/spec.md`. Ready for planning. The spec covers: [brief summary of P1 stories, key entities, critical FRs]. The plan should address the HOW — tech stack decisions, architecture, and implementation tasks."

## Best Practices

1. **Bias toward questions, not assumptions.** If something is ambiguous, mark it `[NEEDS CLARIFICATION]` — don't silently pick a default.
2. **User stories before requirements.** Start from the user's perspective, derive functional requirements from stories.
3. **One spec, one feature.** A spec should describe exactly one feature. If you need multiple independent features, write separate specs.
4. **Specs are living documents.** Update the spec as understanding evolves during implementation. Spec drift = technical debt.
5. **P1 is MVP.** Every spec must have at least one P1 story that delivers standalone value. If no story is independently valuable, reconsider the feature scope.
6. **Constitution gates prevent waste.** A 5-minute constitution check can save days of implementing something that violates project principles.
7. **Clarify early.** The earlier you resolve ambiguity, the cheaper the change. A clarification during spec-writing costs 5 minutes; during implementation it costs hours.

## References

- GitHub Spec Kit: [https://github.com/github/spec-kit](https://github.com/github/spec-kit)
- Spec-Driven Development docs: [https://github.github.com/spec-kit/](https://github.github.com/spec-kit/)
- OpenSpec (lightweight alternative): [https://github.com/Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec)
- BMAD-METHOD: [https://github.com/oimiragieo/BMAD-SPEC-KIT](https://github.com/oimiragieo/BMAD-SPEC-KIT)