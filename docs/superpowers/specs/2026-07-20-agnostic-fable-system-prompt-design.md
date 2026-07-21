# Design Specification: Faithful Agent-Agnostic System Prompt Copy

**Status:** Approved for specification review
**Created:** 2026-07-20
**Source:** `leaks/claude-code-fable-5.md`
**Target:** `prompts/system-prompt.md`

## Problem Statement

Create a faithful, agent-agnostic copy of the source system prompt. The target must preserve all useful operational content while removing or generalizing references to the source agent, its model, and its manufacturer. It must also prevent leakage of source-session personal and environmental data.

The repository already contains an independently written expanded generic prompt. That file is not the source for this task and must not be reorganized, condensed, or substituted for the required source-derived copy.

## Goals

1. Create `prompts/system-prompt.md` from the source prompt.
2. Preserve the source's section order, functional boundaries, operating rules, procedures, examples, states, limits, failure flows, retry rules, and verification rules.
3. Generalize mixed useful/proprietary content rather than deleting the useful rule.
4. Convert exclusive tools, services, paths, schemas, and integrations into abstract capability contracts.
5. Replace concrete session and personal data with generic placeholders.
6. Provide deterministic validation for prohibited references, required structure, placeholder handling, and transformation coverage.

## Non-Goals

- Replacing the target with the existing generic prompt.
- Rewriting, compressing, rearranging, or improving the source's operational design.
- Implementing a new agent runtime, host adapter, or universal tool protocol.
- Preserving source identity, product marketing, model comparisons, vendor links, account details, paths, environment snapshots, or automatic attribution.
- Adding dependencies for validation.

## Approved Design

### Transformation Strategy

Use semantic normalization with transformation traceability.

Each source block must have one of four outcomes:

| Outcome | Use | Result |
|---|---|---|
| Preserve | The text is already portable and contains no source-specific data. | Copy without semantic change. |
| Generalize | A useful rule is mixed with a specific agent, model, vendor, product, service, path, tool, schema, or integration. | Replace the coupling with a portable equivalent while retaining the rule. |
| Placeholder | A structural runtime-context field contains a concrete source-session value. | Keep the field and replace its value with a `<placeholder>`. |
| Remove | The block is solely source identity, product marketing, variant comparison, vendor promotion, automatic attribution, or otherwise has no portable operational equivalent. | Remove the complete block. |

No functional block may be removed merely because it includes source-specific wording. Its portable operational meaning must be generalized instead.

### Target Structure

`prompts/system-prompt.md` must retain the source's macrostructure and order:

1. Identity, security, harness, communication, memory, environment, scratchpad, and context management.
2. Session context, including version-control status, project instructions, user context, and date/time context.
3. Auxiliary-agent and reusable-procedure catalogs.
4. Complete capability catalog covering delegation, artifacts, questions, command execution, version control, scheduling, editing, planning, isolated workspaces, monitoring, reading, writing, web research, task lifecycle, and workflows.
5. Abstracted capability schemas and examples preserving source semantics, types, requirements, limits, and state distinctions.

The target must be derived directly from the source. It must not incorporate or depend on the existing generic prompt.

### Generalization Rules

- Replace source-agent identity with a generic software-development agent identity.
- Replace model, model-family, variant, and manufacturer references with generic capability or runtime-context language, or remove them when no operational content remains.
- Convert exclusive tool and service names into descriptive abstract capability names.
- Preserve tool contracts but use abstract field names only where source field names encode a proprietary integration. Preserve type, requiredness, limits, and behavior.
- Convert source configuration locations and instruction-file names to terms such as `<host-config>`, `<project-instructions>`, `<memory-dir>`, `<artifact-service>`, and `<remote-trigger-service>`.
- Convert source-host web domains, APIs, login methods, hosted services, and UI features into abstract services or host capabilities.
- Remove source-specific commit attribution and generated-by footers rather than replacing them with a new attribution.
- Preserve security, authorization, failure handling, retries, user communication, task state, verification, and completion distinctions.

