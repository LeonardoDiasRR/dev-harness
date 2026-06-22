---
name: ddd
description: >-
  A comprehensive Hermes skill covering Domain-Driven Design (DDD) —
  origins (Eric Evans, Vaughn Vernon), Strategic Design (Bounded Context,
  Context Map, Core/Supporting/Generic Subdomains), Tactical Design (Entity,
  Value Object, Aggregate, Domain Events, Repository, Domain Services),
  Ubiquitous Language, Anti-corruption Layer, Hexagonal Architecture,
  Anemic vs Rich Domain Model, DDD + Microservices, CQRS & Event Storming,
  and authoritative references.
version: 1.0.0
author: Hermes Agent (curated from Eric Evans, Vaughn Vernon, Alberto Brandolini, et al.)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ddd, domain-driven-design, strategic-design, tactical-design, bounded-context, context-map, ubiquitous-language, entity, value-object, aggregate, domain-events, repository, domain-service, anti-corruption-layer, hexagonal-architecture, ports-and-adapters, anemic-domain-model, rich-domain-model, cqrs, event-storming, microservices, software-architecture]
    related_skills: [tdd, hexagonal-architecture, cqrs, event-storming, microservices]
---

# DDD (Domain-Driven Design)

## 1. Origin

### Eric Evans — *Domain-Driven Design: Tackling Complexity in the Heart of Software* (2003)

Eric Evans formalized DDD in the seminal **"Blue Book"** (Addison-Wesley, ISBN 978-0321125217, ~560 pages). The book defines the *what* and *why* of DDD across four parts:

1. **Putting the Domain Model to Work** — why the domain model matters and how it drives design.
2. **Building Blocks of a Model-Driven Design** — the tactical building blocks (Entities, Value Objects, Aggregates, Repositories, Domain Services).
3. **Refactoring Toward Deeper Insight** — how to evolve the model as understanding deepens.
4. **Strategic Design** — Bounded Contexts, Context Maps, and large-scale structuring.

**Core principle:** Software should be built around a deep understanding of the business, with code structure reflecting the domain model's structure. DDD is not a technology or framework — it is a *way of thinking* that prioritizes domain knowledge over technical considerations.

> *"The heart of software is its ability to solve a user's problem."* — Eric Evans

### Vaughn Vernon — *Implementing Domain-Driven Design* (2013)

Vaughn Vernon authored the **"Red Book"** (Addison-Wesley, ISBN 978-0321834577, ~656 pages), which focuses on the *how* — practical implementation in Java/C# with real code examples covering:

- Strategic Design and Bounded Contexts
- Tactical Design implementation
- Aggregates design guidelines
- Domain Events and event-driven communication
- Integration between Bounded Contexts
- Domain-Driven Design with REST, messaging, and CQRS

### Supporting Works

- **Vaughn Vernon (2016)** — *Domain-Driven Design Distilled* (~176 pages, ISBN 978-0134434421): An accessible summary for beginners that introduces **Event Storming**.
- **Eric Evans (2014)** — *Domain-Driven Design Reference*: A concise reference of all DDD patterns.
- **Alberto Brandolini (2014)** — *Introducing Event Storming*: The foundational work on collaborative domain modeling workshops.

---

## 2. Strategic Design

Strategic Design handles how to organize and divide complex systems into manageable parts by defining boundaries and relationships across the entire problem space.

### Bounded Context

An explicit boundary within which a particular domain model is defined and applied. Each Bounded Context has its own **Ubiquitous Language** and its own model.

| Aspect | Description |
|--------|-------------|
| **Definition** | A semantic and organizational boundary around a domain model |
| **Language** | Each Bounded Context has its own Ubiquitous Language |
| **Example** | "Customer" means one thing to Sales, another to Support, another to Billing — each is a separate Bounded Context |
| **Microservices** | Each Bounded Context is a strong candidate for an independent microservice |
| **Ownership** | Typically owned by a single team |

### Context Map

A diagram describing the relationships between different Bounded Contexts. It visualizes boundaries, defines integration patterns, and identifies points of translation, sharing, or isolation.

**Relationship patterns between Bounded Contexts:**

