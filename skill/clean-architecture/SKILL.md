---
name: clean-architecture
description: >-
  A comprehensive Hermes skill covering Clean Architecture — origin (Robert C.
  Martin, 2012), the Dependency Rule, the four layers (Entities, Use Cases,
  Interface Adapters, Frameworks), variations (Hexagonal/Cockburn,
  Onion/Palermo), Ports & Adapters pattern, one-use-case-per-action design,
  canonical directory structure per CONSTITUTION.md B8, frontend adaptations,
  DTOs vs Domain Models, dependency injection approaches, testability
  strategies, criticisms, and authoritative references.
version: 1.0.0
author: Hermes Agent (curated from Robert C. Martin, Alistair Cockburn, Jeffrey Palermo, Martin Fowler, et al.)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [clean-architecture, architecture, hexagonal-architecture, onion-architecture, ports-and-adapters, dependency-rule, ddd, solid, software-design, architecture-patterns, entity, use-case, interface-adapter, framework, dto]
    related_skills: [tdd, dry, yagni, kiss, separation-of-concerns, feature-based-architecture]
---

# Clean Architecture

## 1. Origin

### Robert C. Martin (Uncle Bob) — *Clean Architecture* (2012/2017)

- **Blog post (2012):** Robert C. Martin published *"The Clean Architecture"* on his blog (blog.cleancoder.com) on August 13, 2012. The post synthesized decades of architectural experience into a unified set of principles.
- **Book (2017):** *Clean Architecture: A Craftsman's Guide to Software Structure and Design* (Prentice Hall, ISBN 978-0-13-449416-6) expanded the post into 34 chapters across 6 parts covering paradigms, SOLID, components, architecture details, frameworks-as-details, and a full case study.
- **Goal:** Build systems that are independent of frameworks, testable, independent of UI, independent of databases, and independent of any external agent.
- **Core thesis:** Architecture should *scream* the purpose of the system. Architects distinguish **policy** (business rules) from **details** (delivery mechanisms).

### Influences

Clean Architecture synthesizes ideas from several earlier architectural patterns:

| Influence | Year | Author | Key Contribution |
|-----------|------|--------|------------------|
| Hexagonal Architecture (Ports & Adapters) | 2005 | Alistair Cockburn | Ports/interfaces in the core, adapters outside |
| Onion Architecture | 2008 | Jeffrey Palermo | Concentric layers with DDD at center |
| SOLID Principles | 2000s | Robert C. Martin | Especially the Dependency Inversion Principle |
| Domain-Driven Design | 2003 | Eric Evans | Ubiquitous language, aggregates, bounded contexts |

---

## 2. Dependency Rule

> **"Source code dependencies must point only inward, toward higher-level policies."** — Robert C. Martin

### Definition

The Dependency Rule is the single most important rule in Clean Architecture:

- Nothing in an inner circle can know anything about an outer circle.
- No inner code imports, mentions, or references names declared in outer circles.
- Data crossing boundaries must be **simple data structures** (DTOs, primitives, maps).
- The rule applies to **source-code dependencies only** — control flow can go in any direction.
- **Enforcement mechanism:** The Dependency Inversion Principle (DIP). High-level modules define interfaces (ports); low-level modules implement them (adapters). A DI Container wires them at runtime.

### Layer Diagram

```
[Frameworks & Drivers]  (outermost — lowest level)
       ↑ dependency
[Interface Adapters]
       ↑ dependency
[Use Cases]
       ↑ dependency
[Entities]              (innermost — highest level)
```

### Concrete Rules

| Rule | Description |
|------|-------------|
| Entities → nothing | Domain entities import only language/stdlib, never outer layers |
| Use Cases → Entities only | Application layer imports only domain types — never infrastructure or presentation |
| Interface Adapters → Use Cases + Entities | Adapters implement ports defined by use cases |
| Frameworks → everything inner | Outer layers depend on inner ones, never the reverse |

---

## 3. Four Layers

