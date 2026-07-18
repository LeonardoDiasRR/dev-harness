# 🧠 CONSTITUTION.md
## AI Coding Agent Constitution

This document defines the **non-negotiable principles, architectural standards, and behavioral rules** that MUST guide all code generation, modification, and analysis performed by the AI agent.

The agent MUST always prioritize:
> **Simplicity > Clarity > Maintainability > Performance**

---

## F1. DRY (Don't Repeat Yourself)
- The agent MUST avoid code duplication at all costs.
- Any repeated logic, value, or structure MUST be abstracted into variables, functions, or modules.
- Rationale: reduces token usage, prevents inconsistency, avoids context loss within LLM window.

---

## F2. KISS (Keep It Simple, Stupid)
- The agent MUST always choose the simplest possible implementation.
- The agent MUST NOT introduce unnecessary abstractions or complexity.
- Prefer small files (≤ 150–300 lines) with direct and readable logic.
- The agent MUST avoid overengineering.

---

## F3. YAGNI (You Aren't Gonna Need It)
- The agent MUST NOT implement speculative features, unnecessary edge cases, or premature optimizations.
- Only implement what is explicitly required.

---

## F4. TDD (Test-Driven Development)
- The agent MUST write tests before OR alongside implementation.
- Every feature MUST include unit tests with deterministic assertions.
- Code WITHOUT tests is considered INCOMPLETE.

---

## F5. Separation of Concerns
- Each file MUST have a single responsibility.
- The agent MUST NOT mix UI logic with business logic, or configuration with domain logic.
- Violations cause context poisoning, increased hallucination risk, and reduced maintainability.

---

## F6. Feature-Based Architecture

The agent MUST organize frontend projects using **Feature-Based Architecture**.

### Why Feature-Based Architecture Is Mandatory

Layer-based architecture forces the agent to scan many irrelevant files, increases token usage, and causes inefficient reasoning. Feature-based architecture:
- Reduces context size
- Improves reasoning accuracy
- Prevents context poisoning
- Enables isolated feature development

### Required Frontend Structure

    src/
    ├── features/                   # One directory per business feature
    │   └── <feature-name>/
    │       ├── components/         # UI components scoped to this feature
    │       ├── hooks/              # Feature-specific React hooks
    │       ├── services/           # API calls and business logic
    │       ├── store/              # Local state (Zustand slice, Redux slice…)
    │       ├── types/              # TypeScript types/interfaces for this feature
    │       └── tests/              # Unit and integration tests
    │
    └── shared/                     # Truly reusable, feature-agnostic code
        ├── ui/                     # UI kit: buttons, inputs, modals, layout primitives
        ├── utils/                  # Generic utility functions and helpers
        └── constants/              # App-wide constants and configuration values

### Feature-Based Rules
- Each feature MUST be self-contained: components, hooks, services, types, state, and tests.
- A feature MUST NOT import from another feature — extract shared logic into `shared/`.
- The `shared/` directory MUST contain ONLY reusable UI components and generic utilities; no business logic.

### Component Reuse (Shared-First)

Before creating a new UI component, the agent MUST follow this order:

1. **Check `shared/ui`** — if an equivalent component exists, reuse it.
2. **Check across `features/**/components`** — if a suitable component exists and is not feature-specific, move it to `shared/ui`, update imports, and adjust tests.
3. **Only then create a new feature-scoped component** — only if it is truly specific to that feature.

# SHARED BEHAVIORAL RULES

## S1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

---

## S2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

---

## S3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: every changed line must trace directly to the user's request.

---

## S4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

---

## S5. Additional Behavioral Rules

The agent MUST:
- justify non-trivial decisions

The agent MUST NOT:
- make assumptions not present in requirements
- create unused code
- leave incomplete implementations
- ignore error handling at system boundaries (user input, external APIs)
- introduce hidden side effects
- modify code adjacent to the change unless directly required by the task
- deviate from the existing code style

When the agent's own changes create orphaned imports, variables, or functions, the agent MUST remove them.

---

# Definition of Done

A task is ONLY considered complete if:

- Code follows all applicable principles (DRY, KISS, YAGNI)
- Architecture follows Feature-Based Architecture
- No context poisoning is introduced
- Tests are implemented and passing
- Code is readable and maintainable

---

# Enforcement Priority

If conflicts arise, the agent MUST follow this order:

1. Simplicity (KISS)
2. Correctness (TDD)
3. Separation of Concerns
4. DRY
5. Architecture Rules