| Pattern | Description |
|---------|-------------|
| **Partnership** | Two teams coordinate efforts; mutual success/dependency |
| **Shared Kernel** | Share a minimal subset of the model between contexts |
| **Customer-Supplier** | Downstream (customer) depends on upstream (supplier); upstream sets the pace |
| **Conformist** | Downstream conforms to upstream's model without questioning |
| **Anti-corruption Layer (ACL)** | Translation layer isolates downstream model from upstream contamination |
| **Open Host Service** | Publish an interface/protocol for other contexts to consume |
| **Published Language** | Well-documented shared format/document for communication |
| **Separate Ways** | Completely independent contexts, no integration |

### Domain & Subdomains (Core / Supporting / Generic)

| Type | Description | Investment |
|------|-------------|------------|
| **Core Domain** | The company's competitive differentiator — the reason the software exists. Gets the richest design, best developers, most investment. | **High** |
| **Supporting Subdomain** | Necessary for the business to function, but not a competitive differentiator (e.g., order management for an online store). | **Medium** |
| **Generic Subdomain** | Generic functionality that can be purchased or reused (e.g., authentication, email, payment processing). | **Low** |

**Rule:** The richest, most careful model belongs in the Core Domain. Ready-made solutions are acceptable for Generic Subdomains. Custom development investment should follow the priority: Core > Supporting > Generic.

---

## 3. Tactical Design

Tactical Design provides building blocks for implementing rich, expressive domain models **inside a Bounded Context**.

### Entity

An object with **continuous identity** over time and space, independent of its attributes.

| Aspect | Description |
|--------|-------------|
| **Identity** | Has a unique identifier that persists across state changes |
| **Equality** | Two Entity objects are equal if their IDs are equal, even if all attributes differ |
| **Mutability** | Generally mutable — attributes can change while identity remains |
| **Behavior** | Encapsulates business rules affecting its state |
| **Example** | `Customer` (identified by `customerId`) — a customer may change address/name but remains the same entity |

### Value Object

An object describing a domain characteristic **without conceptual identity**.

| Aspect | Description |
|--------|-------------|
| **Identity** | No conceptual identity — compared by value (all attributes) |
| **Immutability** | Must be immutable — cannot change after creation |
| **Equality** | Two VOs are equal if all attributes are equal |
| **Behavior** | Self-contained behavior related to its value (e.g., `Money.add(Money)`) |
| **Substitutability** | Can be freely replaced with another instance of equal value |
| **Examples** | `Money(amount, currency)`, `Email(address)`, `Address(street, city, zip)`, `PhoneNumber(value)` |

**Guideline:** Favor Value Objects over primitive types (e.g., `Email` instead of `String`, `Money` instead of `number`) to make the domain model richer and more expressive.

### Aggregate & Aggregate Root

A **cluster** of domain objects (Entities and Value Objects) treated as a **single unit** for data changes.

| Aspect | Description |
|--------|-------------|
| **Aggregate Root** | The only Entity externally referenceable; entry point to the cluster |
| **Boundary** | Objects inside the Aggregate are accessed only through the Root |
| **Consistency** | Root guarantees all invariants within the boundary |
| **Transactions** | Each transaction modifies exactly **one** Aggregate |
| **Communication** | Aggregates communicate via Domain Events or ID references |
| **Size** | **Small aggregates** — only what's needed to guarantee invariants (Vernon guideline) |

**Rules:**
1. Root is the only entry point — external objects reference only the Root's ID.
2. Root guarantees all invariants for the entire cluster.
3. Inside the aggregate: **immediate consistency** (transactional).
4. Between aggregates: **eventual consistency** (via Domain Events).
5. Each database transaction modifies exactly one Aggregate instance.

### Domain Events

Something that **happened in the domain** that interested parties need to know.

| Aspect | Description |
|--------|-------------|
| **Name** | Past-tense, domain-relevant name (e.g., `OrderSubmitted`, `PaymentReceived`) |
| **Immutability** | Immutable — records what happened, cannot change |
| **Data** | Carries relevant data (IDs, timestamps, values) |
| **Publisher** | Published by the originating Aggregate Root |
| **Consumers** | Other Aggregates, Domain Services, other Bounded Contexts |

**Use cases:**
- Inter-aggregate communication within the same context
- Notifying other Bounded Contexts about state changes
- Starting long-running workflows (sagas / process managers)
- Triggering non-critical side effects (notifications, logging)
- Feeding CQRS read models

### Repository

