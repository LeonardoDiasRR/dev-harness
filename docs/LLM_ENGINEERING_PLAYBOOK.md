# Generic Engineering Guide for LLM Agents - Engineering Playbook

This document is a generic, reusable guide for LLM agents in any software project. It can be exported to other repositories with minimal project-specific changes.

## 1. Core Behavioral Rules

1. **Do not infer success from compilation.** Code that compiles does not mean code works.
2. **Do not infer runtime behavior from unit tests.** Passing unit tests do not prove the real flow works.
3. **Do not say "implemented" when only the interface changed.** Frontend state is not persistence.
4. **Never convert "not tested" into "pass".** If runtime was not tested, say so explicitly.
5. **Prefer small commits.** Do not mix cleanup with feature fixes.
6. **Do not create documentation without functional justification.** Documentation without concrete value is noise.
7. **Do not remove tags that were already pushed.** Create corrective tags `.1`, `.2`, `.3` instead of moving them.
8. **When you find a reusable false-claim pattern, update this guide.** Lessons must be permanent.

## 2. Sources of Truth

Source-of-truth priority depends on the question being answered.

### 2.1. Normative Truth: What the Agent Must Do

For rules, constraints, and required behavior, follow project instructions in this order:

1. User's direct instructions
2. `CONSTITUTION.md`
3. Project-specific guides such as `docs/LLM_PROJECT_GUIDE.md`
4. This generic playbook
5. Existing code style and conventions

Project instructions are normative. They can override a convenient implementation path even when the current code behaves differently.

### 2.2. Factual Truth: What the System Currently Does

For implementation facts, inspect sources in this order:

1. **Route/endpoint code** - the definitive source for what the API actually does
2. **Application/service code** - the definitive source for real behavior behind the route
3. **Tests** - evidence of expected behavior, but not a substitute for runtime validation
4. **Specification/plan documentation** - context and intent, not implementation proof
5. **User interface** - frontend state is not persistence

**Critical rule:** if documentation says "X exists" but the route code has no endpoint for X, **X does not exist**.

## 3. Planning Rules

- Define verifiable success criteria before implementing.
- "Add validation" means "write tests for invalid inputs, then make them pass".
- "Fix bug" means "write a test that reproduces it, then make it pass".
- "Refactor X" means "tests pass before and after".
- For multi-step tasks, briefly state: plan -> verify -> plan -> verify.

## 4. Coding Rules

### 4.1. Naming

- Classes, functions, methods, and variables: use the project's language, usually English.
- Docstrings and comments: use the project's documentation language.
- Files: use ecosystem conventions, such as snake_case for Python and camelCase for TypeScript/JSX.

### 4.2. Typing

- All new code must have explicit typing.
- Python: use `-> ReturnType` and `param: Type`.
- TypeScript: use strict types and avoid `any`.

### 4.3. TDD

- Write tests before or alongside implementation, as required by `CONSTITUTION.md`.
- Prefer writing the failing test first when feasible.
- Do not skip tests to "move faster".

### 4.4. Scope

- Do not create features outside the current phase or feature scope.
- Do not implement abstractions for single-use code.
- Do not add unsolicited flexibility or configurability.
- If you write 200 lines and it could be 50, rewrite it.

### 4.5. Surgical Changes

- Touch only what you must. Do not "improve" adjacent code.
- Do not remove unrelated dead code.
- When your changes create orphans, such as imports, variables, or functions, remove them.
- Every changed line must trace directly to the user's request.

## 5. Testing Rules

### 5.1. Confidence Hierarchy

E2E > Integration > Unit

A passing unit test **DOES NOT** guarantee that the flow works. A passing E2E test is much stronger evidence for the real user experience.

### 5.2. Unit Tests

- Test isolated functions or methods.
- Use mocks for external dependencies.
- Keep them fast and deterministic.

### 5.3. Integration Tests

- Test a complete flow with a real database or equivalent.
- Verify persistence and ORM/storage behavior.

### 5.4. E2E Tests

- Test the complete user flow with browser and backend.
- Slower, but more reliable for validating the real experience.

### 5.5. General Rules

- Tests must cover positive path, negative path, error path, and relevant edge cases.
- A mock does not replace an integration test when behavior depends on multiple components.
- Do not use `expect.any(String)` when the contract matters; assert the exact value.
- If there is an "on" path, there must be an "off" path. Test both.

## 6. Review Rules

