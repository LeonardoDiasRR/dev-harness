---
name: feature-based-architecture
tags: [architecture, frontend, react, FDD, FSD, code-splitting]
sources: [feature-based-resumo.md]
created: 2026-06-21
updated: 2026-06-21
---

# Feature-Based Architecture

A comprehensive architectural pattern for organizing frontend applications by **business functionality** (vertical slicing) rather than by technical file type (horizontal/layer-based slicing). Each feature is a self-contained module with its own components, hooks, services, state, types, and tests.

---

## 1. Origin: Feature-Driven Development (FDD) — De Luca & Coad (1997/1999)

Feature-Driven Development is one of the **original agile methods**, conceived before the 2001 Agile Manifesto. Unlike Scrum (management focus) and XP (engineering practices), FDD emphasizes **domain modeling + iterative feature delivery**.

### Timeline

| Year | Milestone |
|------|-----------|
| **1997** | Jeff De Luca conceived FDD during a large (~50-person) Java loan system project for United Overseas Bank in Singapore. He partnered with **Peter Coad** (creator of the Coad OOA/OOD method) and **Eric Lefebvre** to formalize the methodology. |
| **1999** | FDD formally published in **Chapter 6** of *"Java Modeling in Color with UML: Enterprise Components and Process"* (Prentice Hall) by Coad, Lefebvre, and De Luca. The book introduced **color modeling** (4-color UML stereotypes: Moment-Interval, Role, Description, Party/Place/Thing) and the FDD process. |
| **2002** | Reference book: *"A Practical Guide to Feature-Driven Development"* by Palmer & Felsing (Prentice Hall) expanded FDD with case studies, scaling strategies, and step-by-step guidance. |

### The 5 FDD Processes

1. **Develop Overall Model** — Domain walkthrough, object model creation, collaborative refinement
2. **Build Feature List** — Decompose domain into *features* (< 2 weeks each), categorized by activity area
3. **Plan by Feature** — Assign features to chief programmers, prioritize, plan iterations
4. **Design by Feature** — 3-5 developer teams, 1-3 day design/diagramming, design inspection
5. **Build by Feature** — Implementation, testing, code inspection, promote to main build

Each feature has **6 progress milestones**: Domain Walkthrough (1%) → Design (40%) → Design Inspection (3%) → Code (45%) → Code Inspection (10%) → Promote to Build (1%). When coding begins, the feature is already **44% complete**.

---

## 2. Feature-Sliced Design (FSD)

Feature-Sliced Design is a **modern Russian-developed architectural methodology** for frontend (widely adopted by Avito, Yandex, Tinkoff). Unlike FDD (which focuses on *process*), FSD is a **structural code organization methodology**.

### FSD Hierarchy: Layers → Slices → Segments

**7 Layers** (top-to-bottom dependency order):

| Layer | Description |
|-------|-------------|
| **app** | Global config, providers, router, global store, global styles |
| **processes** (optional) | Business processes spanning multiple pages |
| **pages** | Full application pages (compose widgets and features) |
| **widgets** | Autonomous reusable UI components between pages |
| **features** | Complete business-value features (user-facing use cases) |
| **entities** | Domain models, business logic, data models |
| **shared** | Utilities, UI kit, constants, helpers — **no business logic** |

**Slices:** Within each layer (except `shared` and `app`), code is divided by **business domain** (e.g., `features/auth`, `features/checkout`).

**Segments:** Internal structure of each slice: `ui/`, `lib/`, `model/`, `api/`, `config/`, `testing/`.

### FSD Unidirectional Dependency Flow

```
app → pages → widgets → features → entities → shared
```

A layer must **never** import from a layer above it.

---

## 3. Layer vs Feature vs Component Comparison

### Layer-Based (Horizontal Slicing)
Groups by *technical file type* — all components in `components/`, all hooks in `hooks/`, etc.

- **Pros:** Simple for beginners, clear technical separation
- **Cons:** High mental navigation (5+ folders per feature), low cohesion, doesn't scale, tight coupling to framework

### Feature-Based (Vertical Slicing)
Groups by *business functionality* — everything for a feature lives in one folder.

- **Pros:** High cohesion, low mental navigation, team parallelism, isolation, natural lazy loading, faster onboarding
- **Cons:** Potential duplication, complex shared/ management, over-engineering for small projects, hard feature boundary definition

### Component-Based (e.g., Atomic Design)
Focuses on reusable UI components (atoms → molecules → organisms → templates → pages).

- **Pros:** High reusability, visual consistency, clear UI/logic separation
- **Cons:** UI-only focus, ignores business logic, can lead to prop drilling, doesn't solve complex feature organization

### Comparison Table