A mechanism encapsulating storage, retrieval, and search of domain objects (Aggregates), providing a collection-like interface.

| Aspect | Description |
|--------|-------------|
| **Interface** | Belongs to the **Domain Layer** — defines what the domain needs |
| **Implementation** | Belongs to the **Infrastructure Layer** — implements persistence |
| **Scope** | One Repository per Aggregate Root |
| **Client** | Domain layer code calls Repository interfaces, never concrete implementations |

**Key principle:** The domain never depends on persistence details. Repositories hide the underlying storage mechanism (SQL, NoSQL, in-memory, filesystem).

### Domain Services

A **stateless** object encapsulating a domain operation that **does not naturally belong** to an Entity or Value Object.

| Aspect | Description |
|--------|-------------|
| **Stateless** | Holds no state; operates on domain objects |
| **Domain logic** | Contains **domain logic** (not use-case orchestration) |
| **Name** | Named after a domain concept (e.g., `TransferService`, `PricingService`) |

**When to use:**
- The operation involves multiple Aggregates
- The logic is a domain process not owned by a single entity
- Coordination between domain and external resources is needed
- The operation doesn't fit naturally as a method on any Entity or VO

**Important distinction:** Domain Services contain **domain logic**. Application Services orchestrate use cases and delegate to Domain Services, Entities, and Repositories — they are NOT the same.

---

## 4. Ubiquitous Language

A **shared language** between developers and domain experts, grounded in the domain model. Everyone — developers, Product Owners, domain experts, QA — uses the same terms with the same meaning.

**Principles:**

- Code terms must exactly reflect business terms — a `Booking` class, not `Reservation`, if the business calls it "Booking".
- Language permeates all conversations, documentation, code, tests, and user interfaces.
- Ambiguities are resolved through continuous refinement between domain experts and developers.
- A confusing or awkward term signals a failure in domain understanding — refactor the model.

> *"The model is the backbone of the language. The language carries the model."* — Eric Evans

**Benefits:**

| Benefit | Description |
|---------|-------------|
| **Clarity** | No translation between business and code — everyone understands each other |
| **Consistency** | Terms have the same meaning everywhere in the system |
| **Model integrity** | Code stays aligned with the domain |
| **Faster onboarding** | New team members learn the domain through the code |

---

## 5. Anti-corruption Layer (ACL)

A design pattern creating a **translation layer** between two Bounded Contexts to prevent concepts from one context from "contaminating" the other's model.

**When to use:**
- Integration with legacy systems
- Third-party systems with different domain models
- Contexts with very different Ubiquitous Languages
- When Conformist is undesirable and the upstream cannot be forced to change

**Components:**

| Component | Role |
|-----------|------|
| **Facade** | Simplified interface to the external system — hides complexity |
| **Adapter** | Converts calls between the two systems |
| **Translator** | Converts objects/messages between the two domain models |

**Benefit:** The modern context's domain model remains pure and aligned with its Ubiquitous Language, free from foreign or legacy concepts. Changes in the external system do not ripple into the protected domain.

---

## 6. Hexagonal Architecture (Ports & Adapters)

**Creator:** Alistair Cockburn (2005)

**Concept:** Places the **application core** (domain + use cases) at the center, isolated from external dependencies through **Ports** (interfaces) and **Adapters** (implementations).

| Layer | Components | Direction |
|-------|------------|-----------|
| **Core / Domain** | Entities, Value Objects, Aggregates, Domain Events, Domain Services | Innermost — no external dependencies |
| **Ports (Primary / Driving)** | Interfaces defining use cases (e.g., `CreateOrderUseCase`) | Call **into** the core |
| **Ports (Secondary / Driven)** | Interfaces the core needs (e.g., `OrderRepository`) | Core **calls** these interfaces |
| **Adapters (Primary)** | Controllers, CLI, HTTP handlers, GUI | Implement driving ports |
| **Adapters (Secondary)** | Repository implementations, message brokers, external APIs | Implement driven ports |

**Benefits:**

- **Isolation** — Domain is completely isolated from infrastructure concerns.
- **Testability** — Adapters can be mocked or replaced with fakes for unit tests.
- **Technology independence** — Database, framework, or UI can be swapped without impacting the domain.
- **Clean boundaries** — Follows the Dependency Inversion Principle (DIP): domain depends on abstractions, not concretions.