### 6.1. Implementation Verification

Before approving any change, verify:

1. Does the endpoint/functionality exist in code, not only in docs?
2. Does the handler contain real logic, not a stub or fake?
3. Does the handler call the correct service/component?
4. Is authorization/validation policy applied?
5. Does the test cover both positive and negative paths?
6. Does the state persist in the backend/storage, not only in the frontend?

### 6.2. Frontend Review

- A checkbox is only "functional" if click -> backend persistence -> survives refresh.
- A button is only "functional" if it has a handler -> calls endpoint -> handles success/error -> updates cache.
- Frontend-only permission filtering is **NOT** security.
- Frontend state is **NOT** persistence.

### 6.3. Finding Classification

- **CONFIRMED** - true and verified
- **PARTIAL** - partially true
- **FALSE CLAIM** - claimed but incorrect
- **MISSING TEST** - works but has no test
- **MISSING RUNTIME VALIDATION** - only unit-tested, with no integration/runtime validation
- **BACKEND GAP** - backend does not implement what the plan requires
- **FRONTEND GAP** - frontend does not implement what the plan requires
- **DOC GAP** - documentation is incorrect or incomplete
- **RELEASE/TAG GAP** - tag does not point to HEAD or push is incomplete

## 7. Runtime Validation Rules

### 7.1. Health Checks

- Health endpoints must respond.
- Health is not feature validation.

### 7.2. Functional Endpoints

For each new endpoint:

1. Add an integration test that calls the real endpoint.
2. Verify the correct HTTP response, including status code and body.
3. Verify database persistence when applicable.
4. Verify error behavior: 400, 401, 403, 404, 500 as relevant.

### 7.3. Frontend

1. Render without TypeScript errors.
2. Pass unit tests.
3. Build successfully.
4. Cover critical flows with E2E tests.

### 7.4. Absolute Rule

If a feature depends on seed data, authentication, or server state, and runtime was not tested: **mark it explicitly as "NOT FULLY VERIFIED"**. Never convert "not tested" into "pass".

## 8. Frontend/Backend Contract Rules

### 8.1. Types

- Frontend TypeScript types/interfaces must reflect backend schemas.
- If the backend changes a field, update the frontend.
- Do not assume backend fields that do not exist.

### 8.2. Endpoints

- Every frontend endpoint must map to a real backend endpoint.
- `method`, `path`, `request body`, and `response schema` must match.
- HTTP errors must be handled in the frontend with try/catch, toast, or state rollback as appropriate.

### 8.3. Cache Invalidation

- Always invalidate cache after mutation.
- Without invalidation, the UI shows stale state.
- This is a common root cause of bugs reported as "data does not update".

## 9. Persistence vs Frontend State Rules

### 9.1. Absolute Rule

**Frontend state is NOT persistence.**

- A checked checkbox in the frontend does NOT mean a permission was granted.
- A clicked button in the frontend does NOT mean a request was sent to the backend.
- A success toast does NOT mean the operation was persisted.

### 9.2. Persistence Verification

To verify that something persisted:

1. Verify that the backend endpoint was called with the exact expected payload.
2. Verify that the data exists in the database through a direct query or list endpoint.
3. Verify that the state survives refresh through refetch and comparison.

## 10. Authorization/Security Rules

### 10.1. Fail-Closed

- If authorization cannot be verified, **deny** access.
- Never grant access through silent failure.
- Every sensitive action goes through authorization policy.

### 10.2. Frontend Filter != Security

- Frontend-only permission filtering is not security.
- Backend must enforce authorization independently of the frontend.

### 10.3. Matrices and Visible Rows

When the interface displays row-based data, for example permissions by group/user:

- The mutation payload must include the visible row identifier, such as `group_code` or `user_id`.
- Never use fixed values such as `user_id: 0` or infer the target from the current user.
- Frontend cache must be mapped by the row identifier.
- Grant for row A must not affect row B. Revoke for row A must not affect row B.

## 11. Documentation Rules

### 11.1. When to Update

- New functionality was implemented.
- Behavior changed.
- A bug fix changes user expectations.
- An architectural decision changed.

### 11.2. How to Update

- Update the corresponding document.
- Do not create documentation without concrete value.
- Do not update documentation before implementation in a way that creates false lead time.

### 11.3. Do Not

- Do not create documentation "just in case".
- Do not update reports with test results you did not run.
- Do not mark "PASS" in a checklist without executing the check.