| Criterion | Layer-Based | Feature-Based | Component-Based |
|-----------|:-----------:|:-------------:|:---------------:|
| Cohesion | Low | **High** | Medium |
| Reusability | Medium | Medium | **High** |
| Mental Navigation | **High** (worst) | Low | Medium |
| Team Parallelism | Low | **High** | Medium |
| Native Lazy Loading | No | **Yes** | Partial |
| Learning Curve | Low | Medium | Low |
| Initial Overhead | Minimal | Moderate | Low |
| Scalability | Poor | **Excellent** | Good (for UI) |
| Refactoring Ease | Hard | **Easy** | Moderate |

---

## 4. React Implementation: Lazy Loading & Code Splitting

Feature-based architecture pairs naturally with code splitting because each feature is a self-contained module.

```tsx
const CheckoutFeature = lazy(() => import('./features/checkout'));
const ProductListFeature = lazy(() => import('./features/products'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/checkout" element={<CheckoutFeature />} />
        <Route path="/products" element={<ProductListFeature />} />
      </Routes>
    </Suspense>
  );
}
```

### How It Works

- `React.lazy()` uses dynamic `import()` → each feature becomes a separate chunk
- Chunk loads only when the user navigates to that route
- `Suspense` shows a fallback while loading

### Performance Benefits

- Smaller initial bundle
- On-demand loading
- Better FCP (First Contentful Paint) and LCP (Largest Contentful Paint)
- Granular caching

### Splitting Strategies

| Strategy | Description |
|----------|-------------|
| **Route-based** | Entire page per feature (most common) |
| **Component-level** | Modals, dialogs, heavy components |
| **Intersection Observer** | Below-the-fold content |

---

## 5. Directory Structure: `features/` and `shared/`

The CONSTITUTION.md mandates the following frontend structure:

```
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
```

### Per-Feature Structure (with barrel export)

```text
src/features/<feature-name>/
  components/    ← Feature-specific React components
  hooks/         ← Feature-specific custom hooks
  services/      ← API calls and service logic
  store/         ← Feature state (Redux slice, Zustand store)
  types/         ← Feature-specific TypeScript types
  tests/         ← Unit and integration tests
  index.ts       ← Public API barrel export
```

### Shared Directory (no business logic)

```text
src/shared/
  ui/            ← Design System / UI Kit (Button, Input, Modal, etc.)
  utils/         ← Pure utility functions (formatDate, debounce, cn)
  constants/     ← Global constants (api-endpoints, routes, app-config)
  types/         ← Shared types (common, api-response)
  hooks/         ← Generic hooks (useDebounce, useMediaQuery)
  api/           ← Generic HTTP client (axios instance, interceptors)
  lib/           ← Auxiliary libraries (logger, analytics)
```

### Principles

- Segments exist only if needed
- Barrel exports (`index.ts`) control public API
- Nothing exported beyond necessity
- Tests co-located with their feature

---

## 6. Dependency Rules: Features Don't Import Features

**The fundamental rule:** A feature **must never** import directly from another feature.

**Rationale:** Prevents coupling, preserves isolation, avoids circular dependencies, enables clean lazy loading chunks.

### How to Share Code Instead

| Need | Destination |
|------|-------------|
| Reusable UI component | `shared/ui/` |
| Utility function | `shared/utils/` |
| Constant/endpoint | `shared/constants/` |
| Common type | `shared/types/` or `entities/` |
| Generic hook | `shared/hooks/` |
| Domain entity (User, Product) | `entities/` |
| Generic API service | `shared/api/` |
| Complex functionality | Extract to `entities/` or new layer |

### Enforcement Tools

- ESLint (`no-restricted-imports`)
- `eslint-plugin-feature-sliced-design`
- Controlled barrel exports
- Code reviews
- Nx / Dependency cruiser / Madge

### Controlled Exceptions

- Cross-feature via events (pub/sub)
- Shared global state (Redux — if slices are independent)
- Composition via pages/widgets layer

---

## 7. Conflicts with DDD / Bounded Context

### The Core Tension

| Approach | Organizes By |
|----------|-------------|
| **DDD / Bounded Contexts** | *Domain boundaries* with explicit models and ubiquitous language |
| **Feature-Based** | *User-facing functionality* |

**Boundaries do not always align.**

### Conflict Scenarios

1. **A feature crosses multiple Bounded Contexts** — e.g., "Complete Order" involves Payment (BC Payments) + Inventory (BC Inventory) + Order (BC Sales)
2. **A Bounded Context contains multiple features** — e.g., BC "Sales" may contain "List Products", "Add to Cart", "Complete Order", "Order History"
3. **Entity reuse mismatch** — DDD may define `Product` differently across BCs; pure feature-based may force a single representation