**Relationship with DDD:** Hexagonal Architecture is the ideal architectural structure for implementing DDD. The Domain Model (Entities, VOs, Aggregates) sits at the center. Repositories are secondary ports. Domain Services live in the core. Application Services are primary port implementations.

---

## 7. Anemic vs Rich Domain Model

### Anemic Domain Model (anti-pattern)

Coined by **Martin Fowler** — domain objects are pure data: getters and setters, no behavior. Business logic lives in separate Application Services or Domain Services.

| Aspect | Anemic Model |
|--------|-------------|
| Domain objects | Only data (getters/setters) |
| Business logic | In external Application/Domain Services |
| Orientation | Procedural programming disguised as OO |
| Cohesion | Low — data and behavior are separated |
| Testability | Difficult — business rules are scattered across services |

**Acceptable for:** Simple CRUD systems, admin screens, rapid prototypes/MVPs. **But it is NOT DDD.**

### Rich Domain Model (DDD-aligned)

Domain objects contain **data + behavior together**. Business rules are encapsulated in Entities and Value Objects.

| Aspect | Rich Domain Model |
|--------|-------------------|
| Domain objects | Data + behavior |
| Business logic | Encapsulated in Entities and Value Objects |
| Orientation | True Object-Oriented design |
| Cohesion | High — state and behavior in the same place |
| Testability | High — direct unit tests on the domain model |

**Comparison table:**

| Aspect | Anemic | Rich (DDD) |
|--------|--------|------------|
| Domain objects | Only data (getters/setters) | Data + behavior |
| Business logic | In external services | In Entities/VOs |
| Orientation | Procedural disguised as OO | True OO |
| Cohesion | Low | High |
| Testability | Difficult | High |
| Encapsulation | Broken | Preserved |
| Model expressiveness | Low | High |

---

## 8. DDD + Microservices

**Fundamental relationship:** DDD and microservices are **naturally complementary** — DDD provides the conceptual toolkit to identify service boundaries.

**Alignment principles:**

1. **Bounded Context ≈ Microservice** — Each Bounded Context is a strong candidate for an independent microservice.
2. **Ubiquitous Language per service** — Each microservice has its own Ubiquitous Language.
3. **Event-driven communication** — Domain Events are the ideal mechanism for inter-service communication.
4. **Decentralized data** — Each microservice owns its own database (database-per-service pattern).

**Practical recommendations:**

- Do **not** blindly map 1:1 — a single Bounded Context may be implemented as multiple microservices for scaling or team size reasons.
- Consider non-functional requirements (latency, scalability, deploy frequency, team size) when deciding service boundaries.
- Use **Anti-corruption Layers** when integrating with other services or legacy systems.
- Prefer **asynchronous communication (events)** between contexts/services over synchronous calls.
- Each microservice maintains its own version of the Ubiquitous Language — terms are not shared globally.

| DDD Concept | Microservice Equivalent |
|-------------|------------------------|
| Bounded Context | Service boundary |
| Ubiquitous Language | Service API vocabulary |
| Aggregate | Transactional consistency boundary |
| Domain Event | Integration event / message |
| Anti-corruption Layer | Gateway / adapter to external services |
| Context Map | Service dependency diagram |

---

## 9. CQRS and Event Storming

### CQRS (Command Query Responsibility Segregation)

**Creator:** Greg Young (popularized by Martin Fowler)

A pattern that separates **read operations (Queries)** from **write operations (Commands)** into separate models.

**Why use with DDD:**
- DDD focuses on Commands (state changes) and Domain Events.
- Rich domain models are optimized for writing, not reading.
- Complex queries can use flat, optimized read models without domain complexity.

**Levels of CQRS:**

| Level | Description |
|-------|-------------|
| **Basic** | Separate Command and Query classes in the same process; same database |
| **Separate Databases** | Different write and read databases (eventually consistent) |
| **CQRS + Event Sourcing** | Commands generate Domain Events that feed read projections |

**Apply when:**
- Asymmetry between reads and writes (different shapes, volumes, frequencies).
- Complex domains with elaborate command validations.
- Multiple read views of the same data (different projections).
- Independent scaling of reads and writes.

**Avoid when:**
- Simple CRUD systems with symmetric reads and writes.
- Small teams or teams inexperienced with the pattern.
- Domains where the same representation works for both reads and writes.