### Runtime Data Rules

Keep the structural context fields but replace concrete values with `<...>` placeholders. This applies to user identity, email, local paths, working directory, operating system, shell, model runtime data, dates, Git status, branch names, commit history, project instruction content, and similar source-session facts.

Placeholders represent host-provided context, not literal requirements for a host implementation.

### Traceability

Implementation must add a machine-readable or reviewable mapping that records, for every transformed or removed source block:

- source heading or line range;
- transformation outcome;
- target heading or line range where applicable;
- replacement category and terms;
- concise rationale.

Unchanged portable blocks need not be individually recorded when a contiguous source range is explicitly declared preserved.

## Functional Requirements

- **FR-001:** The target must preserve all source functional sections in source order unless a section is removed under the approved removal rule.
- **FR-002:** The target must preserve source rules for security, authorization, communication, memory, context, artifacts, delegation, planning, workspaces, monitoring, tasks, scheduling, research, file operations, command execution, version control, workflows, failure, retry, and verification.
- **FR-003:** Mixed proprietary and useful rules must be generalized, not deleted.
- **FR-004:** Source-exclusive tool, service, path, schema, and integration references must become abstract capabilities or placeholders.
- **FR-005:** Source-specific identity, manufacturer, agent, model, family, variant, model identifier, product URL, account detail, local path, personal identifier, runtime snapshot, automatic attribution, and vendor marketing must be absent from the target.
- **FR-006:** Every concrete source-session datum must be replaced by a placeholder while retaining its structural role.
- **FR-007:** The target must not introduce unrelated operational content or external dependencies.
- **FR-008:** A transformation map must explain every generalized, placeholder-substituted, and removed block.
- **FR-009:** Validation must use only the standard library and produce actionable failures.

## Validation Requirements

Add deterministic validation that checks:

1. the target exists and is non-empty;
2. required source functional headings or their documented generic equivalents are present in source order;
3. the transformation mapping covers every non-preserved source block;
4. prohibited source-specific terms and variants do not appear in the target or mapping except as non-operational source locators when unavoidable;
5. no source personal data, exact local paths, session values, or repository snapshot values appear in the target;
6. runtime-context sections use `<...>` placeholders;
7. each source capability family remains represented after transformation;
8. the validator reports the missing heading, prohibited term, uncovered range, or invalid placeholder.

Manual review must compare each generalized block to the source and confirm that its operating rule, boundary, and state distinction survived the transformation.

## Acceptance Scenarios

1. Given a source sentence that combines a source-host tool name with a useful instruction, when transformed, then the target uses an abstract capability name and preserves the instruction.
2. Given a source section that advertises or compares source models, when transformed, then the target removes that section without replacing it with marketing.
3. Given a source session-context block with personal or environmental values, when transformed, then the target preserves its fields using generic placeholders.
4. Given a source tool schema with provider-specific integration fields, when transformed, then the target preserves the contract semantics without requiring the provider's field names or service.
5. Given the finished target, when validation runs, then it rejects leaked identity, model, manufacturer, product, URL, path, user, email, or source-session values.
6. Given the finished target, when a reviewer compares functional headings, then every source capability family is present in the same order or has a documented removal rationale.

## Success Criteria

- `prompts/system-prompt.md` is a single source-derived Markdown prompt.
- Useful source content is preserved or semantically generalized; only non-portable identity or promotional material is removed.
- No source-specific agent, model, manufacturer, product, service, path, account, or session value leaks into the target.
- All source capability families, state distinctions, and lifecycle rules remain reviewable in the target.
- The mapping makes every non-literal transformation auditable.
- Automated validation passes and manual review finds no untracked omission or prohibited coupling.

## Constitution Check

- [x] Uses one target prompt and minimal supporting validation.
- [x] Avoids a new runtime, adapter layer, or dependency.
- [x] Preserves source behavior rather than creating unrelated abstractions.
- [x] Makes destructive and external-action boundaries verifiable.
- [x] Protects personal and environment-specific source data.