### Resolution Approaches

| Approach | Description |
|----------|-------------|
| Feature = BC | Map each feature as a BC (works for simple systems) |
| Feature inside BC | Organize by BC first, features within each BC |
| BC as deployment module | Micro-frontends where each BC is an independent MF |
| Hybrid DDD (FSD solution) | Entities in `entities/` layer, features as use cases in `features/` layer |

**FSD's position:** FSD resolves this tension by:
1. Separating `entities/` (DDD domain models) from `features/` (use cases/application services)
2. Allowing entities to be shared between features under dependency rules
3. Treating features as orchestration of entities

---

## 8. Criticisms

### 8.1 Code Duplication
Since features cannot import each other, similar code may be duplicated. **Counter:** Conscious trade-off — duplication is preferable to coupling. Patterns emerge naturally for extraction to `shared/`. Static analysis tools help.

### 8.2 Over-Engineering for Small Projects
Feature-based adds unnecessary complexity for MVPs, landing pages, or simple CRUD apps. **Counter:** Suitable for **medium to large projects** with multiple features/teams. Layer-based or flat structure works better for small projects.

### 8.3 Poorly Defined Feature Boundaries
The biggest practical challenge: defining what a "feature" is. Features can become too large (mini-monoliths) or too small. No universal objective criterion exists. Leads to frequent boundary refactoring and endless code review debates.

### 8.4 Cross-Cutting Concerns
Logging, analytics, authentication, themes, and i18n affect multiple features. Harder to implement consistently. **Partial solutions:** HOCs/wrappers in `app/`, top-level providers, dependency injection, AOP via decorators/middleware.

### 8.5 Learning Curve
Developers used to layer-based structures need time to adapt. The discipline of not importing across features requires training and automated enforcement.

### 8.6 Shared/ Management Complexity
If `shared/` grows too much, it becomes a "god module" dumping ground; if too little, features end up duplicating. Requires constant attention and governance.

### 8.7 Cross-Feature Refactoring Difficulty
Moving code between features (or to `shared/`) can break imports in many places.

### 8.8 Conflict with File-Based Routing (Next.js App Router)
Next.js App Router uses directory structure for routes (`app/products/[id]/page.tsx`), conflicting with feature-based organization. **Solutions:**
- Feature-based *inside* `app/`
- Keep `app/` for routing only and `src/` for feature-based
- Merge both approaches

### 8.9 Dependency on Team Discipline
Without automated enforcement (ESLint, code review), dependency rules are easily violated and the architecture degrades over time.

---

## 9. References

### Books

1. **Coad, P.; Lefebvre, E.; De Luca, J.** *Java Modeling in Color with UML: Enterprise Components and Process.* Prentice Hall, 1999. ISBN 0130676152. — *First FDD publication (Chapter 6).*
2. **Palmer, S. R.; Felsing, J. M.** *A Practical Guide to Feature-Driven Development.* Prentice Hall, 2002. ISBN 0130676152. — *Definitive FDD reference guide.*
3. **Evans, E.** *Domain-Driven Design: Tackling Complexity in the Heart of Software.* Addison-Wesley, 2003. — *DDD and Bounded Contexts.*

### Online Documentation & Articles

4. **Feature-Sliced Design — Official Documentation.** https://feature-sliced.design/
5. **Feature-Sliced Design — Overview.** https://fsd.how/docs/get-started/overview/
6. **Wikipedia — Feature-Driven Development.** https://en.wikipedia.org/wiki/Feature-driven_development
7. **Feature-Sliced Design GitHub.** https://github.com/feature-sliced
8. **ESLint Plugin for FSD.** https://github.com/nadProg/eslint-plugin-feature-sliced-design
9. **Skomorokhov, M.I.** *Feature-Sliced Design as Universal Architecture for Frontend Projects.* 2023. https://s.eduherald.ru/pdf/2023/6/21341.pdf
10. **dev.to — Layer vs Feature Architecture (smotastic).** https://dev.to/smotastic/layer-vs-feature-architecture-3cko
11. **dev.to — Scalable React Projects with Feature-Based Architecture (Naser Rasouli).** https://dev.to/naserrasouli/scalable-react-projects-with-feature-based-architecture-117c
12. **LogRocket — Lazy Loading React Components.** https://blog.logrocket.com/lazy-loading-components-in-react-16-6-6cea535c0b52/
13. **freeCodeCamp — Micro-Frontend Architecture Handbook.** https://www.freecodecamp.org/news/complete-micro-frontends-guide/
14. **Microsoft Learn — DDD-oriented Microservice Design.** https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/ddd-oriented-microservice