## 12. Git, Commit, Tag, and Release Rules

### 12.1. Tag Creation

- Use annotated tags with `git tag -a`.
- Name follows the pattern: `phase{N}-{feature}-ready.{counter}`.
- Increment counter for corrections: `.1`, `.2`, `.3`.

### 12.2. Do Not Move Tags

- If a tag was already pushed, **DO NOT** move it.
- Create a new tag `.2`, `.3`, etc.
- Moving a pushed tag is an anti-pattern.

### 12.3. Verification

Before push:

```bash
git rev-parse HEAD
git rev-list -n 1 <tag>
# must be EQUAL
```

### 12.4. Workflow

1. Commit docs and fixes.
2. Verify clean working tree.
3. Run quality gates.
4. Create tag.
5. Verify tag points to HEAD.
6. Push main.
7. Push tag.

### 12.5. Commit Messages

- Use the project convention, for example `feat(...)`, `fix(...)`, `docs(...)`.
- Keep the message clear and concise.
- Do not create empty commits.

## 13. Definition of DONE

A task is DONE when:

1. Implementation is complete in code.
2. Tests are written and passing.
3. Quality gates are clean: linter, formatter, tests.
4. Documentation is updated when necessary.
5. Commit has a clear message, when committing is part of the task.

## 14. Definition of READY

A phase or release is READY when:

1. **Clean working tree** - `git status --short` is empty.
2. **Green gates** - all tests, linters, and formatters pass.
3. **Accurate documentation** - the phase report reflects the real state, not an optimistic state.
4. **Tag points to final HEAD** - `git rev-list -n 1 <tag>` == `git rev-parse HEAD`.
5. **No overclaiming** - the report does not claim unverified functionality.
6. **Runtime when possible** - if runtime was not tested, document that explicitly.

**NEVER mark READY without runtime evidence when runtime can be verified.**

## 15. Common LLM Agent Failure Patterns

### 15.1. READY Claim Without Runtime Evidence

**What happens:** The report says "READY", but no endpoint was tested at runtime.

**How to avoid:** Include at least one integration test that calls the real endpoint. If runtime is not possible, mark explicitly as "NOT FULLY VERIFIED".

### 15.2. Checkbox That Does Not Persist

**What happens:** A checkbox toggles in the frontend but does not call the backend.

**How to avoid:** Verify that `onChange` calls the correct function and that the result is persisted.

### 15.3. Frontend State Confused With Persistence

**What happens:** The report says "permissions persist", but only React state changes.

**How to avoid:** Verify API calls and/or database state.

### 15.4. Disabled Buttons Instead of Real CRUD

**What happens:** A button has `disabled` but no handler, or the handler does nothing.

**How to avoid:** Verify handler, endpoint, and persistence.

### 15.5. Fake Frontend CRUD Without Backend

**What happens:** The UI allows create/edit/delete, but only in local state.

**How to avoid:** Verify that each operation calls the corresponding backend endpoint.

### 15.6. Forgotten Cache Invalidation

**What happens:** Data is mutated but UI does not update.

**How to avoid:** Every mutate must have `invalidateQueries` or corresponding refetch.

### 15.7. Forgotten Reverse Behavior

**What happens:** Grant works but revoke does not, or vice versa.

**How to avoid:** Test both paths. If there is an "on" path, there must be an "off" path.

### 15.8. Unit Tests Only, No Runtime

**What happens:** All unit tests pass, but the real flow fails.

**How to avoid:** Add at least one integration test for critical flows.

### 15.9. Tag Created Before Documentation Commit

**What happens:** The tag points to a HEAD that lacks final documentation.

**How to avoid:** Commit docs BEFORE creating the tag.

### 15.10. Pushed Tag Does Not Point to Final HEAD

**What happens:** Additional commits were made after the tag.

**How to avoid:** Verify `git rev-list -n 1 <tag>` == `git rev-parse HEAD` after all commits.

### 15.11. Context/Multitenancy Ignored

**What happens:** Endpoints work without a context header, or backend does not validate scope.

**How to avoid:** Test with valid, invalid, and missing headers. Backend must reject invalid scopes.

### 15.12. Missing Seed Users, Login "Tested"

**What happens:** The report says "login tested", but the database has no seed users.

**How to avoid:** Add seeding or mark "RUNTIME NOT FULLY VERIFIED - blocked by missing seed users".

