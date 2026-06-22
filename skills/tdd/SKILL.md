---
name: tdd
description: >-
  A comprehensive Hermes skill covering Test-Driven Development (TDD) —
  origins (Kent Beck), definition and the Red-Green-Refactor cycle, Test
  Pyramid vs. Test Trophy, Frontend TDD with React Testing Library and Vitest,
  Backend TDD with mocks/stubs/fakes (Fowler taxonomy), FIRST and AAA patterns,
  empirical studies (Nagappan Microsoft/IBM), anti-patterns and test smells,
  mock vs. integration guidelines, and authoritative references.
version: 1.0.0
author: Hermes Agent (curated from Kent Beck, Martin Fowler, Robert C. Martin, Gerard Meszaros, Kent C. Dodds, et al.)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [tdd, test-driven-development, testing, red-green-refactor, react-testing-library, vitest, unittest, integration-test, mock, stub, fake, test-pyramid, test-trophy, quality, software-design, best-practices]
    related_skills: [dry, yagni, kiss, design-skill]
---

# TDD (Test-Driven Development)

## 1. Origin

### Kent Beck — *Test-Driven Development: By Example* (2002)

Kent Beck, creator of Extreme Programming (XP), formalized TDD in the early 2000s.
The book's subtitle — *"Clean code that works"* — captures TDD's core promise.

**Core ideas:**

- **The test paradox:** _"Test the program before writing it"_ — write tests *first* to resolve the tension that testing is necessary but laborious.
- **Fear → confidence:** TDD converts the fear of introducing bugs into confidence to refactor and evolve code.
- **Loose coupling:** TDD forces early discovery that highly interdependent code is painful to test, incentivizing decoupled design.
- **Requirements before code:** Writing the test first forces thinking about expected behavior before implementation.

**Iconic quote:**

> *"Tests should be coupled to the behavior of the code and decoupled from the structure of the code."* — Kent Beck

### Supporting Works

- **GOOS (Freeman & Pryce, 2009)** — *Growing Object-Oriented Software, Guided by Tests*: Uses TDD to drive OO design; advocates the *mockist* (London School) approach; introduces "Walking Skeleton" and "listen to your tests."
- **Jay Fields (2014)** — *Working Effectively with Unit Tests*: Focuses on test *maintainability*; introduces the *Solitary vs. Sociable* test distinction; argues that tests that don't boost productivity should be deleted.
- **Robert C. Martin (Uncle Bob)** — *Clean Code* (Chapter 9): Formalizes The Three Laws of TDD.

---

## 2. Definition & Red-Green-Refactor

### Definition

**TDD** is a software development process where automated tests are written *before* production code. It is fundamentally a **design** technique — tests guide code structure, not merely verify correctness.

> **Write a failing test → Make it pass with minimal code → Refactor**

### The Three Laws of TDD (Robert C. Martin)

1. Do not write production code until you have a failing unit test.
2. Do not write more of a unit test than enough to fail (not compiling is failing).
3. Do not write more production code than enough to make the failing test pass.

### The Red-Green-Refactor Cycle

| Phase | Goal | Key Actions |
|-------|------|-------------|
| **RED** | Write a failing test | Think of desired behavior; write a small, focused test; run it to confirm it fails (verifies no false positive and test framework works). |
| **GREEN** | Make it pass with minimal code | Write the simplest production code to pass; may use "fake it" (return constants), obvious implementation, or triangulation (multiple examples). |
| **REFACTOR** | Improve code without changing behavior | Remove duplication; improve naming; extract methods; restructure. No new functionality added. The test suite protects against regressions. |

### Beck's 5-Step Expanded Version

1. **List** — Write a list of test scenarios (expected behaviors).
2. **Write a test** — Pick one item and write the test.
3. **Make it compile** — Create enough production code to compile.
4. **Make it pass** — Get the test to green.
5. **Refactor** — Remove duplication and improve design.

---

## 3. Test Pyramid vs. Test Trophy