### 3.1 Entities (Enterprise Business Rules)

- Enterprise-wide business objects (not app-specific).
- Most stable, highest-level layer.
- May be classes, structs, or pure functions + data structures.
- Depend on **nothing external** (no frameworks, no ORMs, no databases).
- Examples: `Customer`, `Order`, `BankAccount` with intrinsic validations.

```python
# Pure domain entity — no framework dependencies
@dataclass
class Customer:
    id: UUID
    name: str
    email: Email  # Value Object

    def change_email(self, new_email: Email) -> None:
        if self.email == new_email:
            raise DomainError("New email must differ from current email")
        self.email = new_email
```

### 3.2 Use Cases (Interactors / Application Business Rules)

- Application-specific behavior — what the user can do.
- **One class/module per use case** (Command Pattern).
- Orchestrate entities to fulfill a goal.
- Know nothing about HTTP, databases, UI, or external details.
- Define **ports** — interfaces the outside world must implement.
- Examples: `CreateOrderUseCase`, `CancelReservationUseCase`.

```python
# Use case — depends only on domain types and ports (interfaces)
class CreateOrderUseCase:
    def __init__(self, order_repo: OrderRepository, notifier: NotificationPort):
        self.order_repo = order_repo
        self.notifier = notifier

    def execute(self, input_dto: CreateOrderInput) -> CreateOrderOutput:
        customer = self.order_repo.find_customer(input_dto.customer_id)
        order = Order.create(customer=customer, items=input_dto.items)
        self.order_repo.save(order)
        self.notifier.send_order_confirmation(order)
        return CreateOrderOutput(order_id=order.id, status="created")
```

### 3.3 Interface Adapters

- Bridge between Use Cases/Entities and the external world.
- Sub-components:

| Component | Role |
|-----------|------|
| **Controllers** | Receive external input, convert to Use Case format |
| **Presenters** | Receive Use Case output, format for display (JSON, HTML, ViewModel) |
| **Gateways** | Implement repository/service interfaces defined by Use Cases |
| **DTOs** | Simple data structures crossing boundaries |

- **Critical rule:** No code from this layer leaks into Use Cases or Entities.

### 3.4 Frameworks & Drivers

- Outermost layer — everything concrete and detailed.
- Includes web frameworks (Django, Spring, Express), ORMs/database drivers, HTTP clients, queues, caches, file systems, devices, screens.
- > **"Frameworks and drivers are details."** — Robert C. Martin
- Must not contaminate inner layers with framework annotations, inheritance, or infrastructure calls.

---

## 4. Variations

### 4.1 Hexagonal Architecture (Ports & Adapters) — Alistair Cockburn, 2005

- **Origin:** Technical report published September 4, 2005.
- **Core idea:** The system is a **hexagon** (shape not meaningful) with **ports** (interfaces) on each side. The application core communicates with the outside world **exclusively through ports**.

| Term | Definition |
|------|-----------|
| **Port** | Interface in the core defining an operation |
| **Adapter** | Concrete implementation of a port |
| **Driving Actor** | Agent that *initiates* communication (user, scheduler) → primary/driving ports |
| **Driven Actor** | Agent that *responds* (database, external API) → secondary/driven ports |

- No concentric layers — all adapters at the boundary.

### 4.2 Onion Architecture — Jeffrey Palermo, 2008

- **Origin:** 3-part blog series in July/August 2008.
- **Core idea:** Concentric layers like an onion, dependencies point inward. Inspired by Domain-Driven Design (Eric Evans, 2003).
- **Layers (inside → out):**
  1. **Domain Model** (Entities, Value Objects, Aggregates)
  2. **Domain Services** (orchestrate multiple entities; repository interfaces)
  3. **Application Services** (use cases, transaction orchestration, authorization)
  4. **Infrastructure / UI** (concrete implementations)
- **Differences from Clean Architecture:** Onion is older (2008 vs 2012), explicitly DDD-based, allows variable layer count, and puts UI in the outer layer rather than separating Presenters.

