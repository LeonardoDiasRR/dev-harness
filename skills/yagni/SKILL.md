---
name: yagni
tags: [agile, extreme-programming, software-design, principles, simplicity]
created: 2026-06-21
updated: 2026-06-21
---

# YAGNI (You Aren't Gonna Need It)

> *"Always implement things when you actually need them, never when you just foresee that you need them."* — **Ron Jeffries**

---

## Origin

YAGNI emerged in the late 1990s as a core principle of **Extreme Programming (XP)**, the agile methodology pioneered by **Kent Beck** during the **Chrysler Comprehensive Compensation System (C3)** project (1996–1999).

| Contributor | Role | Key Work |
|---|---|---|
| **Kent Beck** | Creator of XP; formalized YAGNI in Simple Design | *Extreme Programming Explained: Embrace Change* (1st ed. 1999, Ch. 17) |
| **Ron Jeffries** | XP co-founder; coined the phrase and wrote the definitive article | *"You're NOT gonna need it!"* (XProgramming.com, April 4, 1998) |
| **Ann Anderson & Chet Hendrickson** | XP practitioners who expanded the concept alongside DTSTTCPW | *Extreme Programming Installed* (2000) |

Beck incorporated YAGNI as one of the four rules of **Simple Design** in XP:

1. Pass all tests
2. Reveal intent (expressive code)
3. No duplication (DRY)
4. Minimum number of classes and methods — where YAGNI directly acts

---

## Definition

