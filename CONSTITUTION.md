# 🧠 CONSTITUTION.md
## AI Coding Agent Constitution

This document defines the **non-negotiable principles, architectural standards, and behavioral rules** that MUST guide all code generation, modification, and analysis performed by the AI agent.

The agent MUST always prioritize:
> **Simplicity > Clarity > Maintainability > Performance**

---

# 1. Core Coding Principles

## 1.1 DRY (Don't Repeat Yourself)
- The agent MUST avoid code duplication at all costs.
- Any repeated logic, value, or structure MUST be abstracted into:
  - variables
  - functions
  - modules
- Rationale:
  - Reduces token usage
  - Prevents inconsistency
  - Avoids context loss within LLM window

---

## 1.2 KISS (Keep It Simple, Stupid)
- The agent MUST always choose the simplest possible implementation.
- The agent MUST NOT introduce unnecessary abstractions or complexity.
- Prefer:
  - small files (≤ 150–300 lines)
  - direct and readable logic
- The agent MUST avoid overengineering.

---

## 1.3 YAGNI (You Aren't Gonna Need It)
- The agent MUST NOT implement:
  - speculative features
  - unnecessary edge cases
  - premature optimizations
- Only implement what is explicitly required.

---

## 1.4 TDD (Test-Driven Development)
- The agent MUST:
  - write tests before OR alongside implementation
- Every feature MUST include:
  - unit tests
  - deterministic assertions
- Code WITHOUT tests is considered INCOMPLETE.

---

## 1.5 Separation of Concerns
- Each file MUST have a single responsibility.
- The agent MUST NOT mix:
  - UI logic with business logic
  - configuration with domain logic
- Violations cause:
  - Context Poisoning
  - Increased hallucination risk
  - Reduced maintainability

---

# 2. Architectural Principles

## 2.1 Mandatory Architecture: Feature-Based

The agent MUST organize the project using **Feature-Based Architecture**.

---

## 2.2 Why This Is Mandatory

Layer-based architecture:
- Forces the agent to scan many irrelevant files
- Increases token usage
- Causes inefficient reasoning

Feature-based architecture:
- Reduces context size
- Improves reasoning accuracy
- Prevents context poisoning
- Enables isolated feature development

---

## 2.3 Required Project Structure

The agent MUST follow this structure:

    src/
    ├── features/
    │   ├── <feature-name>/
    │   │   ├── components/
    │   │   ├── hooks/
    │   │   ├── services/
    │   │   ├── store/
    │   │   ├── types/
    │   │   └── tests/
    │
    └── shared/
        ├── ui/
        ├── utils/
        └── constants/

---

## 2.4 Feature Encapsulation Rule

- Each feature MUST be self-contained.
- A feature MUST include:
  - UI (components)
  - Logic (hooks/services)
  - Types
  - State (if applicable)
  - Tests

---

## 2.5 Shared Layer Constraints

- The `shared/` directory MUST contain ONLY:
  - reusable UI components
  - generic utilities
- The agent MUST NOT place business logic in `shared/`.

---

# 3. Context Optimization Rules (LLM-Specific)

## 3.1 Context Efficiency
- The agent MUST minimize the number of files required to solve a task.
- The agent SHOULD operate within a single feature whenever possible.

---

## 3.2 Context Poisoning Prevention
The agent MUST avoid introducing unrelated logic into files.

Examples of violations:
- Mixing authentication logic inside sales modules
- Adding global state unnecessarily
- Placing unrelated types together

---

## 3.3 File Size Control
- Files SHOULD remain small and focused.
- If a file exceeds reasonable size:
  - it MUST be split by responsibility

---

# 4. Karpathy Behavioral Rules for the Agent

## 4.1 Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

---

## 4.2 Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

---

## 4.3 Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

---

## 4.4 Goal-Driven Execution

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

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

## 4.5 Additional Behavioral Rules

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

## 4.6 Testing Discipline
- Every feature MUST be testable
- The agent MUST transform tasks into verifiable goals before writing code:
  - "Fix the bug" -> write a test that reproduces it, then make it pass
  - "Add validation" -> write tests for invalid inputs, then make them pass
- For multi-step tasks, the agent MUST state a brief plan with a verify step per stage
- Tests MUST:
  - be deterministic
  - not depend on external state
  - reflect real use cases

---

# 5. Definition of Done

A task is ONLY considered complete if:

- Code follows all principles (DRY, KISS, YAGNI)
- Architecture follows Feature-Based structure
- No context poisoning is introduced
- Tests are implemented and passing
- Code is readable and maintainable

---

# 6. Enforcement Priority

If conflicts arise, the agent MUST follow this order:

1. Simplicity (KISS)
2. Correctness (TDD)
3. Separation of Concerns
4. DRY
5. Architecture Rules

---

# Final Rule

The agent MUST ALWAYS read and comply with this CONSTITUTION.md  
BEFORE generating, modifying, or reviewing any code.

Failure to comply invalidates the output.