### 4.3 Comparison

| Feature | Hexagonal (2005) | Onion (2008) | Clean (2012) |
|---------|-----------------|--------------|---------------|
| Shape | Hexagon (boundary) | Onion (concentric) | Circles (concentric) |
| Focus | Ports & Adapters | DDD + domain at center | Dependency Rule + 4 layers |
| Layer count | 2 (core + adapters) | 4+ (variable) | 4 (fixed) |
| Presenters | Output adapter | Outer UI layer | Own layer (Interface Adapters) |
| Use Cases | Secondary/driving ports | Application Services | Interactors (one per action) |

---

## 5. Ports & Adapters

The operational pattern that makes the Dependency Rule possible:

1. The **Use Case** (inner circle) declares an interface — the **Port**.
2. **Infrastructure** (outer circle) implements the interface — the **Adapter**.
3. The Use Case uses the Port; the Adapter implements the Port.
4. The **DI Container** wires them at the **Composition Root**.

```
[Use Case] → [Port: IRepository] ←interface→ [Adapter: RepositorySQL]
              (code dependency inward)         (implements port)
```

### Types of Adapters

| Type | Direction | Examples |
|------|-----------|----------|
| **Driving Adapters** | Input → Core | HTTP Controller, CLI, queue listener |
| **Driven Adapters** | Core → Output | SQL Repository, REST client, Email provider, Redis cache |

```python
# Port — interface defined in the application layer
class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> None: ...

    @abstractmethod
    def find_by_id(self, order_id: UUID) -> Order: ...

# Adapter — concrete implementation in infrastructure layer
class PostgresOrderRepository(OrderRepository):
    def __init__(self, connection: Connection):
        self.conn = connection

    def save(self, order: Order) -> None:
        # SQL INSERT implementation
        pass

    def find_by_id(self, order_id: UUID) -> Order:
        # SQL SELECT implementation
        pass
```

---

## 6. Use Cases (One per Action)

- **Each use case is a separate class/module.**
- **Why?** SRP (single reason to change), explicit reusability, isolated testability, clear boundaries.

```python
# ❌ Bad: monolithic service
class OrderService:
    def create_order(self, ...): ...
    def cancel_order(self, ...): ...
    def calculate_shipping(self, ...): ...

# ✅ Good: one use case per action
class CreateOrderUseCase: ...
class CancelOrderUseCase: ...
class CalculateShippingUseCase: ...
```

| Element | Description |
|---------|-------------|
| **Input** | Request Model / Input DTO — simple object with input data |
| **Output** | Response Model / Output DTO — simple object with the result |
| **Ports** | Interfaces the use case depends on (repositories, services) |
| **Orchestration** | The use case coordinates entities and calls ports — no business logic duplicated |

---

## 7. Directory Structure

### Canonical Structure (per CONSTITUTION.md B8)

```
src/
├── domain/                           # Core — depends on nothing
│   ├── entities/                     # Aggregates & Entities with identity
│   ├── value-objects/                # Immutable domain concepts (Email, Money, CPF…)
│   ├── events/                       # Domain Events
│   ├── exceptions/                   # Domain-specific exceptions
│   ├── repositories/                 # Repository interfaces (contracts only)
│   └── services/                     # Domain Services (logic spanning multiple aggregates)
│
├── application/                      # Application business rules — orchestrates domain
│   ├── use-cases/                    # One class per use case
│   ├── dtos/                         # Input/Output data transfer objects
│   ├── ports/                        # Interfaces for external services (email, storage…)
│   └── mappers/                      # Domain ↔ DTO transformations
│
├── infrastructure/                   # Frameworks & drivers — implements domain interfaces
│   ├── persistence/                  # Repository implementations, ORM models, migrations
│   ├── messaging/                    # Event bus, queue adapters
│   ├── external/                     # Third-party API clients
│   └── config/                       # Env vars, DI container wiring
│
└── presentation/                     # Delivery mechanism — HTTP, CLI, gRPC…
    ├── http/
    │   ├── controllers/              # Thin: validate input → call use case → serialize output
    │   ├── middlewares/
    │   └── routes/
    └── cli/                          # Optional: CLI commands
```