### Test Pyramid (Mike Cohn, 2009)

Introduced in *Succeeding with Agile*. Three layers:

```
        /\
       /  \     ← E2E Tests — few, slow (UI/browser, full integration)
      /    \
     /────────\
    /          \  ← Integration Tests — moderate quantity (service, API, contract, DB)
   /            \
  /──────────────\
   Unit Tests — many, fast (milliseconds), isolated
```

**Principles:**
- **Many unit tests** — broad base, fast, isolated.
- **Fewer integration tests** — medium layer, test component interactions.
- **Few E2E tests** — narrow top, slow but high-value for critical flows.

**Fowler refinement (2018):** The pyramid isn't about technology but about trade-offs between speed, confidence, and maintenance cost.

### Testing Trophy (Kent C. Dodds)

An alternative for modern JavaScript applications:

```
        ╔═══════════════╗
        ║  E2E Tests   ║  ← Some E2E tests
        ╚═══════════════╝
      ╔═══════════════════╗
      ║ Integration Tests ║  ← THE MAJORITY of tests
      ╚═══════════════════╝
   ╔═══════════════════════╗
   ║   Unit Tests         ║  ← Few unit tests
   ╚═══════════════════════╝
╔═══════════════════════════╗
║ Static Analysis (TS/ESLint) ║  ← Static analysis tooling
╚═══════════════════════════╝
```

**Key differences vs. Pyramid:**
- Integration tests give more confidence-per-test than pure unit tests.
- For React apps, most tests should be integration — render a component, interact via user events, verify DOM results.
- The trophy's base is **static analysis** (TypeScript, ESLint), preventing bugs without running code.

---

## 4. Frontend TDD (React Testing Library, Vitest)

### Philosophy — React Testing Library (RTL)

Created by Kent C. Dodds. Core mantra:

> *"The more your tests resemble the way your software is used, the more confidence they can give you."*

**Principles:**
- **Test behavior, not implementation** — no testing internal state, private methods, or implementation details.
- **Semantic queries by priority:**
  1. `getByRole` (accessibility) — most preferred
  2. `getByLabelText`
  3. `getByPlaceholderText`
  4. `getByText`
  5. `getByDisplayValue`
  6. `getByAltText`
  7. `getByTitle`
  8. `getByTestId` (last resort)
- **`userEvent` over `fireEvent`** — `userEvent` simulates real user interactions more realistically.

### Vitest (Modern Test Runner)

- Up to **20x faster** than Jest on large projects (uses Vite-native transformation).
- **Jest-compatible API** (trivial migration).
- **Native ESM support** — no extra config.
- **Hot Module Replacement (HMR)** for instant reload on test changes.
- Reuses Vite configuration (aliases, plugins, etc.).

### Practical Example (React + Vitest + RTL)

```typescript
// RED: Write the test first
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect } from 'vitest'
import Counter from './Counter'

describe('Counter', () => {
  it('should increment counter on button click', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<Counter />)
    // Act
    const button = screen.getByRole('button', { name: /increment/i })
    await user.click(button)
    // Assert
    expect(screen.getByText('1')).toBeInTheDocument()
  })
})

// GREEN: Minimal implementation
// function Counter() {
//   const [count, setCount] = useState(0)
//   return (
//     <div>
//       <p>{count}</p>
//       <button onClick={() => setCount(c => c + 1)}>Increment</button>
//     </div>
//   )
// }

// REFACTOR: Extract, rename, clean up...
```

---

## 5. Backend TDD (Mocks, Stubs, Fakes — Fowler Taxonomy)

### Test Doubles Taxonomy (Meszaros / Fowler)

Martin Fowler's *Mocks Aren't Stubs* (2007) popularized Gerard Meszaros's taxonomy:

| Type | Definition | Use |
|------|-----------|-----|
| **Dummy** | Object passed to fill a parameter but never used | Completing argument lists |
| **Fake** | Simplified functional implementation (e.g., in-memory DB) | Replace slow dependency with fast functional version |
| **Stub** | Returns pre-programmed responses for specific calls | Control what the SUT receives from dependencies |
| **Spy** | Stub that records information about how it was called | Verify how many times / with what arguments it was called |
| **Mock** | Object pre-programmed with interaction expectations | Verify interactions (London School) |

### London School (Mockist) vs. Detroit School (Classicist)

| Aspect | London School (Mockist) | Detroit School (Classicist) |
|--------|------------------------|----------------------------|
| **Approach** | Replace *all* dependencies with mocks | Use real objects when possible |
| **Verification** | Verify *interactions* between objects | Verify *final state*, not interactions |
| **Reference** | *GOOS* (Freeman & Pryce) | *TDD by Example* (Kent Beck) |
| **Advantage** | Full isolation, fast design feedback | Tests more resistant to refactoring |
| **Disadvantage** | Tests coupled to implementation | Difficult to set up complex fixtures |

### Backend Integration Testing Guidelines

**Use mocks when:**
- Dependencies are slow (network, external API, filesystem)
- Non-deterministic behavior (date/time, random)
- Hard-to-reproduce error scenarios (network failure, timeout)
- Setup cost for real environment is prohibitive

**Use real integration tests when:**
- Database (Testcontainers or in-memory DB)
- Message queues
- Internal APIs within the same service
- ORM mapping validation
- When the real test provides more confidence than the mock

**Mocking best practices:**
- Mock only what you own (not stable third-party libraries)
- Prefer functional fakes over heavyweight mocks
- Use interaction testing sparingly — prefer state testing
- Don't mock what you don't need to isolate

---

## 6. FIRST & AAA Patterns

### FIRST Principles (Robert C. Martin)

| Principle | Meaning | Why It Matters |
|-----------|---------|----------------|
| **F**ast | Tests must be fast (milliseconds) | If slow, they won't be run frequently |
| **I**solated / Independent | Tests must not depend on each other | One test should not set up state for another |
| **R**epeatable | Tests must produce the same result every time | Must not depend on environment, date/time, network |
| **S**elf-validating | Tests must have a binary result (pass/fail) | No manual log interpretation |
| **T**imely | Tests must be written at the right time (before code) | TDD: test first, code after |

### AAA Pattern (Arrange-Act-Assert)

Proposed by William Wake, popularized by Meszaros in *xUnit Test Patterns*.

```typescript
it('should calculate cart total with discount', () => {
  // ARRANGE — Set up the scenario
  const cart = new Cart()
  cart.addItem({ name: 'Product A', price: 100 })
  cart.addItem({ name: 'Product B', price: 50 })
  const discount = new PercentDiscount(10) // 10% off

  // ACT — Execute the action
  const total = cart.calculateTotal(discount)

  // ASSERT — Verify the result
  expect(total).toBe(135) // 150 - 15
})
```

**Benefits:**
- **Clarity** — each section has a specific purpose
- **Consistency** — all tests follow the same structure
- **Isolation** — separates setup, execution, and verification
- **Readability** — any developer understands the test flow

### Given-When-Then (BDD variant)

```
GIVEN a cart with 2 items
 WHEN a 10% discount is applied
 THEN the total should be 135
```

---

## 7. Empirical Studies

### Microsoft & IBM (Nagappan, Maximilien, Bhat, Williams — 2008)

- **Paper:** *"Realizing Quality Improvement Through Test Driven Development"*
- **Methodology:** Case studies with 3 Microsoft teams and 1 IBM team adopting TDD vs. similar non-TDD teams.

**Results:**

| Metric | Result |
|--------|--------|
| Pre-release defect density reduction | **40% to 90%** vs. similar non-TDD projects |
| Productivity impact | Small increase in development time (estimated 15–35%) |
| Participants | 4 industrial teams, real-world projects |

**Lessons:** TDD requires proper training; benefits are larger on projects with volatile requirements; design quality (cohesion, coupling) improves significantly.