**YAGNI (You Aren't Gonna Need It)** is a software design principle that states: **do not add functionality, abstraction, configuration, or complexity until there is a real, present need for it.**

### Formal Definitions

| Source | Definition |
|---|---|
| **Ron Jeffries** (1998) | *"Always implement things when you actually need them, never when you just foresee that you need them."* |
| **Martin Fowler** (2015) | *"Yagni is a strategy to avoid building capabilities into software to support a presumptive feature. It only applies to capabilities that introduce extra complexity now that you won't take advantage of until later."* |

### Levels of Application

| Level | Scope | Example |
|---|---|---|
| **Code** | Functions, classes, parameters | Don't create a generic method when only one specific case is needed |
| **Architecture** | Systems, services, infrastructure | Don't adopt microservices when a monolith suffices |
| **Product** | Features, modules | Don't build "advanced reporting" if the MVP needs a simple list |

---

## Empirical Evidence (Standish CHAOS Report)

### Standish Group CHAOS Report

The Standish Group has collected data since 1994 on feature usage in software projects:

| Category | Percentage | Description |
|---|---|---|
| **Always used** | 7% | Features used on every execution |
| **Frequently used** | 13% | Features used on most executions |
| **Sometimes used** | 16% | Features used occasionally |
| **Rarely used** | 19% | Features used rarely |
| **Never used** | **45%** | Features that were never used |

**Key finding (2002): 64% of features are rarely or never used.**

- A **Pendo (2019)** study raised this to **80%** in enterprise SaaS applications.
- Only **~20% of features deliver ~80% of value** (Pareto Principle).

### Cost of Dead Code

Maintaining speculative code carries measurable costs:

1. **Cognitive cost** — developers waste time understanding unused code
2. **Build/compilation cost** — extra code increases build time and artifact size
3. **Testing cost** — dead code must be covered or generates false coverage positives
4. **Refactoring cost** — dead code creates dependencies that must be maintained
5. **Technical debt** — estimates (e.g., Steve McConnell, *Code Complete*) suggest dead code adds 20–40% to total maintenance cost over a system's lifetime

---

## When to Apply & When NOT

### ✅ When to Apply YAGNI

1. **Projects with volatile requirements** — frequent changes make prediction futile
2. **MVP / early-stage products** — focus on validating hypotheses, not building infrastructure
3. **Low-priority backlog items** — if it's not in the current sprint, don't implement
4. **Internal code without public API** — easier to refactor later
5. **Speculative features** ("maybe someday...") — ask if the business would pay for it today
6. **Premature optimization** — Knuth: *"Premature optimization is the root of all evil"*

**Decision techniques:** MVP, Cost of Delay (CoD), Weighted Shortest Job First (WSJF), User Story Mapping, Impact Mapping, Real-need test ("Does this solve a problem a real user has today?"), Data-driven usage analysis.

### ❌ When NOT to Apply YAGNI

1. **Irreversible architectural decisions** — high reversal cost warrants some upfront planning:
   - Database selection (SQL ↔ NoSQL migration is expensive)
   - Platform/deployment choices (cloud provider, containerization, OS)
   - Public data structures / API contracts (once published, breaking changes are costly)

2. **Security and compliance requirements:**
   - Audit trails, data protection (LGPD/GDPR), access control
   - Retrofitting security is often more expensive

3. **Fundamental performance constraints** — non-negotiable performance requirements from the start

4. **Martin Fowler's exception:** YAGNI does NOT apply when adding something for the future that **does not increase complexity**:

   > *"If you do something for a future need that doesn't actually increase the complexity of the software, then there's no reason to invoke yagni."*
   >
   > — Martin Fowler, "Yagni" (bliki, 2015)

   Example: naming a variable clearly for readability — adds no complexity, improves future maintainability.

---

## Relationship with KISS / DRY / DTSTTCPW

### YAGNI ↔ KISS (Keep It Simple, Stupid)

| Aspect | YAGNI | KISS |
|---|---|---|
| **Focus** | Timing — *when* to implement | Complexity — *how* to implement |
| **Question** | "Do we need this now?" | "Can we do this more simply?" |
| **Relationship** | Complementary: YAGNI removes unnecessary scope; KISS ensures simple implementation of what remains |

### YAGNI ↔ DRY (Don't Repeat Yourself)

These can conflict when misapplied:

- **DRY misapplied:** creating premature generic abstractions to eliminate duplication that doesn't yet exist → violates YAGNI
- **YAGNI tempered with DRY:** eliminate *real* (already existing) duplication; don't add speculative abstractions

**Reconciliation — The Rule of Three:** Only generalize when the same pattern appears **three times**. Tolerate some temporary duplication rather than introduce premature abstractions (Joshua Kerievsky, *Refactoring to Patterns*).

### YAGNI ↔ DTSTTCPW (Do The Simplest Thing That Could Possibly Work)

- **DTSTTCPW** asks: "What is the simplest implementation that passes the tests?"
- **YAGNI** asks: "Do we really need this at all?"
- Together, they form the foundation of XP's **Simple Design** philosophy.

### YAGNI ↔ SOLID

| SOLID Principle | Relationship with YAGNI |
|---|---|
| **SRP** (Single Responsibility) | YAGNI prevents classes from having speculative responsibilities |
| **OCP** (Open/Closed) | YAGNI warns against premature extensibility preparation |
| **LSP** (Liskov Substitution) | YAGNI avoids speculative inheritance hierarchies |
| **ISP** (Interface Segregation) | YAGNI prevents bloated interfaces with unnecessary methods |
| **DIP** (Dependency Inversion) | YAGNI warns against abstracting dependencies that never vary |

---

## Practical Code Examples

### Example 1: Generic Dialog Box (Kent Beck's classic)

**Scenario:** Programmer needs to display *"File saved successfully."*

❌ **YAGNI violation:** Creates a generic `DialogBox` class with customizable titles, icons, configurable buttons, flexible layout, themes — "in case someone else needs it."

```python
class DialogBox:
    def __init__(self, title, message, icon, buttons, layout, theme):
        ...
```

✅ **YAGNI applied:**

```python
alert("File saved successfully")
```

Refactor when a second dialog case arises.

### Example 2: Repository Abstraction

**Scenario:** Simple user CRUD against an SQL database.

❌ **YAGNI violation:** Creates interface `UserRepository`, implementations `SqlUserRepository`, `InMemoryUserRepository` (for tests that don't exist yet), `CachedUserRepository`, plus a factory.

```python
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, id): ...

class SqlUserRepository(UserRepository): ...
class InMemoryUserRepository(UserRepository): ...
class CachedUserRepository(UserRepository): ...
```

✅ **YAGNI applied:**

```python
class UserRepository:
    def find_by_id(self, id):
        # Direct SQL implementation
        ...
```

Extract an interface later via IDE refactoring when a second implementation is actually needed.

### Example 3: Premature Microservices

**Scenario:** A 3-person team, <1000 users/day.

❌ **YAGNI violation:** Kubernetes, service mesh, API gateway, message queues, separate deployment per service.

✅ **YAGNI applied:** Well-structured modular monolith. Extract services only when proven necessary (scale issues, team growth, independent deployment needs).

> *"When I see an architecture for an enterprise app with Kubernetes and Docker, the first thought that pops into my head is YAGNI."*
> — Martin Fowler, *Is Design Dead?* (2004)

### Example 4: Unnecessary Strategy Pattern

**Scenario:** Only credit card payment is in the backlog.

❌ **YAGNI violation:** Interface `PaymentStrategy` with `CreditCardPayment`, `DebitCardPayment`, `PayPalPayment`, `PixPayment`, `BoletoPayment` — for speculative future needs.

✅ **YAGNI applied:**

```python
def process_credit_card_payment(amount, card_number):
    ...
```

Add new payment methods when they become real requirements.

### Example 5: Plugin / Configuration System

**Scenario:** Internal app needs to display data in a table.

❌ **YAGNI violation:** Plugin system for different views, template engine, external JSON config, hot-reload configuration.

✅ **YAGNI applied:** Render the table directly in code. Refactor when a second view type emerges.

---

## Anti-patterns

### Speculative Generality (Martin Fowler's code smell)

Creating hooks, parameters, abstractions, and configuration options for hypothetical generalizations that never materialize.

**Symptoms:**
- Interfaces with only one concrete implementation, no realistic prospect of a second
- Methods with unused parameters ("just in case")
- Abstract base classes with a single subclass
- Configuration flags for behaviors that never change
- "Framework-itis": building generic frameworks where simple functions would suffice

### Gold Plating

Adding features, polish, or capabilities beyond what was requested to "beautify" or "future-proof" the product — often driven by developer pride rather than user need.

**Symptoms:**
- Features that "would be cool to have" but no user asked for
- Over-engineered UI with animations and transitions on an internal tool
- Excessive error handling for edge cases that have never occurred and have zero impact

### Other Related Anti-patterns

| Anti-pattern | Description |
|---|---|
| **Boat Anchor** | Keeping a component/system that has no use "just in case" |
| **Debugging the Void** | Implementing and testing scenarios that will never occur |
| **Framework-itis** | Building homegrown frameworks instead of using simple functions or libraries |

### Violation Indicators

Watch for these phrases during code review:

- *"While we have the hood open..."*
- *"This will be useful when..."*
- *"We might as well set it up for..."*
- *"Better to create an interface/abstraction because..."*
- *"One day we'll need..."*

---

## References

### Books

1. **BECK, Kent.** *Extreme Programming Explained: Embrace Change*. 1st ed. Addison-Wesley, 1999. (Ch. 17 — "YAGNI")
2. **BECK, Kent.** *Extreme Programming Explained: Embrace Change*. 2nd ed. Addison-Wesley, 2004.
3. **JEFFRIES, Ron; ANDERSON, Ann; HENDRIKSON, Chet.** *Extreme Programming Installed*. Addison-Wesley, 2000.
4. **SHORE, James; WARDEN, Shane.** *The Art of Agile Development*. 1st ed. O'Reilly, 2007.
5. **SHORE, James.** *The Art of Agile Development*. 2nd ed. O'Reilly, 2021.
6. **FEATHERS, Michael.** *Working Effectively with Legacy Code*. Prentice Hall, 2004.
7. **KERIEVSKY, Joshua.** *Refactoring to Patterns*. Addison-Wesley, 2004.
8. **FOWLER, Martin.** *Refactoring: Improving the Design of Existing Code*. 2nd ed. Addison-Wesley, 2018.
9. **McCONNELL, Steve.** *Code Complete*. 2nd ed. Microsoft Press, 2004.
10. **BLOCH, Joshua.** *Effective Java*. 3rd ed. Addison-Wesley, 2018.

### Articles & Online Publications

11. **JEFFRIES, Ron.** "You're NOT gonna need it!" XProgramming.com, 4 Apr 1998. https://ronjeffries.com/xprog/articles/practices/pracnotneed/
12. **JEFFRIES, Ron.** "YAGNI, yes. Skimping, no. Technical Debt? Not even." RonJeffries.com, 2 Apr 2019. https://ronjeffries.com/articles/019-01ff/iter-yagni-skimp/
13. **FOWLER, Martin.** "Yagni". MartinFowler.com (bliki), 26 May 2015. https://martinfowler.com/bliki/Yagni.html
14. **FOWLER, Martin.** "Is Design Dead?" MartinFowler.com, 2004. https://martinfowler.com/articles/designDead.html

### Research Reports

15. **STANDISH GROUP.** *CHAOS Report*. 1994–2024. (Especially 2002 edition with feature usage data)
16. **PENDO.** *Product Benchmarks Report 2019*. (80% of features unused in SaaS)

### Technical & Web

17. **Wikipedia.** "You aren't gonna need it". https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it
18. **Wiki C2.** "Xp Yagni Pitfalls". https://wiki.c2.com/?XpYagniPitfalls
19. **FOWLER, Martin.** "Speculative Generality". In: *Refactoring* (catalog of code smells).

---

*Created from the research document at `/tmp/yagni-resumo.md` (June 21, 2026).*