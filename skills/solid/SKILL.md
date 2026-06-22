---
name: solid
description: >-
  A comprehensive Hermes skill covering the SOLID principles of object-oriented
  design — Single Responsibility (SRP), Open/Closed (OCP), Liskov Substitution
  (LSP), Interface Segregation (ISP), and Dependency Inversion (DIP). Includes
  origin with Robert C. Martin and Michael Feathers, detailed definitions,
  before/after code examples in TypeScript and Java, frontend (React) and
  backend applications, criticisms from functional programming and YAGNI
  perspectives, and SRP vs. Separation of Concerns (SoC) comparison.
version: 1.0.0
author: >-
  Hermes Agent (curated from Robert C. Martin, Barbara Liskov, Bertrand Meyer,
  Michael Feathers, Martin Fowler, Dan North, et al.)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags:
      - solid
      - solid-principles
      - single-responsibility
      - open-closed
      - liskov-substitution
      - interface-segregation
      - dependency-inversion
      - oop
      - object-oriented-design
      - clean-code
      - clean-architecture
      - design-principles
      - software-architecture
      - typescript
      - java
      - react
      - backend
    related_skills:
      - dry
      - yagni
      - kiss
      - separation-of-concerns
      - feature-based-architecture
      - tdd
---

# SOLID Principles

> **A mnemonic acronym for five foundational principles of object-oriented class design, introduced by Robert C. Martin (Uncle Bob) and named by Michael Feathers.**

---

## 1. Origin

SOLID is a mnemonic acronym coined by **Michael Feathers** to represent the first five class-design principles defined by **Robert C. Martin (Uncle Bob)** in the early 2000s.

| Letter | Principle | Original Source |
|--------|-----------|----------------|
| **S** | Single Responsibility Principle (SRP) | Robert C. Martin (~2002) |
| **O** | Open/Closed Principle (OCP) | Bertrand Meyer (1988), popularized by Martin |
| **L** | Liskov Substitution Principle (LSP) | Barbara Liskov (OOPSLA 1987); formalized w/ Jeannette Wing (1994) |
| **I** | Interface Segregation Principle (ISP) | Robert C. Martin — *C++ Report* (1996) |
| **D** | Dependency Inversion Principle (DIP) | Robert C. Martin — *C++ Report* (1996) |

### Timeline of Key Publications

- **1987** — Barbara Liskov delivers keynote "Data Abstraction and Hierarchy" at OOPSLA 1987, introducing LSP.
- **1988** — Bertrand Meyer publishes *Object-Oriented Software Construction*, coining OCP.
- **1994** — Liskov & Wing publish "A Behavioral Notion of Subtyping" (ACM TOPLAS), formalizing LSP.
- **1995** — First spark: Robert C. Martin posts about design principles in the comp.object newsgroup (March 1995).
- **1996** — Martin publishes ISP and DIP articles in *C++ Report*.
- **2000** — Martin's article "The Principles of OOD" (Object Mentor) lists **11 OOD principles**.
- **2002** — **"Agile Software Development, Principles, Patterns, and Practices"** (Pearson, ISBN 0135974445) — the canonical book covering the 5 SOLID principles + package principles + GoF design patterns.

### The Core Idea

> *"A set of principles that, when followed, tend to create code that is more maintainable, flexible, and resilient to change."*

---

## 2. Single Responsibility Principle (SRP)

### Definition

> **"A module should be responsible to one, and only one, actor."** — Robert C. Martin

Alternative formulation: **"A class should have only one reason to change."**

### Origin

Robert C. Martin first articulated SRP in the early 2000s as part of his OOD principles. The concept draws from earlier work on **cohesion** by Yourdon & Constantine (1979), who defined functional cohesion as the strongest type of cohesion — a module where all elements contribute to a single, well-defined task.

### Key Interpretation