### Event Storming

**Creator:** Alberto Brandolini (~2012–2013)

A collaborative workshop technique for exploring complex business domains. Participants (domain experts, developers, stakeholders) model business processes visually on a wall covered with paper.

**Color-coded Post-its:**

| Color | Element | Description |
|-------|---------|-------------|
| 🟧 Orange | **Domain Events** | "Something that happened" (e.g., "Order Placed") |
| 🟦 Blue | **Commands** | Actions that trigger events (e.g., "Place Order") |
| 🟩 Green | **Aggregates** | Objects receiving commands and producing events |
| 🟨 Yellow | **Actors/Roles** | People or systems involved in the process |
| 🟪 Purple | **Policies / Business Rules** | Rules reacting to events and triggering commands |
| ⬜ White | **External Systems** | Systems outside the modeled context |
| ⬛ Red | **Hot Spots** | Problems, risks, questions requiring attention |

**Three variations:**

| Variation | Duration | Focus |
|-----------|----------|-------|
| **Big Picture** | ~2–4 hours | Organization-wide view, identifies bounded contexts |
| **Process Modeling** | ~1–2 days | Detailed process modeling within a context |
| **Software Design** | ~2–3 days | Detailed implementation design, aggregates, events |

**Why it matters for DDD:**
- Breaks the communication gap between developers and domain experts.
- Ubiquitous Language emerges naturally through collaborative discussion.
- Bounded Contexts reveal themselves through language shifts or timeline breaks.
- Aggregates emerge as objects receiving commands and producing events.
- Hot spots surface areas of risk, uncertainty, or complexity early.

---

## 10. References

### Books

| # | Title | Author | Year | ISBN |
|---|-------|--------|------|------|
| 1 | **Domain-Driven Design: Tackling Complexity in the Heart of Software** ("Blue Book") | Eric Evans | 2003 | 978-0321125217 |
| 2 | **Implementing Domain-Driven Design** ("Red Book") | Vaughn Vernon | 2013 | 978-0321834577 |
| 3 | **Domain-Driven Design Distilled** | Vaughn Vernon | 2016 | 978-0134434421 |
| 4 | **Domain-Driven Design Reference** | Eric Evans | 2014 | — |
| 5 | **Introducing Event Storming** | Alberto Brandolini | 2014 | — |
| 6 | **Hexagonal Architecture Explained** | Alistair Cockburn & Juan Manuel Garrido de Paz | 2024 | — |

### Papers & Articles

| # | Title | Author | Year | URL |
|---|-------|--------|------|-----|
| 1 | **Anemic Domain Model** | Martin Fowler | 2003 | martinfowler.com/bliki/AnemicDomainModel.html |
| 2 | **CQRS** | Martin Fowler | 2011 | martinfowler.com/bliki/CQRS.html |
| 3 | **Mocks Aren't Stubs** | Martin Fowler | 2007 | martinfowler.com/articles/mocksArentStubs.html |

### Online Resources

| Resource | URL |
|----------|-----|
| DDD Community | https://www.dddcommunity.org/ |
| Domain Language (Eric Evans) | https://www.domainlanguage.com/ |
| DDD Reference PDF (2015) | https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf |
| Microsoft — Domain Events Design | https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/domain-events-design-implementation |
| Microsoft — Anti-Corruption Layer | https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer |
| Microsoft — CQRS Pattern | https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs |
| AWS — Anti-Corruption Layer | https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/acl.html |
| Alistair Cockburn — Hexagonal Architecture | https://alistair.cockburn.us/hexagonal-architecture/ |
| Event Storming Official | https://www.eventstorming.com/ |
| Wikipedia — Domain-Driven Design | https://en.wikipedia.org/wiki/Domain-driven_design |

### Example Repositories

| Repository | Description | URL |
|------------|-------------|-----|
| ddd-hexagonal-cqrs-es-eda | Complete DDD + Hexagonal + CQRS + Event Sourcing example | https://github.com/bitloops/ddd-hexagonal-cqrs-es-eda |
| typescript-ddd-example (CodelyTV) | DDD example in TypeScript | https://github.com/CodelyTV/typescript-ddd-example |
| ddd-blue-book-study | Blue Book study guide | https://github.com/sabinewinkler/ddd-blue-book-study |