### 15.13. "All Buttons Work" Without a Matrix

**What happens:** The report claims all buttons work without verifying each one.

**How to avoid:** Create a button-by-button table with each button's status.

### 15.14. Visible Row Ignored in Payload

**What happens:** A table displays data by row, but the handler ignores the clicked row and sends a fixed or wrong target.

**How to avoid:** For each matrix mutation, verify in code and tests that `row id + column action + resource id` reach the backend with exact values.

### 15.15. Incompatible Frontend/Backend Contract

**What happens:** The frontend sends `group_code`, `user_id: 0`, or another payload that does not match the backend schema.

**How to avoid:** Read the endpoint schema, compare it with the TypeScript type, and create a test that fails if the payload has the wrong field or missing target.

### 15.16. Test Too Permissive to Prove Behavior

**What happens:** A test uses `expect.any(String)`, only verifies that a function was called, or does not cover reverse/negative paths.

**How to avoid:** Assert exact values for base, target, and action; cover grant, revoke, refresh, and authorization denial.

### 15.17. Permission Target Model Does Not Match UI Row

**What happens:** The interface displays permissions by group/row, but the backend uses `user_id` to identify the target. The frontend sends `user_id: 0` or `current_user.user_id`, ignoring the row. Cache is mapped by `base + action`, collapsing all rows.

**How to avoid:** When the UI shows permissions by row/group, ensure that:

1. The grant payload contains the visible row identifier, never a fixed value or current user.
2. The revoke payload contains the same identifier.
3. Frontend cache is mapped by the row identifier.
4. Tests assert exact payload values, not `expect.any(String)`.
5. Grant for row A does not affect row B, and revoke for row A does not affect row B.

## 16. How to Avoid Each Failure Pattern

| Error | Prevention |
|-------|------------|
| READY without evidence | Run at least one integration test or mark "NOT FULLY VERIFIED" |
| Checkbox without persistence | Verify API call in `onChange` and verification query after |
| Frontend state != persistence | Verify API calls and database state |
| Fake CRUD | Verify each operation has a corresponding backend endpoint |
| Cache without invalidation | Every mutate must invalidate queries or refetch |
| Missing reverse behavior | Test both: grant+revoke, create+delete, enable+disable |
| Unit tests only | Add at least one integration test for critical flows |
| Tag before docs | Commit docs BEFORE creating tag |
| Tag does not point to HEAD | Verify SHA before and after tag |
| Multitenancy ignored | Test with valid, invalid, and missing headers |
| Missing seed users | Seed or explicitly mark "NOT FULLY VERIFIED" |
| No button matrix | Create a button-by-button table in the report |
| Visible row ignored | Assert exact row id + action + resource id in payload |
| Frontend/backend contract mismatch | Compare backend schema, TypeScript type, and real call |
| Test too permissive | Replace `expect.any` with exact values when contract matters |
| Wrong permission target model | Grant/revoke must use the UI row identifier, never a fixed value |

## 17. Final Checklist Before Claiming READY

- [ ] Clean working tree: `git status --short` is empty
- [ ] Linter/formatter clean
- [ ] Backend tests passing
- [ ] Frontend lint/build passing, when applicable
- [ ] Documentation updated
- [ ] Tag created and points to final HEAD
- [ ] Runtime tested OR "NOT FULLY VERIFIED" documented
- [ ] No claim about unverified functionality
- [ ] All new endpoints tested with unit and integration tests
- [ ] Reverse behaviors tested: grant/revoke, create/delete, etc.
- [ ] Cache invalidation verified
- [ ] Backend authorization verified, not only frontend filtering

## 18. Final Report Format for Phases and Releases

For phase, release, or handoff work, the agent must return a final report with the fields below. For small tasks, use a concise final response that includes only the relevant evidence and omissions.

```text
Phase {N} - {title} - Final Report

Model used:
GPT-5.5 medium escalation:
Branch:
Final HEAD:
Origin/main HEAD:
Tag:
Tag points to HEAD:
Working tree:
Backend Ruff:
Backend format:
Backend tests:
Focused backend tests:
Frontend lint:
Frontend unit:
Frontend build:
Focused frontend tests:
Root cause:
Old behavior:
New behavior:
Runtime validation:
Docs:
Commits:
Accepted gaps:
Final status:

Final status must be one of:
READY - {descriptive reason}
BLOCKED - {exact blocker}
```