### Meta-Analysis — Rafique & Mišić (2012)

- **Paper:** *"The Effects of TDD on External Quality and Productivity: A Meta-Analysis"* (IEEE)
- **Methodology:** Meta-analysis of **27 studies**.
- **Results:**
  - **External quality:** Significantly positive effect (fewer defects).
  - **Productivity:** Moderately negative (TDD is slower than Test-Last Development).

### Systematic Review — Bissi et al. (2016)

- **Paper:** *"The Effects of TDD on Internal Quality, External Quality and Productivity: A Systematic Review"* (Information and Software Technology)

**Results:**

| Aspect | % of studies showing benefit |
|--------|------------------------------|
| Internal code quality | ~76% of studies |
| External quality (fewer defects) | ~88% of studies |
| Productivity | ~44% showed lower productivity vs. TLD |

**Conclusion:** *"TDD produces more benefits than TLD for internal and external software quality, but results in lower developer productivity than TLD."*

### Synthesis Table

| Study | Year | Scope | Quality | Productivity |
|-------|------|-------|---------|--------------|
| Nagappan et al. (MS/IBM) | 2008 | 4 industrial teams | +40–90% (defect reduction) | −15–35% |
| Rafique & Mišić | 2012 | 27 studies (meta-analysis) | Significant improvement | Moderate reduction |
| Bissi et al. | 2016 | Systematic review | +76–88% | −44% of studies |

---

## 8. Anti-Patterns & Test Smells

Based on Gerard Meszaros's taxonomy (*xUnit Test Patterns*).

### Obscure Tests

| Anti-pattern | Description | Solution |
|-------------|-----------|---------|
| **Mystery Guest** | Test uses external data (files, DB) without clarity | Inline data builders, explicit factories |
| **Eager Test** | Test verifies multiple conditions/units at once | Split into smaller tests |
| **General Fixture** | Setup contains objects unnecessary for the test | Minimal, specific fixtures |
| **Indirect Testing** | Test interacts with SUT indirectly via another object | Test the SUT directly |
| **Irrelevant Information** | Setup data irrelevant to the test | Builders with sensible defaults |
| **Hard-Coded Test Data** | Magic values without context | Named constants, builders |

### Fragile Tests

| Anti-pattern | Description | Solution |
|-------------|-----------|---------|
| **Implementation Tests** | Testing internal details (private methods, internal state) | Test public behavior |
| **Over-Mocking** | Mocking everything, even non-isolated dependencies | Prefer real objects or fakes |
| **Fragile Fixture** | Environment changes break tests | Self-contained fixtures |
| **Flaky Tests** | Tests that pass/fail intermittently | Eliminate non-deterministic dependencies |
| **Assertion Roulette** | Multiple assertions without messages — hard to tell which failed | One logical assertion per test or descriptive messages |

### Behavioral

| Anti-pattern | Description | Solution |
|-------------|-----------|---------|
| **Conditional Logic in Tests** | `if/else`, loops, try/catch inside tests | Tests must be linear |
| **Tests That Never Fail** | Tautological tests (e.g., `expect(x).toBe(x)`) | Test real, known values |
| **Silent Tests** | Tests that pass but test nothing (no assertions) | Always assert something |
| **Living Documentation Tests** | Tests so complex they serve as documentation — and are fragile | Simplify, follow AAA |

### Organizational

| Anti-pattern | Description | Solution |
|-------------|-----------|---------|
| **The Iceberg** | 99% E2E, 1% unit tests | Invert the pyramid |
| **The Slow Poke** | Test suite that takes hours | Move slow tests to appropriate layer |
| **Local Hero** | Tests that only pass on the developer's machine | Eliminate environment dependencies |
| **Test Code Duplication** | Repeated setup across multiple tests | Extract helpers, factories, builders |
| **Conditional Test Logic** | Tests making different decisions based on conditions | Write deterministic tests |