- **"Responsibility"** = *"a reason to change"*
- **"Actor"** = a group of stakeholders who can request a change
- If two different actors can request changes to the same module for different reasons, SRP is violated
- SRP is **not** about a class doing one thing (that's functional cohesion); it's about a class serving a single actor

### Violation Example (Java)

```java
// ❌ SRP Violation: Three actors, one class
class Employee {
    public double calculatePay() {
        // Finance department rules
        return 0.0;
    }

    public String reportHours() {
        // HR department rules
        return "";
    }

    public void save() {
        // DBA/IT rules — persistence logic
    }
}
// Three actors (Finance, HR, DBA) → three reasons to change → SRP violation
```

### Correction Example (Java)

```java
// ✅ SRP Compliance: Each class serves one actor

class Employee {
    // Pure data only
    private String id;
    private double hourlyRate;
    private int hoursWorked;
    // getters & setters...
}

class PayCalculator {
    public double calculatePay(Employee e) {
        // Finance department logic only
        return e.getHourlyRate() * e.getHoursWorked();
    }
}

class HourReporter {
    public String reportHours(Employee e) {
        // HR department logic only
        return "Employee " + e.getId() + " worked " + e.getHoursWorked() + " hours.";
    }
}

class EmployeeRepository {
    public void save(Employee e) {
        // Persistence logic only
        // INSERT INTO employees ...
    }
}
```

### Violation Example (TypeScript)

```typescript
// ❌ SRP Violation
class UserService {
  constructor(private db: Database) {}

  validateUser(data: unknown): boolean {
    // Validation logic
    return true;
  }

  computeFullName(first: string, last: string): string {
    // Business logic
    return `${first} ${last}`;
  }

  async save(data: unknown): Promise<void> {
    // Persistence logic
    await this.db.insert('users', data);
  }

  async sendWelcomeEmail(email: string): Promise<void> {
    // Email logic — completely different concern
    // ...
  }
}
```

### Correction Example (TypeScript)

```typescript
// ✅ SRP Compliance

class UserValidator {
  validate(data: unknown): boolean {
    // Only validation logic
    return true;
  }
}

class UserFactory {
  createFullName(first: string, last: string): string {
    // Only name computation
    return `${first} ${last}`;
  }
}

class UserRepository {
  constructor(private db: Database) {}

  async save(data: unknown): Promise<void> {
    // Only persistence
    await this.db.insert('users', data);
  }
}

class EmailService {
  async sendWelcomeEmail(email: string): Promise<void> {
    // Only email sending
  }
}
```

### Frontend Application (React)

**Violation:** A `UserProfile` component that fetches data, transforms dates, manages loading/error state, and renders UI — all in one file.

```typescript
// ❌ SRP Violation: Component does everything
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(r => r.json())
      .then(data => {
        setUser(data);
        setLoading(false);
      });
  }, [userId]);

  const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString('en-US', {
      year: 'numeric', month: 'long', day: 'numeric'
    });
  };

  if (loading) return <Spinner />;
  return (
    <div>
      <h1>{user.name}</h1>
      <p>Joined: {formatDate(user.createdAt)}</p>
    </div>
  );
}
```

**Correction:** Separate concerns into a custom data-fetching hook, a pure presentational component, and an orchestrator.

```typescript
// ✅ SRP Compliance

// Hook — only data fetching
function useUser(userId: string) {
  const [state, setState] = useState<{ user: User | null; loading: boolean }>({
    user: null, loading: true
  });

  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(r => r.json())
      .then(user => setState({ user, loading: false }));
  }, [userId]);

  return state;
}

// Utility function — only date formatting
function formatJoinDate(date: string): string {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric', month: 'long', day: 'numeric'
  });
}

// Pure component — only rendering
function UserInfo({ name, joinDate }: { name: string; joinDate: string }) {
  return (
    <div>
      <h1>{name}</h1>
      <p>Joined: {formatJoinDate(joinDate)}</p>
    </div>
  );
}

// Orchestrator — composes the above
function UserProfile({ userId }: { userId: string }) {
  const { user, loading } = useUser(userId);

  if (loading) return <Spinner />;
  return <UserInfo name={user.name} joinDate={user.createdAt} />;
}
```

### Backend Application (NestJS/Express)

**Violation:** A controller handling HTTP + business logic + persistence.

**Correction:** Layered architecture with single-responsibility layers:

| Layer | Responsibility | Actor |
|-------|---------------|-------|
| `UserController` | Only HTTP concerns (routing, request/response, status codes) | Frontend team / API consumers |
| `UserService` | Only business logic (validation, rules, orchestration) | Product owner |
| `UserRepository` | Only persistence (SQL queries, ORM calls) | DBA / data team |

```typescript
// ✅ SRP layered architecture (NestJS style)

@Controller('users')
class UserController {
  constructor(private userService: UserService) {}

  @Post()
  async create(@Body() dto: CreateUserDto) {
    return this.userService.create(dto);
  }
}

class UserService {
  constructor(private userRepo: UserRepository) {}

  async create(dto: CreateUserDto) {
    // Business logic only
    if (!this.isValidEmail(dto.email)) {
      throw new ValidationError('Invalid email');
    }
    return this.userRepo.save(dto);
  }

  private isValidEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
}

class UserRepository {
  constructor(private prisma: PrismaClient) {}

  async save(dto: CreateUserDto) {
    // Persistence only
    return this.prisma.user.create({ data: dto });
  }
}
```

---

## 3. Open/Closed Principle (OCP)

### Definition

> **"Software entities (classes, modules, functions) should be open for extension, but closed for modification."** — Bertrand Meyer (1988)

### Origin

Bertrand Meyer introduced OCP in his 1988 book *Object-Oriented Software Construction*. The principle was later popularized and integrated into SOLID by Robert C. Martin. Meyer's original formulation relied on inheritance (subclassing), but modern interpretations favor **abstractions** (interfaces, abstract classes) and **composition** (Strategy pattern).

### Key Interpretation

- **Open for extension:** New behavior can be added (new class, new implementation)
- **Closed for modification:** Existing source code is not changed when adding new functionality
- Achieving OCP requires identifying **variation points** — aspects of the system that are likely to change — and abstracting them behind interfaces
- Violations manifest as long `if/else` or `switch` chains that grow with each new feature

### Violation Example (Java)

```java
// ❌ OCP Violation: Switch-based approach
class AreaCalculator {
    public double calculateArea(Object shape) {
        if (shape instanceof Circle) {
            Circle c = (Circle) shape;
            return 3.14159 * c.radius * c.radius;
        } else if (shape instanceof Rectangle) {
            Rectangle r = (Rectangle) shape;
            return r.width * r.height;
        }
        // ❌ Adding Triangle → must modify this method
        throw new IllegalArgumentException("Unknown shape");
    }
}
```

### Correction Example (Java)

```java
// ✅ OCP Compliance via polymorphism
interface Shape {
    double area();
}

class Circle implements Shape {
    private double radius;
    public Circle(double radius) { this.radius = radius; }
    @Override
    public double area() { return 3.14159 * radius * radius; }
}

class Rectangle implements Shape {
    private double width, height;
    public Rectangle(double w, double h) { this.width = w; this.height = h; }
    @Override
    public double area() { return width * height; }
}

// ✅ New shape = new class, no existing code modified
class Triangle implements Shape {
    private double base, height;
    public Triangle(double b, double h) { this.base = b; this.height = h; }
    @Override
    public double area() { return 0.5 * base * height; }
}

class AreaCalculator {
    public double calculateArea(Shape shape) {
        return shape.area(); // Closed for modification, open for extension
    }
}
```

### Violation Example (TypeScript)

```typescript
// ❌ OCP Violation
class PaymentProcessor {
  processPayment(type: string, amount: number): void {
    if (type === 'credit') {
      // Credit card logic
    } else if (type === 'debit') {
      // Debit card logic
    } else if (type === 'pix') {
      // PIX (Brazilian instant payment) logic
    }
    // ❌ Adding new payment type → modify this method
  }
}
```

### Correction Example (TypeScript) — Strategy Pattern

```typescript
// ✅ OCP Compliance via Strategy pattern
interface PaymentMethod {
  process(amount: number): void;
}

class CreditPayment implements PaymentMethod {
  process(amount: number): void {
    console.log(`Processing credit card payment of $${amount}`);
  }
}

class DebitPayment implements PaymentMethod {
  process(amount: number): void {
    console.log(`Processing debit card payment of $${amount}`);
  }
}

class PixPayment implements PaymentMethod {
  process(amount: number): void {
    console.log(`Processing PIX payment of $${amount}`);
  }
}

// ✅ New payment type = new class, PaymentProcessor untouched
class CryptoPayment implements PaymentMethod {
  process(amount: number): void {
    console.log(`Processing cryptocurrency payment of $${amount}`);
  }
}

class PaymentProcessor {
  constructor(private paymentMethod: PaymentMethod) {}

  processPayment(amount: number): void {
    this.paymentMethod.process(amount);
  }
}
```

### Frontend Application (React)

**Violation:** A `Button` component using `if/else` or a massive `switch` for each variant.

```typescript
// ❌ OCP Violation
function Button({ variant, children }: { variant: string; children: ReactNode }) {
  let className = 'btn';
  if (variant === 'primary') className += ' btn-primary';
  else if (variant === 'secondary') className += ' btn-secondary';
  else if (variant === 'danger') className += ' btn-danger';
  else if (variant === 'success') className += ' btn-success';
  // Adding a new variant → modify this component
  return <button className={className}>{children}</button>;
}
```

**Correction:** Composition-based approach — a base `Button` that accepts class names, and variant-specific composed components.

```typescript
// ✅ OCP Compliance

// Base component — closed for modification
interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  className?: string;
  children: ReactNode;
}

function BaseButton({ className = '', children, ...props }: ButtonProps) {
  return <button className={`btn ${className}`} {...props}>{children}</button>;
}

// Variant components — open for extension
function PrimaryButton(props: Omit<ButtonProps, 'className'>) {
  return <BaseButton className="btn-primary" {...props} />;
}

function SecondaryButton(props: Omit<ButtonProps, 'className'>) {
  return <BaseButton className="btn-secondary" {...props} />;
}

function DangerButton(props: Omit<ButtonProps, 'className'>) {
  return <BaseButton className="btn-danger" {...props} />;
}

// ✅ New variant = new component, no existing code changed
function GhostButton(props: Omit<ButtonProps, 'className'>) {
  return <BaseButton className="btn-ghost" {...props} />;
}
```

### Backend Application (Strategy Pattern)

```typescript
// ✅ OCP in Backend — Shipping strategy
interface ShippingStrategy {
  calculate(order: Order): number;
  getEstimatedDays(): number;
}

class PACShipping implements ShippingStrategy {
  calculate(order: Order): number {
    return order.weight * 0.5;
  }
  getEstimatedDays(): number {
    return 10;
  }
}

class SEDEXShipping implements ShippingStrategy {
  calculate(order: Order): number {
    return order.weight * 1.2;
  }
  getEstimatedDays(): number {
    return 3;
  }
}

// Closed for modification, open for extension
class ShippingCalculator {
  constructor(private strategy: ShippingStrategy) {}

  calculate(order: Order): number {
    return this.strategy.calculate(order);
  }

  getEstimate(order: Order): string {
    const cost = this.calculate(order);
    const days = this.strategy.getEstimatedDays();
    return `$${cost.toFixed(2)} — ${days} business days`;
  }
}
```

---

## 4. Liskov Substitution Principle (LSP)

### Definition (Liskov, 1987)

> **"If S is a subtype of T, then objects of type T may be replaced by objects of type S, without breaking the program."** — Barbara Liskov, OOPSLA 1987 Keynote

**Formal definition (Liskov & Wing, 1994):**
> *"Let φ(x) be a property provable about objects x of type T. Then φ(y) should be true for objects y of type S where S is a subtype of T."*

### Origin

Barbara Liskov first presented the concept in her 1987 OOPSLA keynote "Data Abstraction and Hierarchy." She later formalized it with Jeannette Wing in a 1994 ACM TOPLAS paper. The principle establishes a **behavioral** notion of subtyping — it's not enough that subclasses share the same interface; they must also preserve the **behavioral contract** of the superclass.

### Substitution Rules

**Signature rules:**
- Method parameter types in subtype must be **contravariant** (accept wider types) or equal
- Return types in subtype must be **covariant** (return narrower types) or equal
- Subtype cannot throw additional exception types not thrown by the supertype

**Behavioral rules (the "Design by Contract" view):**
- **Preconditions** cannot be strengthened in the subtype (subtype cannot require more than the supertype)
- **Postconditions** cannot be weakened in the subtype (subtype must guarantee at least what the supertype guarantees)
- **Invariants** of the superclass must be preserved in the subtype

### Classic Violation: Rectangle-Square

```java
// ❌ LSP Violation — The canonical example
class Rectangle {
    private int width, height;

    public void setWidth(int w) { this.width = w; }
    public void setHeight(int h) { this.height = h; }
    public int getArea() { return width * height; }
}

class Square extends Rectangle {
    @Override
    public void setWidth(int w) {
        super.setWidth(w);
        super.setHeight(w);  // Violates LSP: changes expected behavior
    }

    @Override
    public void setHeight(int h) {
        super.setHeight(h);
        super.setWidth(h);   // Violates LSP: changes expected behavior
    }
}

// Client expects Rectangle behavior → FAILS with Square
void resizeToFixedAspect(Rectangle r) {
    r.setWidth(5);
    r.setHeight(10);
    assert r.getArea() == 50;  // TRUE for Rectangle, FALSE for Square!
}
```

### Correction Example (Java)

```java
// ✅ LSP Compliance: Both implement a common abstraction
interface Shape {
    int getArea();
}

class Rectangle implements Shape {
    private int width, height;

    public Rectangle(int w, int h) { this.width = w; this.height = h; }

    @Override
    public int getArea() { return width * height; }
}

class Square implements Shape {
    private int side;

    public Square(int side) { this.side = side; }

    @Override
    public int getArea() { return side * side; }
}

// Client works with any Shape
void printArea(Shape shape) {
    System.out.println("Area: " + shape.getArea());
}
```

### Violation Example (TypeScript)

```typescript
// ❌ LSP Violation — Bird example
class Bird {
  fly(): string {
    return 'Flying!';
  }
}

class Penguin extends Bird {
  fly(): string {
    throw new Error('Penguins cannot fly!');
  }
}

function letItFly(bird: Bird): string {
  return bird.fly();
}

const penguin = new Penguin();
letItFly(penguin); // 💥 Runtime error!
```

### Correction Example (TypeScript)

```typescript
// ✅ LSP Compliance

interface Bird {
  // No fly method here — only common bird behavior
  getDescription(): string;
}

interface FlyingBird extends Bird {
  fly(): string;
}

class Sparrow implements FlyingBird {
  getDescription(): string {
    return 'A small brown bird.';
  }

  fly(): string {
    return 'Sparrow takes flight!';
  }
}

class Penguin implements Bird {
  getDescription(): string {
    return 'A flightless Antarctic bird.';
  }
  // No fly method — no substitution problem
}

function describeBird(bird: Bird): string {
  return bird.getDescription(); // Safe for any bird subtype
}

function letItFly(bird: FlyingBird): string {
  return bird.fly(); // Safe: only birds that CAN fly get passed here
}
```

### LSP Leads to Composition over Inheritance

The GoF principle applies: **"Favor object composition over class inheritance."** Instead of modeling `Square extends Rectangle`, use a common interface (`Shape`) and have both implement it independently. This avoids the behavioral contract violations that LSP guards against.

### Frontend Application (React)

LSP applies to React component composition — any component that receives common props and behaves consistently per its type contract.

```typescript
// ❌ LSP Violation in React — A specialized component that breaks the contract
interface BaseModalProps {
  isOpen: boolean;
  onClose: () => void;
  children: ReactNode;
}

function BaseModal({ isOpen, onClose, children }: BaseModalProps) {
  if (!isOpen) return null;
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        {children}
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
}

// ❌ This component silently ignores onClose
function NoCloseModal({ isOpen, children }: Omit<BaseModalProps, 'onClose'>) {
  if (!isOpen) return null;
  return (
    <div className="modal-overlay">
      <div className="modal-content">
        {children}
        {/* No close button, backdrop click doesn't close */}
      </div>
    </div>
  );
}
// If used where BaseModal is expected, onClose never fires → LSP violation
```

```typescript
// ✅ LSP Compliance — Separate concerns explicitly
interface ModalProps {
  isOpen: boolean;
  children: ReactNode;
}

// Reusable building block
function ModalBackdrop({ isOpen, children }: ModalProps) {
  if (!isOpen) return null;
  return <div className="modal-overlay">{children}</div>;
}

// Specific variants
function DismissableModal({ isOpen, onClose, children }: BaseModalProps) {
  return (
    <ModalBackdrop isOpen={isOpen}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        {children}
        <button onClick={onClose}>Close</button>
      </div>
    </ModalBackdrop>
  );
}

function StaticModal({ isOpen, children }: ModalProps) {
  return (
    <ModalBackdrop isOpen={isOpen}>
      <div className="modal-content">{children}</div>
    </ModalBackdrop>
  );
}
```

### Backend Application

The classic example is repository pattern conformance:

```typescript
// ✅ LSP in Repository Pattern
interface Repository<T> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  save(entity: T): Promise<T>;
  delete(id: string): Promise<void>;
}

class PostgresUserRepository implements Repository<User> {
  async findById(id: string): Promise<User | null> {
    // Returns User or null — satisfies contract
  }
  async findAll(): Promise<User[]> { /* ... */ }
  async save(entity: User): Promise<User> { /* ... */ }
  async delete(id: string): Promise<void> { /* ... */ }
}

// ✅ Must also satisfy the contract (same pre/post conditions)
// ❌ If InMemoryUserRepository throws on delete() instead of no-op — LSP violation
class InMemoryUserRepository implements Repository<User> {
  async delete(id: string): Promise<void> {
    // ✅ If user doesn't exist, just resolve (no-op) — preserves contract
    // ❌ If user doesn't exist, throw NotFoundError — strengthens postcondition? Violation?
  }
}
```

---

## 5. Interface Segregation Principle (ISP)

### Definition

> **"Clients should not be forced to depend upon interfaces that they do not use."** — Robert C. Martin

Also stated as: **"No client should be forced to depend on methods it does not use."**

### Origin

Robert C. Martin introduced ISP in his 1996 article for *C++ Report*. The principle was motivated by practical experience with "fat" interfaces in C++ (where multiple inheritance was the solution) and Java (where interface segregation became idiomatic).

### Key Interpretation

- "Fat interfaces" force implementors to depend on methods they don't need
- ISP focuses on interface design from the **client's perspective** — what do **callers** actually need?
- The solution is to segregate large interfaces into smaller, more specific ones
- **ISP vs SRP:** SRP focuses on a class's internal responsibility (one reason to change for one actor); ISP focuses on interface design from the caller's perspective

### Violation Example (Java)

```java
// ❌ ISP Violation — Fat interface
interface Machine {
    void print(Document d);
    void scan(Document d);
    void fax(Document d);
}

// ✅ Has all capabilities — fine
class MultiFunctionPrinter implements Machine {
    public void print(Document d) { /* ok */ }
    public void scan(Document d) { /* ok */ }
    public void fax(Document d) { /* ok */ }
}

// ❌ Forced to implement methods it doesn't use
class OldPrinter implements Machine {
    public void print(Document d) { /* ok */ }
    public void scan(Document d) { throw new UnsupportedOperationException(); }
    public void fax(Document d) { throw new UnsupportedOperationException(); }
}
```

### Correction Example (Java)

```java
// ✅ ISP Compliance — Segregated interfaces
interface Printer {
    void print(Document d);
}
interface Scanner {
    void scan(Document d);
}
interface Fax {
    void fax(Document d);
}

// Implements only what it needs
class OldPrinter implements Printer {
    public void print(Document d) { /* ok */ }
}

// Implements everything
class MultiFunctionPrinter implements Printer, Scanner, Fax {
    public void print(Document d) { /* ok */ }
    public void scan(Document d) { /* ok */ }
    public void fax(Document d) { /* ok */ }
}

// New use case: only scanning needed
class DocumentScanner implements Scanner {
    public void scan(Document d) { /* ok */ }
}
```

### Violation Example (TypeScript)

```typescript
// ❌ ISP Violation
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
  getPaid(): void;
}

class HumanWorker implements Worker {
  work() { console.log('Working...'); }
  eat() { console.log('Eating...'); }
  sleep() { console.log('Sleeping...'); }
  getPaid() { console.log('Getting paid...'); }
}

class RobotWorker implements Worker {
  work() { console.log('Working...'); }
  eat() { throw new Error('Robots do not eat!'); }
  sleep() { throw new Error('Robots do not sleep!'); }
  getPaid() { console.log('Getting maintenance budget...'); }
}
```

### Correction Example (TypeScript)

```typescript
// ✅ ISP Compliance — Segregated interfaces
interface Workable {
  work(): void;
}

interface Eatable {
  eat(): void;
}

interface Sleepable {
  sleep(): void;
}

interface Compensable {
  getPaid(): void;
}

class HumanWorker implements Workable, Eatable, Sleepable, Compensable {
  work() { console.log('Working...'); }
  eat() { console.log('Eating...'); }
  sleep() { console.log('Sleeping...'); }
  getPaid() { console.log('Getting paid...'); }
}

class RobotWorker implements Workable, Compensable {
  work() { console.log('Working...'); }
  getPaid() { console.log('Getting maintenance budget...'); }
}
```

### Frontend Application (React)

**Violation:** A single `useUser()` hook that returns everything about the user.

```typescript
// ❌ ISP Violation — Fat hook
function useUser(userId: string) {
  // ... fetches profile, posts, friends, settings
  return {
    profile,      // needed by UserProfile
    posts,        // needed by UserPosts
    friends,      // needed by UserFriends
    settings,     // needed by UserSettings
    // Every consumer gets everything, even if they don't need it
  };
}
```

**Correction:** Segregated hooks — each consuming only the interface it needs.

```typescript
// ✅ ISP Compliance — Segregated hooks
function useUserProfile(userId: string) {
  // Only fetches profile data
  // Returns: { name, email, avatar, ... }
}

function useUserPosts(userId: string) {
  // Only fetches posts
  // Returns: { posts, isLoading, error }
}

function useUserFriends(userId: string) {
  // Only fetches friends
  // Returns: { friends, isLoading, error }
}

function useUserSettings(userId: string) {
  // Only fetches settings
  // Returns: { theme, notifications, privacy, ... }
}

// Each component imports only what it needs
function UserProfile({ userId }: { userId: string }) {
  const { name, email, avatar } = useUserProfile(userId);
  return <div>{/* ... */}</div>;
}

function UserPosts({ userId }: { userId: string }) {
  const { posts } = useUserPosts(userId);
  return <div>{/* ... */}</div>;
}
```

### Backend Application (Repository Segregation)

```typescript
// ✅ ISP in Repository Pattern

// Small, focused interfaces
interface ReadOnlyRepository<T> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
}

interface WriteRepository<T> {
  save(entity: T): Promise<T>;
  delete(id: string): Promise<void>;
}

// Composed where needed
interface UserRepository extends ReadOnlyRepository<User>, WriteRepository<User> {
  findByEmail(email: string): Promise<User | null>;
}

// Read-only service doesn't need write methods
class UserReportService {
  constructor(private repo: ReadOnlyRepository<User>) {}
  // Only depends on read capabilities
  async generateReport(): Promise<Report> { /* ... */ }
}

// Admin service needs full access
class UserAdminService {
  constructor(private repo: UserRepository) {}
}
```

---

## 6. Dependency Inversion Principle (DIP)

### Definition

> **A. High-level modules should not depend on low-level modules. Both should depend on abstractions.**
> **B. Abstractions should not depend upon details. Details should depend upon abstractions.** — Robert C. Martin

### Origin

Robert C. Martin introduced DIP in his 1996 article for *C++ Report*. The principle inverts the traditional dependency flow of procedural programming, where high-level policy modules would directly call low-level detail modules. Martin's insight was that abstractions (interfaces) should define policy, and details (implementations) should conform to those abstractions.

### DIP vs Dependency Injection vs IoC

| Concept | Role | Example |
|---------|------|---------|
| **DIP** | The **principle** — *what* to do | "Depend on abstractions, not concretions" |
| **Dependency Injection (DI)** | A **technique** — *how* to do it | Constructor injection, setter injection, interface injection |
| **Inversion of Control (IoC)** | The broader concept | Framework calls your code (Hollywood Principle: "Don't call us, we'll call you") |

### Violation Example (Java)

```java
// ❌ DIP Violation: High-level depends on low-level
class EmailService {
    public void sendEmail(String message) {
        // SMTP server details — concrete implementation
        System.out.println("Sending via SMTP: " + message);
    }
}

class NotificationService {
    private EmailService email = new EmailService(); // Direct concrete dependency

    public void notify(String message) {
        email.sendEmail(message);
    }
}
// To add SMS support → must modify NotificationService!
```

### Correction Example (Java)

```java
// ✅ DIP Compliance
interface MessageService {
    void send(String message);
}

class EmailService implements MessageService {
    @Override
    public void send(String message) {
        System.out.println("Sending via SMTP: " + message);
    }
}

class SMSService implements MessageService {
    @Override
    public void send(String message) {
        System.out.println("Sending via SMS API: " + message);
    }
}

class PushNotificationService implements MessageService {
    @Override
    public void send(String message) {
        System.out.println("Sending via push notification: " + message);
    }
}

class NotificationService {
    private final MessageService messenger; // Depends on abstraction

    public NotificationService(MessageService messenger) { // Constructor DI
        this.messenger = messenger;
    }

    public void notify(String message) {
        messenger.send(message); // No knowledge of concrete implementation
    }
}
```

### Violation Example (TypeScript)

```typescript
// ❌ DIP Violation
class MySQLDatabase {
  async query(sql: string): Promise<unknown> {
    return db.query(sql);
  }
}

class UserService {
  private db = new MySQLDatabase(); // Hard-coded concrete dependency

  async getUsers() {
    return this.db.query('SELECT * FROM users');
  }
}
```

### Correction Example (TypeScript)

```typescript
// ✅ DIP Compliance
interface Database {
  query(sql: string): Promise<unknown>;
}

class MySQLDatabase implements Database {
  async query(sql: string): Promise<unknown> {
    return db.query(sql);
  }
}

class PostgreSQLDatabase implements Database {
  async query(sql: string): Promise<unknown> {
    return pg.query(sql);
  }
}

class InMemoryDatabase implements Database {
  private data: unknown[] = [];

  async query(sql: string): Promise<unknown> {
    // Simplified in-memory implementation for testing
    return this.data;
  }
}

class UserService {
  constructor(private db: Database) {} // Depends on abstraction

  async getUsers(): Promise<User[]> {
    return this.db.query('SELECT * FROM users') as Promise<User[]>;
  }
}

// Composition root
const db = new PostgreSQLDatabase();
const userService = new UserService(db);
```

### Frontend Application (React)

**Violation:** A `ProductsList` component calling `fetch('/api/products')` directly — coupling UI to a specific API endpoint.

```typescript
// ❌ DIP Violation — UI coupled to implementation detail
function ProductsList() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch('/api/products')  // Direct HTTP coupling
      .then(r => r.json())
      .then(setProducts);
  }, []);

  return <div>{/* render products */}</div>;
}
```

**Correction:** Abstract the data source behind an interface.

```typescript
// ✅ DIP Compliance

interface ProductRepository {
  fetchAll(): Promise<Product[]>;
  fetchById(id: string): Promise<Product | null>;
}

class ApiProductRepository implements ProductRepository {
  async fetchAll(): Promise<Product[]> {
    const res = await fetch('/api/products');
    return res.json();
  }

  async fetchById(id: string): Promise<Product | null> {
    const res = await fetch(`/api/products/${id}`);
    return res.json();
  }
}

class MockProductRepository implements ProductRepository {
  private mockData: Product[] = [
    { id: '1', name: 'Mock Product', price: 29.99 }
  ];

  async fetchAll(): Promise<Product[]> {
    return this.mockData;
  }

  async fetchById(id: string): Promise<Product | null> {
    return this.mockData.find(p => p.id === id) ?? null;
  }
}

// Hook depends on abstraction
function useProducts(repository: ProductRepository) {
  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    repository.fetchAll().then(setProducts);
  }, [repository]);

  return products;
}

// Component receives the abstraction
function ProductsList({ repository }: { repository: ProductRepository }) {
  const products = useProducts(repository);
  return <div>{/* render */}</div>;
}

// Usage in production
// <ProductsList repository={new ApiProductRepository()} />

// Usage in tests/storybook
// <ProductsList repository={new MockProductRepository()} />
```

### Backend Application (Spring Boot / DI Containers)

```java
// ✅ DIP with Spring Boot Dependency Injection
interface PaymentGateway {
    boolean processPayment(String orderId, BigDecimal amount);
}

@Component
class StripePaymentGateway implements PaymentGateway {
    @Override
    public boolean processPayment(String orderId, BigDecimal amount) {
        // Stripe API implementation
        return true;
    }
}

@Component
@Profile("sandbox")
class SandboxPaymentGateway implements PaymentGateway {
    @Override
    public boolean processPayment(String orderId, BigDecimal amount) {
        // Always succeeds for testing
        return true;
    }
}

@Service
class CheckoutService {
    private final PaymentGateway paymentGateway;

    // Spring injects the correct implementation via @Autowired (implicit via constructor)
    public CheckoutService(PaymentGateway paymentGateway) {
        this.paymentGateway = paymentGateway;
    }

    public CheckoutResult checkout(Order order) {
        boolean success = paymentGateway.processPayment(order.getId(), order.getTotal());
        return new CheckoutResult(success);
    }
}
```

```typescript
// ✅ DIP with NestJS / DI
interface Logger {
  log(message: string): void;
  error(message: string, trace?: string): void;
}

class ConsoleLogger implements Logger {
  log(message: string): void { console.log(`[INFO] ${message}`); }
  error(message: string, trace?: string): void { console.error(`[ERROR] ${message}`, trace); }
}

class FileLogger implements Logger {
  log(message: string): void { /* append to log file */ }
  error(message: string, trace?: string): void { /* append to error file */ }
}

// High-level service has no idea which Logger implementation it uses
class OrderService {
  constructor(private logger: Logger) {}

  async placeOrder(order: Order): Promise<void> {
    try {
      // ... order logic
      this.logger.log(`Order ${order.id} placed successfully`);
    } catch (err) {
      this.logger.error('Failed to place order', err.stack);
      throw err;
    }
  }
}
```

---

## 7. Functional Programming Perspective

### How FP Achieves Each Principle Without OOP

| Principle | Critique in Functional Context | Functional Equivalent |
|-----------|-------------------------------|----------------------|
| **SRP** | Already natural in FP: each function does one thing via composition of pure functions | Single-purpose functions composed with `pipe`/`compose` |
| **OCP** | Achieved via higher-order functions and composition, not inheritance | `map`, `filter`, `reduce` as closed-for-modification abstractions |
| **LSP** | Doesn't directly apply — FP uses duck typing and algebraic types (union types), not subtyping | Discriminated unions and pattern matching instead of class hierarchies |
| **ISP** | Natural in FP: functions receive only what they need; TypeScript's `Pick<T, K>` | Partial application, dependency injection via function arguments |
| **DIP** | Realized via currying, partial application, and passing functions as arguments | Higher-order functions that accept "dependencies" as parameters |

### Functional OCP Example (TypeScript)

```typescript
// ✅ OCP in functional style — no classes, no inheritance
type ShippingFn = (order: Order) => number;

const pacShipping: ShippingFn = (order) => order.weight * 0.5;
const expressShipping: ShippingFn = (order) => order.weight * 2.5;
const droneShipping: ShippingFn = (order) => order.weight * 5.0 + 10.0;

// Closed for modification, open for extension — no classes needed
const calculateShipping = (strategy: ShippingFn, order: Order): number =>
  strategy(order);

// Adding a new shipping method = new function
const internationalShipping: ShippingFn = (order) =>
  order.weight * 3.0 + order.distance * 0.01;
```

### Functional DIP Example (TypeScript)

```typescript
// ✅ DIP in functional style
// The "abstraction" is a function type
type SaveFn<T> = (entity: T) => Promise<void>;
type SendEmailFn = (to: string, body: string) => Promise<void>;

// High-level orchestration — depends on function types (abstractions)
const createUser = (
  save: SaveFn<User>,
  sendEmail: SendEmailFn
) => async (data: CreateUserDto): Promise<void> => {
  const user = { id: crypto.randomUUID(), ...data };
  await save(user);
  await sendEmail(user.email, 'Welcome!');
};

// Implementations are injected as functions
const saveToPostgres: SaveFn<User> = async (user) => {
  await pg.query('INSERT INTO users ...', [user]);
};

const sendSESEmail: SendEmailFn = async (to, body) => {
  await ses.sendEmail({ to, body });
};

// Compose
const createUserWithPostgres = createUser(saveToPostgres, sendSESEmail);
```

---

## 8. Criticisms of SOLID

### Overengineering & YAGNI

Several prominent voices in software engineering have criticized the dogmatic application of SOLID principles:

- **Dan North** (creator of BDD): Criticized the "Clean Code industry" for promoting unnecessary abstractions that increase accidental complexity. His talk "Decoding SOLID" reinterprets the principles as diagnostic tools rather than prescriptive rules.

- **DHH** (creator of Ruby on Rails): Rails deliberately violates several SOLID principles in favor of productivity. The "Rails Way" prioritizes convention over configuration and rapid iteration over strict abstraction boundaries.

- **Kevlin Henney**: Argues that principles are *guidelines*, not laws — context dictates application. What's appropriate for a banking system may be harmful for a prototype.

- **"The Dark Side of Clean Code" critiques (2020s)**: Growing sentiment that SOLID and DRY, when poorly applied, actively harm code by creating:
  - Premature abstraction
  - Accidental complexity
  - Coupling between modules that don't need to be coupled
  - "Architecture astronaut" syndrome

### When NOT to Apply SOLID Rigidly

| Scenario | Why | Better Approach |
|----------|-----|-----------------|
| One-page scripts / prototypes | Abstraction overhead > benefit | Just write the code |
| MVPs and early-stage products | Speed of iteration matters | Refactor later when patterns emerge |
| Simple glue/config code | Too little complexity to justify layers | Keep it simple |
| Functional-first languages (Clojure, Elixir) | Principles assume OOP class hierarchy | FP idioms achieve same goals naturally |
| Performance-critical hot paths | Virtual dispatch and indirection have cost | Inline, avoid abstractions |

### Specific Criticisms by Principle

| Principle | Common Criticism |
|-----------|------------------|
| **SRP** | "What is *one* responsibility?" is highly subjective — can lead to anemic classes or class explosion with dozens of tiny classes | 
| **OCP** | Premature abstractions violate YAGNI — not every extension point needs an abstract interface or base class |
| **LSP** | Less relevant in structurally-typed languages (TypeScript, Go) where duck typing replaces nominal subtyping |
| **ISP** | Can lead to excessive interface granularity ("interface explosion") — too many single-method interfaces |
| **DIP** | Inversion can add unnecessary complexity in small projects — a concrete dependency is sometimes fine |

### Balanced View

> *"SOLID principles are diagnostic tools, not prescriptive laws. They help identify smells in existing code. Applying them preemptively — before you have evidence the smell exists — risks overengineering."*

The most mature interpretation uses SOLID as a **code smell detector**:
1. Write simple, direct code first
2. When a specific change hurts (too many files to modify), identify which principle is being violated
3. Refactor to address that specific pain point
4. Stop when the pain stops — don't abstract for hypothetical futures

---

## 9. SRP vs Separation of Concerns (SoC)

### Comparison Table

| Aspect | SoC (Separation of Concerns) | SRP (Single Responsibility Principle) |
|--------|------------------------------|---------------------------------------|
| **Scope** | Broad architecture (layers, systems, subsystems) | Classes, modules, functions |
| **Origin** | Edsger Dijkstra (1974) — "On the role of scientific thought" | Robert C. Martin (2000/2002) — Agile Software Development |
| **Criterion** | "Concern" — a distinct area of interest (e.g., business logic vs. infrastructure vs. presentation) | "Actor" — a group of stakeholders who can request a change |
| **Granularity** | Macro level (systems, layers, tiers) | Micro level (classes, methods, functions) |
| **Focus** | System organization and modular decomposition | Who can request changes and why |
| **Paradigm** | Applies to all paradigms (functional, procedural, OOP) | Primarily OOP class design |
| **Example** | MVC pattern: Model / View / Controller layers | `PayCalculator` vs `HourReporter` separated by actor (Finance vs HR) |

### Relationship

- **SoC is more general:** It applies to any paradigm (functional, procedural, object-oriented) and to any level of system architecture.
- **SRP is a specialization** of SoC for OOP class design — it answers a specific question that SoC doesn't address: *"Who will ask to change this class?"*
- **SoC asks:** "What concern does this module address?" (e.g., "data access", "business logic", "presentation")
- **SRP asks:** "Which actor(s) can request a change to this code?" (e.g., "the Finance team can request changes to pay calculation")

### Key Nuance

Two classes can address the **same concern** (e.g., both are part of the "business logic" layer) but violate SRP if they serve **different actors** within that concern. Conversely, a class can address **different concerns** (e.g., does validation AND persistence) but satisfy SRP if the **same actor** requests both sets of changes.

### Practical Guidance

| You should think in terms of... | When applying... |
|-------------------------------|------------------|
| Layers and boundaries | SoC |
| Who will change this code | SRP |
| Cohesion within a module | SoC |
| Class-level maintainability | SRP |
| System architecture | SoC |
| Dependency management | Both |

---

## 10. References

### Books

1. **Martin, Robert C.** *Agile Software Development, Principles, Patterns, and Practices.* Pearson, 2002. ISBN 0135974445. — The canonical book covering SOLID principles, package principles, and GoF patterns.
2. **Martin, Robert C.** *Clean Architecture: A Craftsman's Guide to Software Structure and Design.* Prentice Hall, 2017. — Expands on DIP and architectural implications of SOLID.
3. **Martin, Robert C.** *Clean Code: A Handbook of Agile Software Craftsmanship.* Prentice Hall, 2008. — Covers SRP and low-level application.
4. **Meyer, Bertrand.** *Object-Oriented Software Construction.* Prentice Hall, 1988. — OCP original definition (first edition).
5. **Gamma, Erich, et al.** *Design Patterns: Elements of Reusable Object-Oriented Software.* Addison-Wesley, 1994. (GoF) — Patterns that help implement SOLID principles.
6. **Freeman, Steve, & Pryce, Nat.** *Growing Object-Oriented Software, Guided by Tests.* Addison-Wesley, 2009. — Practical application of DIP and OCP with TDD.
7. **Yourdon, Edward, & Constantine, Larry L.** *Structured Design: Fundamentals of a Discipline of Computer Program and Systems Design.* 1979. — Foundations of cohesion and coupling that influenced SRP.

### Original Papers & Articles

8. **Martin, Robert C.** "The Principles of OOD." Object Mentor, 2000. *(butunclebob.com)* — The article listing 11 OOD principles.
9. **Liskov, Barbara.** "Data Abstraction and Hierarchy." Keynote, OOPSLA 1987. — Original presentation of LSP.
10. **Liskov, Barbara, & Wing, Jeannette.** "A Behavioral Notion of Subtyping." *ACM Transactions on Programming Languages and Systems (TOPLAS)*, Vol. 16, No. 6, November 1994. — Formalization of LSP.
11. **Martin, Robert C.** "The Interface Segregation Principle." *C++ Report*, 1996.
12. **Martin, Robert C.** "The Dependency Inversion Principle." *C++ Report*, 1996.
13. **Martin, Robert C.** "The Single Responsibility Principle." *The Principles of OOD*, 2002.
14. **Dijkstra, Edsger W.** "On the role of scientific thought." 1974. — Origin of Separation of Concerns (EWD 447).
15. **Meyer, Bertrand.** "Applying 'Design by Contract'." *Computer*, Vol. 25, No. 10, 1992. — Formal preconditions/postconditions that underpin LSP behavioral rules.

### Online Resources

16. Wikipedia — [SOLID](https://en.wikipedia.org/wiki/SOLID)
17. DigitalOcean — [SOLID Design Principles Explained](https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design)
18. Baeldung — [A Solid Guide to SOLID Principles](https://www.baeldung.com/solid-principles)
19. Real Python — [SOLID Design Principles in Python](https://realpython.com/solid-principles-python/)
20. Martin Fowler — [DIP in the Wild](https://martinfowler.com/articles/dipInTheWild.html)
21. JSDev.Space — [SOLID Principles in React](https://jsdev.space/react-solid-srp-ocp/)
22. Incubyte Blog — [SOLID Principles in React](https://blog.incubyte.co/blog/solid-principles-in-react-a-simple-and-practical-guide/)
23. Dev.to — [Do SOLID Principles Apply to FP?](https://dev.to/patferraggi/do-the-solid-principles-apply-to-functional-programming-56lm)
24. Baeldung — [When SOLID May Not Be Appropriate](https://www.baeldung.com/cs/solid-principles-avoid)
25. Stack Overflow — [Difference between SRP and SoC](https://stackoverflow.com/questions/1724469)
26. Clean Coder Blog — [The Principles of OOD](http://butunclebob.com/ArticleS.UncleBob.PrinciplesOfOod)

### Talks

27. **Robert C. Martin** — "SOLID Principles" (Clean Coders video series)
28. **Barbara Liskov** — "Data Abstraction and Hierarchy" (OOPSLA 1987 keynote)
29. **Klaus Iglberger** — "Breaking Dependencies: The SOLID Principles" (CppCon 2020)
30. **Dan North** — "Decoding SOLID" (critique and reinterpretation of the principles as diagnostic tools)
31. **Kevlin Henney** — "What I Wish I Had Known About SOLID" (NDC conferences)

---

> *"Principles are not laws. Their value lies not in rigid adherence but in the questions they force us to ask about our design."*
