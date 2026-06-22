---
name: dry
description: >-
  A comprehensive Hermes skill covering the DRY (Don't Repeat Yourself)
  principle — origins, formal definition, types of duplication, when to apply
  and when not, relationships with other principles (KISS, YAGNI, SPOT),
  practical TypeScript/JavaScript examples, common pitfalls, detection tools,
  and authoritative references.
version: 1.0.0
author: Hermes Agent (curated from Hunt & Thomas, The Pragmatic Programmer)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [dry, don-t-repeat-yourself, pragmatic-programmer, code-quality, refactoring, software-design, best-practices]
    related_skills: [design-skill]
---

# DRY (Don't Repeat Yourself)

## 1. Origin & Authors

The DRY principle was coined by **Andrew Hunt** and **David Thomas** in their seminal book *The Pragmatic Programmer: From Journeyman to Master* (Addison-Wesley, 1999). Both Hunt and Thomas are signatories of the Agile Manifesto (2001).

- **Book:** *The Pragmatic Programmer* — Chapter 2, "A Pragmatic Approach", section *"The Evils of Duplication"*.
- **2nd Edition:** Released in 2019 with updated examples; the core principle remains unchanged.
- **Tip #11 (1st ed.) / Tip #14 (2nd ed.):**

> *"Every piece of knowledge must have a single, unambiguous, authoritative representation within a system."*

---

## 2. Formal Definition

**Canonical definition** (Hunt & Thomas, 1999):

> *"Every piece of knowledge must have a single, unambiguous, authoritative representation within a system."*

**Wikipedia definition:**

> *"A principle of software development aimed at reducing repetition of information which is likely to change, replacing it with abstractions that are less likely to change, or using data normalization which avoids redundancy in the first place."*

**From the 2003 Artima interview (Hunt & Thomas):**

> *"When you have duplication, you have two representations of the same thing, and they can get out of sync. The result is bugs. So DRY is really about trying to make sure that every piece of knowledge in your system is represented once and only once."*

> **Crucial nuance:** DRY is about **knowledge**, not about code text. Two textually identical code snippets that represent *different* domain concepts do NOT violate DRY.

---

## 3. Types of Duplication

### Hunt & Thomas's Four Types

| Type | Description | Solution |
|------|-------------|----------|
| **Imposed** | Environment forces repetition (e.g., schema in DB + Java classes + docs) | Code generators, doc from source |
| **Inadvertent** | Developers unaware they are duplicating (e.g., same validation by two people) | Communication, code review, detection tools |
| **Impatient** | Deadline pressure → copy-paste shortcuts | Discipline, immediate refactoring, tech debt tickets |
| **Inter-developer** | Multiple devs on same project create overlapping features unknowingly | Clear architecture, strong tech lead, well-defined modules |

### Academic Clone Taxonomy (Four Types)

| Type | Name | Description |
|------|------|-------------|
| Type 1 | Exact clones | Identical except whitespace/comments |
| Type 2 | Renamed clones | Syntactically identical, identifiers renamed |
| Type 3 | Near-miss clones | Copies with minor insertions/deletions/modifications |
| Type 4 | Semantic clones | Syntactically different but functionally equivalent |

---

## 4. When to Apply & When NOT

### ✅ Apply DRY when:

- Same **business logic** is replicated across services/files
- Configurations and constants (URLs, API keys, thresholds)
- Data schemas for the same entity
- Identical validations for the **same domain concept**
- Repetitive data transformations (parsing, serialization, formatting)
- Test setup (fixtures, helpers, factories)

### ❌ Avoid / Delay DRY when:

- Code looks similar but represents **different domain concepts** that could change independently (incidental/accidental duplication)
- Requirements are still unstable (prototypes, MVPs, experimental code)
- Abstraction would require many parameters, flags, or conditionals
- Performance-critical path (abstraction overhead matters)

### Rule of Three

Attributed to **Don Roberts** and popularized by **Martin Fowler** (*Refactoring*, 1999):

> *"The first time you do something, you just do it. The second time you do something similar, you wince at the duplication, but you do the duplicate anyway. The third time you do something similar, you refactor."*

| Occurrence | Action |
|------------|--------|
| 1st time | Just write it |
| 2nd time | Accept duplication, stay alert |
| 3rd time | Refactor into abstraction |

### AHA Principle (Avoid Hasty Abstractions)

Coined by **Kent C. Dodds**, the AHA principle prioritizes explicit code over premature abstractions. It complements DRY: don't abstract too early.

### Quick Decision Guide

| Question | Decision |
|----------|----------|
| Does this represent the **same** business knowledge? | ✅ Abstract |
| Would these change **together** under the same requirement? | ✅ Abstract |
| Is this **coincidentally** similar (different domains)? | ❌ Keep separate |
| Not sure if they'd change together? | ❌ Wait (apply Rule of Three) |

---

## 5. Relationship with Other Principles

| Principle | Relationship with DRY |
|-----------|----------------------|
| **KISS** (Keep It Simple, Stupid) | Often conflicts — if a DRY abstraction makes code *less* simple, duplication is preferable |
| **YAGNI** (You Ain't Gonna Need It) | "Don't abstract for futures you don't know about (YAGNI), but don't duplicate knowledge you already have (DRY)" |
| **SPOT** (Single Point of Truth, Gerard J. Holzmann, IEEE 2015) | Focus on **information/data** rather than knowledge; SPOT = DRY applied to data and state |
| **Separation of Concerns (SoC)** | Complementary: SoC divides the system, DRY ensures each concern is declared once |
| **Orthogonality** (Hunt & Thomas) | DRY = each knowledge in one place; Orthogonality = each component independent. Together they make change safe |
| **SOLID** | S (Single Responsibility) aligns with DRY; O (Open/Closed) — DRY avoids modifying multiple places; D (Dependency Inversion) + DRY = effective reuse |
| **Data Normalization** (3NF, BCNF) | DRY applied to databases — each atomic fact in one table, avoid redundancy |

---

## 6. Practical Code Examples (Before / After)

### Example 1: Magic Constants (Obvious DRY)

**Before (WET):** The same magic number `0.15` scattered across files meaning different things.

```typescript
// order-service.ts
const discount = price * 0.15;

// tax-service.ts
const tax = subtotal * 0.15;

// shipping-service.ts
const freeShipping = total > 0.15 * 100;  // what does 0.15 mean here?
```

**After (DRY):** Named constants with explicit intent.

```typescript
// config/rates.ts
export const DISCOUNT_RATE = 0.15;
export const TAX_RATE = 0.15;
export const FREE_SHIPPING_MULTIPLIER = 0.15;

// order-service.ts
import { DISCOUNT_RATE } from './config/rates';
const discount = price * DISCOUNT_RATE;

// tax-service.ts
import { TAX_RATE } from './config/rates';
const tax = subtotal * TAX_RATE;
```

### Example 2: Input Validation (Correct DRY)

**Before:** Email validation logic duplicated across services.

```typescript
// user-service.ts
function createUser(email: string) {
  if (!email.includes('@') || !email.includes('.')) {
    throw new Error('Invalid email');
  }
  // ...
}

// order-service.ts
function createOrder(email: string) {
  if (!email.includes('@') || !email.includes('.')) {
    throw new Error('Invalid email');
  }
  // ...
}
```

**After:** Extracted shared validation.

```typescript
// validators.ts
export function isValidEmail(email: string): boolean {
  return email.includes('@') && email.includes('.');
}

// user-service.ts
import { isValidEmail } from './validators';
function createUser(email: string) {
  if (!isValidEmail(email)) throw new Error('Invalid email');
  // ...
}

// order-service.ts
import { isValidEmail } from './validators';
function createOrder(email: string) {
  if (!isValidEmail(email)) throw new Error('Invalid email');
  // ...
}
```

### Example 3: When NOT to DRY (Accidental Duplication)

Two functions that look similar textually but represent fundamentally different domain concepts.

```typescript
// loan.ts — PRICE amortization system
function calculateMonthlyPayment(principal: number, annualRate: number, months: number): number {
  const monthlyRate = annualRate / 12 / 100;
  return principal * (monthlyRate * Math.pow(1 + monthlyRate, months)) / (Math.pow(1 + monthlyRate, months) - 1);
}

// investment.ts — compound interest projection
function calculateMonthlyReturn(invested: number, annualRate: number, months: number): number {
  const monthlyRate = annualRate / 12 / 100;
  return invested * Math.pow(1 + monthlyRate, months);
}
```

`annualRate / 12 / 100` appears in both, but loan amortization and investment return calculations belong to different domains and may diverge independently. **Do NOT abstract** — the textual similarity is coincidental.

### Example 4: Test Parametrization (Beneficial DRY)

**Before:** Three separate test functions.

```typescript
describe('DiscountService', () => {
  it('should apply 10% discount for premium customers', () => {
    const result = applyDiscount('premium', 100);
    expect(result).toBe(90);
  });

  it('should apply 5% discount for regular customers', () => {
    const result = applyDiscount('regular', 100);
    expect(result).toBe(95);
  });

  it('should apply 0% discount for basic customers', () => {
    const result = applyDiscount('basic', 100);
    expect(result).toBe(100);
  });
});
```

**After:** Parameterized test (e.g., using `test.each` in Vitest/Jest).

```typescript
describe('DiscountService', () => {
  it.each([
    ['premium', 100, 90],
    ['regular', 100, 95],
    ['basic', 100, 100],
  ])('should apply correct discount for %s customers', (tier, amount, expected) => {
    const result = applyDiscount(tier, amount);
    expect(result).toBe(expected);
  });
});
```

### Example 5: Utility Functions (Beneficial DRY)

**Before:** Three near-identical currency formatters scattered across the codebase.

```typescript
// file1.ts
function formatCurrency(amount: number): string {
  return `$${amount.toFixed(2)}`;
}

// file2.ts
function formatMoney(amount: number): string {
  return `$${amount.toFixed(2)}`;
}

// file3.ts
function displayPrice(price: number): string {
  return `$${price.toFixed(2)}`;
}
```

**After:** A single, localized utility function.

```typescript
// utils/currency.ts
export function formatCurrency(amount: number, locale = 'en-US', currency = 'USD'): string {
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency,
  }).format(amount);
}
```

---

## 7. Common Pitfalls

| # | Pitfall | Symptom | Correction |
|---|---------|---------|------------|
| 1 | **Premature abstraction** | Creating generic functions/classes "just in case" with only 2 instances | Wait for 3 occurrences (Rule of Three) |
| 2 | **Over-DRYing** | Extracting every duplicated line → deep indirection layers, impossible to follow | Apply KISS; if abstraction hurts readability, don't do it |
| 3 | **Ignoring DRY (Impatient)** | "I'll copy-paste now, refactor later" — later never comes | Refactor immediately or create a high-priority tech debt ticket |
| 4 | **Wrong abstraction level** | Identifying duplication but abstracting at wrong granularity | Create specific functions (`validateEmail`, `validateCPF`) sharing only what's necessary |
| 5 | **DRY in wrong layer** | Frontend and backend both validate same rule independently | Use a shared library or make backend the single source of truth |
| 6 | **Coupling through abstraction** | Two unrelated services share a function → a change in one breaks the other | Keep unrelated domains decoupled; duplication is cheaper than false coupling |
| 7 | **DRY for configuration** | Treating environment-specific config as shared DRY code | Use environment variables or per-environment config files |

---

## 8. Detection Tools

| Tool | Type | Languages | Clone Types | Cost | CI/CD |
|------|------|-----------|-------------|------|-------|
| **CPD (PMD)** | CLI / Build plugin | 20+ (Java, C#, Go, Ruby, PHP, etc.) | Type 1-2, partial Type 3 | Free | ✅ |
| **SonarQube** | Platform | 30+ | Type 1-2, partial Type 3 | Free / Enterprise | ✅ |
| **ESLint + sonarjs** | Linter plugin | JavaScript, TypeScript | Strings only | Free | ✅ |
| **jscpd** | CLI / MCP server | 223+ formats | Type 1-2, limited Type 3 | Free | ✅ |
| **CodeScene / CodeClimate** | SaaS | 20+ | Type 1-3 | Paid | ✅ |

### Key Commands

```bash
# CPD (PMD)
pmd cpd --minimum-tokens 100 --files /src --language typescript

# jscpd
npx jscpd /path/to/src

# ESLint sonarjs (install first)
npm install eslint-plugin-sonarjs --save-dev
# Rule: sonarjs/no-duplicate-string
```

---

## 9. References

### Books

1. **Hunt, A.; Thomas, D.** *The Pragmatic Programmer.* Addison-Wesley, 1999. ISBN: 0-201-61622-X.
2. **Hunt, A.; Thomas, D.** *The Pragmatic Programmer, 2nd Edition.* Addison-Wesley, 2019. ISBN: 978-0135957059.
3. **Fowler, M.** *Refactoring: Improving the Design of Existing Code.* Addison-Wesley, 1999.
4. **Martin, R. C.** *Clean Code.* Prentice Hall, 2008.

### Author Interviews

5. **Hunt & Thomas.** "Orthogonality and the DRY Principle." Artima, 2003. → [https://www.artima.com/articles/orthogonality-and-the-dry-principle](https://www.artima.com/articles/orthogonality-and-the-dry-principle)

### Wikipedia

6. Don't repeat yourself: [https://en.wikipedia.org/wiki/Don%27t_repeat_yourself](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)
7. Rule of three: [https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming)](https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming))
8. Single source of truth: [https://en.wikipedia.org/wiki/Single_source_of_truth](https://en.wikipedia.org/wiki/Single_source_of_truth)

### Academic Papers

9. **Sajnani, Saini & Lopes (2014).** "A Comparative Study of Bug Patterns in Java Cloned and Non-cloned Code." IEEE SCAM. DOI: 10.1109/SCAM.2014.12.
10. **Rahman & Roy (2017).** "Comparing Software Bugs in Clone and Non-clone Code." IJSEKE. DOI: 10.1142/S0218194017400083.
11. **Holzmann (2015).** "Points of Truth." IEEE Software. DOI: 10.1109/MS.2015.103.
12. **(2024).** "An empirical study of code clones: Density, entropy, and patterns." ScienceDirect.
13. **(2026).** "An Empirical Study on the Characteristics of Reusable Code Clones." ACM Digital Library.

### Blog Posts & Articles

14. **Google Testing Blog (2024).** "Don't DRY Your Code Prematurely." Code Health Series.
15. **The Valuable Dev.** "The DRY Principle: Benefits and Costs with Examples."
16. **Sciamanna, A. (2018).** "The DRY Principle and Incidental Duplication."
17. **InfoQ (2012).** "Using DRY: Between Code Duplication and High-Coupling."
18. **Erasmus, B. (2026).** "DRY Is About Knowledge, Not Just Code."

### Tool Documentation

19. **PMD CPD:** [https://pmd.github.io/pmd/pmd_userdocs_cpd.html](https://pmd.github.io/pmd/pmd_userdocs_cpd.html)
20. **SonarQube Duplications:** [https://docs.sonarsource.com/sonarqube/latest/user-guide/duplications/](https://docs.sonarsource.com/sonarqube/latest/user-guide/duplications/)
21. **jscpd:** [https://github.com/kucherenko/jscpd](https://github.com/kucherenko/jscpd)
22. **ESLint sonarjs:** [https://github.com/SonarSource/eslint-plugin-sonarjs](https://github.com/SonarSource/eslint-plugin-sonarjs)