### Backend Layer Rules (B8)

| Rule | Description |
|------|-------------|
| `domain/` → nothing | Must NOT import from `application/`, `infrastructure/`, or `presentation/` |
| `application/` → domain only | Must NOT import from `infrastructure/` or `presentation/` |
| `infrastructure/` + `presentation/` → inner | Implement interfaces defined in inner layers |
| Controllers are thin | No business logic, no direct repository access |

### Simplified Structure (smaller projects)

```
src/
├── core/
│   ├── entities/
│   ├── use_cases/
│   └── ports/
├── adapters/
│   ├── persistence/
│   ├── api/
│   └── email/
├── main.py            # Composition root
└── config.py
```

### Golden Rules (consolidated)

1. **Domain** imports nothing from other layers (stdlib/language runtime only).
2. **Application** imports only Domain — never Infrastructure or Presentation.
3. **Infrastructure** imports Domain and Application — never Presentation.
4. **Presentation** imports Application (and may import Domain for types).
5. **Boundary-specific DTOs** — don't reuse the same class for request/response and domain entities.
6. **No logic in controllers** — delegate immediately to Use Cases.
7. **Never expose ORM models** outside Infrastructure — use mappers.
8. **ORM annotations annotate Models, never Entities** — entities are pure classes.
9. **Unit tests** test Domain and Application without real infrastructure.
10. **Integration tests** test Infrastructure with real databases.

---

## 8. Frontend Adaptations

- **Entities** → Domain models (e.g., `User`, `Cart`)
- **Use Cases** → App actions (e.g., `LoginUseCase`, `AddToCartUseCase`)
- **Interface Adapters** → Store/State Management (Redux, Zustand, Pinia), Presenters
- **Frameworks & Drivers** → UI components (React, Angular, Vue)

### Common Frontend Adaptations

| Clean Architecture Concept | Frontend Equivalent |
|---------------------------|---------------------|
| Use Case | Custom hook or service + state action |
| Port (interface) | Interface for HTTP repository, local storage, cache |
| Adapter | fetch/axios implementation for REST APIs |
| Presenter | Hook (React) or Selector (Redux) |
| Controller | Event handler that calls the Use Case |

- Use Cases orchestrate API calls + state logic.
- Ports are interfaces for HTTP repositories, local storage, cache.
- Adapters implement fetch/axios for REST APIs.
- Presenters become *hooks* (React) or *selectors* (Redux).
- UI components **never call APIs directly** — they call Use Cases.

### Feature-Sliced Design (FSD) — Modern Frontend Methodology

FSD combines Clean Architecture with feature-based slicing:

```
src/
├── app/             # Framework configuration
├── pages/           # Complete pages
├── features/        # Features (each with ui/, model/, api/)
├── entities/        # Business entities
└── shared/          # Shared code (UI kit, helpers)
```

---

## 9. DTOs vs Domain Models

| Feature | Domain Model | DTO |
|---------|-------------|-----|
| Purpose | Encapsulate business rules + behavior | Transport data between layers/services |
| Behavior | Has methods with business logic | No behavior (fields only) |
| State | Mutable or immutable | Generally immutable |
| Dependencies | None (POJO/POCO) | None (simple struct/dataclass) |
| Serialization | Not directly serializable | Designed for serialization (JSON, XML) |
| Persistence | No ORM annotations | Not annotated — transport only |

### Rule of Thumb

Use **Domain Models** inside `domain/` and `application/`. Convert to **DTOs** at boundaries (controllers, presenters, APIs).

```
[Controller] ←DTO→ [Use Case] ←Entity/Domain→ [Repository] ←ORM/DTO→ [DB]
```