---

## 9. Mock vs. Integration Guidelines

### When to Use Mocks ✅

- Dependency is slow (network, disk, remote DB)
- Dependency is non-deterministic (random, clock)
- Error scenario is hard to reproduce (timeout, network failure)
- Testing *interaction logic* (whether object A called the correct method on B)
- Following the London School (full unit isolation)

### When NOT to Use Mocks ❌

- Dependency is fast and deterministic
- Real implementation can be used without prohibitive cost
- The mock would make the test fragile to implementation changes
- Testing a system boundary (real integration is essential)

### When to Use Integration Tests ✅

- Component interaction is the main focus
- Need to verify ORM mapping correctness
- Business logic depends on persistent data (database)
- Testing an HTTP API
- The confidence gained is worth the extra setup cost

### Quick Decision Flowchart

```
Is the dependency slow, non-deterministic, or unavailable?
  ├─ Yes → Can I test the scenario with a Fake (functional)?
  │        ├─ Yes → Use Fake
  │        └─ No → Use Mock (interaction verify) or Stub (provide data)
  └─ No → Can I use the real implementation?
           ├─ Yes → Prefer real integration
           └─ Depends on cost → Evaluate trade-off
```

### Hybrid Strategies

- **Testcontainers** — disposable database containers for integration tests.
- **WireMock / MSW** — simulate external APIs in contract tests.
- **In-memory databases** (SQLite, H2) — as fakes for fast tests.
- **Port/Adapter (Hexagonal Architecture)** — interfaces allow swapping real implementations for fakes.

---

## 10. References

### Books

| Title | Author(s) | Year | ISBN |
|-------|-----------|------|------|
| *Test-Driven Development: By Example* | Kent Beck | 2002 | 0-321-14653-0 |
| *Growing Object-Oriented Software, Guided by Tests* | Steve Freeman, Nat Pryce | 2009 | 978-0321503626 |
| *Working Effectively with Unit Tests* | Jay Fields | 2014 | 978-1503242700 |
| *xUnit Test Patterns: Refactoring Test Code* | Gerard Meszaros | 2007 | 0-13-149505-4 |
| *Succeeding with Agile* | Mike Cohn | 2009 | 978-0321579362 |
| *Clean Code* (Chapter 9 — Tests) | Robert C. Martin | 2008 | 978-0132350884 |

### Papers

| Title | Author(s) | Year | Venue |
|-------|-----------|------|-------|
| *Realizing Quality Improvement Through Test Driven Development* | Nagappan, Maximilien, Bhat, Williams | 2008 | Empirical Software Engineering / Microsoft Research |
| *The Effects of TDD on External Quality and Productivity: A Meta-Analysis* | Rafique, Mišić | 2012 | IEEE Transactions on Software Engineering |
| *The Effects of TDD on Internal Quality, External Quality and Productivity: A Systematic Review* | Bissi, Sampaio, et al. | 2016 | Information and Software Technology |
| *Mocks Aren't Stubs* | Martin Fowler | 2007 | martinfowler.com/articles/mocksArentStubs.html |
| *Test Double* | Martin Fowler | 2006 | martinfowler.com/bliki/TestDouble.html |
| *The Practical Test Pyramid* | Martin Fowler (with Ham Vocke) | 2018 | martinfowler.com/articles/practical-test-pyramid.html |

### Online Resources

| Resource | URL | Description |
|----------|-----|-------------|
| React Testing Library | testing-library.com | Behavior-focused testing library |
| Vitest | vitest.dev | Modern test runner for Vite/ESM |
| Test Smell Catalog | test-smell-catalog.readthedocs.io | Open catalog of test anti-patterns |
| xUnit Patterns | xunitpatterns.com | Meszaros' book companion site |
| Kent C. Dodds — Testing Trophy | kentcdodds.com/blog/the-testing-trophy | Original trophy article |
| Google Testing Blog | testing.googleblog.com | Google's testing blog |