```python
# Domain Model — has behavior
class Order:
    def __init__(self, items: list[OrderItem]):
        self.items = items
        self._total = self._calculate_total()

    def _calculate_total(self) -> Decimal:
        return sum(item.price * item.quantity for item in self.items)

# DTO — data transport only, no behavior
@dataclass
class CreateOrderRequest:
    customer_id: str
    items: list[tuple[str, int]]  # product_id, quantity

@dataclass
class CreateOrderResponse:
    order_id: str
    status: str
    total: Decimal
```

---

## 10. DI Approaches

| Technique | Description | When to Use |
|-----------|-------------|-------------|
| **Constructor Injection** | Dependencies passed in constructor | **Preferred** (90% of cases) — explicit, testable, no container coupling |
| **Factory Pattern** | Method/factory creating instances | When creation logic is complex or runtime-dependent (8% of cases) |
| **DI Container** | Framework auto-resolving the dependency tree | **Composition Root only** — the single application entry point (2% of cases) |

### Recommended Hierarchy

1. **Constructor Injection (90%)** — explicit, testable, no coupling
2. **Factory (8%)** — runtime-parameterized creation
3. **DI Container / Service Locator (2%)** — Composition Root only

```python
# Constructor Injection (preferred)
class CreateOrderUseCase:
    def __init__(self, repo: OrderRepository, notifier: NotificationPort):
        self.repo = repo
        self.notifier = notifier

# Composition Root (entry point)
def main():
    db = create_db_connection(config.DATABASE_URL)
    repo = PostgresOrderRepository(db)
    email = SmtpEmailProvider(config.SMTP_HOST)

    create_order = CreateOrderUseCase(repo, email)
    cancel_order = CancelOrderUseCase(repo)

    app = Flask(__name__)
    register_routes(app, create_order=create_order, cancel_order=cancel_order)
    app.run()
```

---

## 11. Testability

Clean Architecture provides exceptional testability because each layer can be tested independently:

| Layer | Testing Strategy | Dependencies |
|-------|-----------------|--------------|
| **Domain** | Pure unit tests | None (no mocks, no DB, no IO) |
| **Application** | Unit tests with mocks | Mock ports/interfaces |
| **Infrastructure** | Integration tests | Real or in-memory DB (e.g., SQLite) |
| **Presentation** | Contract/API tests | Mocked use cases (e.g., `TestClient`) |

### Test Pyramid in Clean Architecture

- **Base (most):** Unit tests (Domain + Application) — fast, isolated
- **Middle:** Acceptance/API tests (Presentation)
- **Top (fewest):** Integration tests (Infrastructure)

```python
# Testing a Use Case with mocked ports
def test_create_order_success():
    repo = Mock(spec=OrderRepository)
    email = Mock(spec=NotificationService)
    use_case = CreateOrderUseCase(repo, email)

    result = use_case.execute(CreateOrderInput(client_id="123", items=[...]))

    assert result.status == "created"
    repo.save.assert_called_once()
    email.send.assert_called_once()

# Testing Domain Entity (no mocks needed)
def test_order_total_calculation():
    order = Order(items=[
        OrderItem(product_id="p1", price=Decimal("50"), quantity=2),
        OrderItem(product_id="p2", price=Decimal("30"), quantity=1),
    ])
    assert order.total == Decimal("130")
```

---

## 12. Criticisms

### Main Criticism: Overengineering for Small Applications

- **Excessive boilerplate:** Every use case becomes a class, every boundary a DTO, every adapter an interface + implementation. Disproportionate overhead for simple CRUD.
- **Unnecessary indirection:** Data traverses Controller → DTO → Use Case → Port → Adapter → DB for simple queries.
- **YAGNI violation:** Adding layers for flexibility that may never be needed.
- **High cognitive cost:** Junior developers struggle with 4 layers and multiple abstractions.
- **Setup time:** Configuring structure, interfaces, and DI for an MVP delays market validation.
- **False sense of security:** Layers don't guarantee good architecture if the team doesn't understand the principles — can devolve into "lasagna architecture."

### When NOT to Use Clean Architecture

- Prototypes and MVPs (rapid validation)
- Small teams with short timelines
- Trivial business rules (pure CRUD)
- Scripts and disposable internal tools
- Extremely simple microservices (1–2 endpoints)

### Defense / Counter-Arguments

- Overengineering is a manageable trade-off — technical debt from *not* having architecture is greater long-term.
- For projects that will grow, the cost of refactoring later exceeds the initial setup cost.
- It's a **spectrum, not binary** — apply only some principles (e.g., separate business rules from frameworks without 4 separate projects).
- Start with well-defined boundaries; add layers as complexity grows.

### Community Consensus

> **"Use Clean Architecture when the value of the business lies in the business rules, not in the CRUD."**

| Scenario | Approach |
|----------|----------|
| Simple app (< 5 use cases, CRUD) | Layered architecture (controller → service → repository) |
| Medium app (5–20 use cases) | Simplified Clean Architecture (core + adapters) |
| Complex app (> 20 use cases, DDD, multiple bounded contexts) | Full Clean Architecture with ports & adapters |
| Legacy system → refactoring | Apply gradually per bounded context (Strangler Fig pattern) |

---

## 13. References

### Primary Sources

1. **MARTIN, Robert C.** *"The Clean Architecture"*. Blog Clean Coder, 13 Aug 2012. https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
2. **MARTIN, Robert C.** *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. Prentice Hall, 2017. ISBN 978-0-13-449416-6.
3. **COCKBURN, Alistair.** *"Hexagonal Architecture" (Ports & Adapters)*. HaT Technical Report 2005.02, 4 Sep 2005. https://alistair.cockburn.us/hexagonal-architecture/
4. **PALERMO, Jeffrey.** *"The Onion Architecture"* (part 1). Programming with Palermo, Jul 2008. https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/

### Secondary Sources (Articles & Guides)

5. **GRACA, Herberto.** *"Ports & Adapters Architecture"*, 14 Sep 2017. https://herbertograca.com/2017/09/14/ports-adapters-architecture/
6. **GRACA, Herberto.** *"Onion Architecture"*, 21 Sep 2017. https://herbertograca.com/2017/09/21/onion-architecture/
7. **GRACA, Herberto.** *"Clean Architecture"*, 1 Nov 2017. https://herbertograca.com/2017/11/16/clean-architecture/
8. **JOVANOVIC, Milan.** *"How To Approach Clean Architecture Folder Structure"*, 24 Sep 2022. https://www.milanjovanovic.tech/blog/clean-architecture-folder-structure
9. **Feature-Sliced Design.** *"Clean Architecture in Frontend: A How-To Guide"*, 2025. https://feature-sliced.design/blog/frontend-clean-architecture
10. **FREE CODE CAMP.** *"A quick introduction to clean architecture"*, Daniel Báez. https://www.freecodecamp.org/news/a-quick-introduction-to-clean-architecture-990c014448d2/

### Criticisms & Analysis

11. **AlgoCademy.** *"Why Your Clean Architecture Is Making Things More Complicated"*, 2025. https://algocademy.com/blog/why-your-clean-architecture-is-making-things-more-complicated/
12. **Learnixo.** *"When NOT to Use Clean Architecture — Trade-offs, Complexity, Overengineering"*, May 2026. https://learnixo.io/blog/clean-arch-when-not-to-use
13. **Three Dots Labs.** *"Is Clean Architecture Overengineering?"* (Podcast). https://threedots.tech/episode/is-clean-architecture-overengineering/

### Reference Code

14. **bespoyasov/frontend-clean-architecture** — React + TypeScript example. https://github.com/bespoyasov/frontend-clean-architecture
15. **ardalis/CleanArchitecture** — .NET reference implementation. https://github.com/ardalis/CleanArchitecture