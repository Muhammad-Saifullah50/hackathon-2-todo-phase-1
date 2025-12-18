<!--
Sync Impact Report:
- Version: 0.0.0 → 1.0.0
- Rationale: Initial constitution creation for CLI Todo Application
- New sections added:
  * 10 Core Principles (Architecture, Code Quality, Testing, Data Management, Error Handling, User Experience, Performance & Scalability, Security & Safety, Python Standards, Development Workflow)
  * Python Tooling & Environment section
  * Code Review & Quality Gates section
- Templates requiring updates:
  ✅ plan-template.md - Constitution Check section will reference these principles
  ✅ spec-template.md - Requirements aligned with UX and functional principles
  ✅ tasks-template.md - Task organization reflects testing and architecture principles
- No deferred placeholders
-->

# CLI Todo Application Constitution

## Core Principles

### I. Architecture & Design - Separation of Concerns

The application MUST maintain clear boundaries between layers to ensure modularity, testability, and future extensibility.

**Rules:**
- CLI interface, business logic, and data persistence MUST be independent layers
- Each module, class, and function has ONE clear purpose (Single Responsibility Principle)
- Dependencies MUST be passed explicitly via dependency injection; no global state
- Define clear contracts using Python protocols/abstract base classes between layers
- Each CLI command MUST be an independent, testable unit following the Command Pattern

**Rationale:** Separation of concerns enables isolated testing, easier refactoring, and the ability to swap implementations (e.g., JSON → SQLite storage) without cascading changes. This architecture supports long-term maintainability and scalability.

### II. Code Quality - Explicit & Self-Documenting

Code clarity and explicit behavior take precedence over cleverness or brevity.

**Rules:**
- Type hints MUST be used everywhere; enforce with mypy strict mode
- Code MUST be self-documenting; avoid magic or implicit behaviors
- DRY (Don't Repeat Yourself) - Extract common patterns, but avoid premature abstraction
- YAGNI (You Aren't Gonna Need It) - Build what's needed now; don't over-engineer for hypothetical futures
- Fail Fast - Validate inputs early at system boundaries; raise clear, specific exceptions

**Rationale:** Explicit code reduces cognitive load, makes intent clear to reviewers and future maintainers, and prevents subtle bugs from implicit behaviors. Type hints enable better tooling support and catch errors at development time.

### III. Testing - Test-Driven Development (NON-NEGOTIABLE)

Testing is mandatory and MUST follow strict Test-Driven Development (TDD) discipline.

**Rules:**
- **RED-GREEN-REFACTOR cycle MUST be followed strictly:**
  1. **RED**: Write tests FIRST; verify they FAIL before implementation
  2. **GREEN**: Write minimal code to make tests pass
  3. **REFACTOR**: Clean up code while keeping tests green
- Tests MUST be written BEFORE any implementation code (no exceptions)
- 100% of tests MUST pass before code can be committed or merged
- Test pyramid MUST be followed: Many unit tests, fewer integration tests, minimal end-to-end tests
- Tests MUST be independent: No shared state or execution order dependencies
- Code coverage MUST maintain minimum 80% threshold
- External dependencies (file I/O, network) MUST be mocked in unit tests
- Each test MUST test ONE thing and have a clear, descriptive name

**Rationale:** TDD ensures code is testable by design, prevents over-engineering, and provides immediate feedback. Writing tests first forces clear thinking about requirements and API design. 100% test pass rate is non-negotiable because failing tests indicate broken functionality or incorrect tests—both must be fixed immediately.

### IV. Data Management - Single Source of Truth

Data integrity and consistency are paramount; all data operations must be safe and predictable.

**Rules:**
- One canonical data store (JSON file initially, designed for future database migration)
- All read-modify-write operations MUST be atomic to prevent data corruption
- Data validation MUST occur at system boundaries (user input and persistence layer)
- Schema versioning MUST be planned from day one for data format evolution
- Backwards compatibility MUST be maintained; never break existing user data

**Rationale:** Data is the most valuable asset. Atomic operations prevent race conditions and corruption. Schema versioning and backwards compatibility ensure users can upgrade without data loss or manual migration.

### V. Error Handling - Clear & User-Friendly

Errors must be handled gracefully with messages that guide users toward resolution.

**Rules:**
- Define custom exception types for domain-specific errors
- CLI errors MUST show user-friendly messages; no raw stack traces in production mode
- Graceful degradation: Handle corrupted/missing data files without crashing
- Logging MUST capture errors with full context for debugging while keeping user output clean
- Every error message MUST be actionable (tell the user what went wrong and how to fix it)

**Rationale:** Good error handling distinguishes professional tools from prototypes. Users should never see technical stack traces; they need clear guidance. Developers need detailed logs for debugging without polluting user experience.

### VI. User Experience - Beautiful & Intuitive CLI (NON-NEGOTIABLE)

The application MUST provide a visually appealing, intuitive interface that delights users even in a terminal environment.

**Rules:**
- Visual hierarchy MUST use colors, tables, and panels for clarity (via `rich` library)
- Interactive menus MUST be used for all commands requiring input (via `questionary` library)
- Consistent feedback: Every action MUST show immediate, visible confirmation with appropriate visual treatment
- Progressive disclosure: Show summaries by default; provide details on demand
- Accessibility: Provide `--simple` mode for scripting, piping, and screen reader compatibility
- Color + symbols: Don't rely on color alone (support colorblind users)
- Empty states: Show helpful, beautiful messages when no todos exist (not blank output)
- Consistent color scheme: Success (green), warnings (yellow), errors (red), info (blue)

**Rationale:** User experience is not a luxury in CLI tools. Beautiful, intuitive interfaces increase adoption, reduce support burden, and demonstrate craftsmanship. Interactive menus reduce errors and cognitive load compared to memorizing command flags.

### VII. Performance & Scalability - Efficient by Design

The application must perform efficiently at expected scale and be designed for future growth.

**Rules:**
- MUST handle thousands of todos without performance degradation
- Lazy loading: Load data only when needed
- Storage layer MUST be pluggable: Design allows swapping JSON → SQLite → Database later
- Use appropriate data structures for O(1) lookups where needed (indexed access by ID)
- Avoid premature optimization, but measure and optimize hot paths

**Rationale:** While over-engineering is wasteful, ignoring performance creates technical debt. Pluggable storage and efficient data structures ensure the app can scale when users need it without requiring a complete rewrite.

### VIII. Security & Safety - Secure by Default

Security and data safety must be considered from the start, not bolted on later.

**Rules:**
- Input sanitization: Validate and sanitize ALL user input
- File permissions: Set appropriate read/write permissions on data files (user-only access)
- No secrets in code: Never hardcode paths, credentials, or sensitive data
- Safe defaults: Secure by default; explicit opt-in for risky operations (e.g., delete requires confirmation)
- Path traversal protection: Validate all file paths to prevent directory traversal attacks

**Rationale:** Security vulnerabilities in personal productivity tools can expose sensitive data. Input validation prevents injection attacks. Proper file permissions prevent unauthorized access. Safe defaults prevent accidental data loss.

### IX. Python Standards - Modern & Professional

Code must follow Python community standards and leverage modern language features.

**Rules:**
- PEP 8 compliance MUST be followed (enforced via tooling)
- Python 3.13+ features MUST be used where appropriate (pattern matching, improved type hints)
- Type checking: Run mypy in strict mode (no implicit Any types)
- Linting: Use ruff for fast, comprehensive linting (replaces flake8, isort, etc.)
- Formatting: Use black for consistent, opinionated code formatting
- Dependency management: Use uv for fast, reproducible virtual environments and dependencies
- All code MUST pass type checking, linting, and formatting checks before commit

**Rationale:** Following Python standards ensures code is familiar to other Python developers. Modern tooling (ruff, black, mypy, uv) provides fast feedback and catches issues before they reach production. Python 3.13 features improve code clarity and performance.

### X. Development Workflow - Spec-Driven & Systematic

Development follows a disciplined, spec-driven approach to ensure quality and traceability.

**Rules:**
- Spec-Driven Development MUST be followed: Spec → Plan → Tasks → Implementation
- Small, atomic commits: Each commit represents ONE logical change with clear message
- Commit messages MUST follow Conventional Commits format (feat:, fix:, docs:, etc.)
- Branch per feature: Isolated development branches (###-feature-name format)
- Code review ready: All code MUST be self-explanatory or have clear comments explaining "why" (not "what")
- Every user interaction MUST be recorded in a Prompt History Record (PHR)
- Architecturally significant decisions MUST be documented in Architecture Decision Records (ADRs)

**Rationale:** Spec-driven development prevents scope creep and ensures alignment before implementation. Small commits enable easy rollback and clear history. Conventional commits enable automated changelog generation. PHRs and ADRs provide project memory and onboarding material.

## Python Tooling & Environment

**Mandatory Tools:**
- **Python Version**: 3.13+
- **Dependency Manager**: uv (fast, modern alternative to pip/poetry)
- **Type Checker**: mypy (strict mode)
- **Linter**: ruff (replaces flake8, pylint, isort, pyupgrade)
- **Formatter**: black
- **UI Libraries**: rich (formatting), questionary (interactive prompts)
- **Testing**: pytest with pytest-cov for coverage
- **Virtual Environment**: Managed by uv

**Installation & Setup:**
```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
uv pip install -r requirements.txt

# Run quality checks
ruff check .
black --check .
mypy .
pytest --cov=src tests/
```

**Pre-commit Requirements:**
All commits MUST pass:
1. `ruff check .` (no linting errors)
2. `black --check .` (proper formatting)
3. `mypy .` (type checking passes)
4. `pytest` (100% of tests pass, minimum 80% coverage)

## Code Review & Quality Gates

**Before Merging:**
- [ ] All tests pass (100% pass rate, minimum 80% coverage)
- [ ] Tests were written BEFORE implementation (TDD compliance)
- [ ] Type checking passes (mypy strict mode)
- [ ] Linting passes (ruff with no errors)
- [ ] Code formatted (black)
- [ ] No hardcoded secrets or paths
- [ ] Error handling includes user-friendly messages
- [ ] UI follows visual hierarchy principles (tables for lists, panels for feedback)
- [ ] Interactive prompts used appropriately
- [ ] Documentation updated if public API changed
- [ ] Commit messages follow Conventional Commits
- [ ] PHR created for significant user interactions
- [ ] ADR created for architecturally significant decisions (if applicable)

## Governance

This constitution supersedes all other development practices and coding standards for this project. All code, designs, and decisions MUST align with these principles.

**Amendment Process:**
1. Propose changes via issue or discussion with clear rationale
2. Document impact on existing code and practices
3. Update constitution with new version number following semantic versioning:
   - MAJOR: Backward-incompatible governance changes or principle removals
   - MINOR: New principles added or materially expanded guidance
   - PATCH: Clarifications, wording fixes, non-semantic refinements
4. Update all dependent templates (plan, spec, tasks) to reflect changes
5. Migration plan required if existing code must be updated

**Compliance:**
- All pull requests MUST verify compliance with this constitution
- Complexity violations MUST be justified in the Complexity Tracking section of plan.md
- Constitution checks are mandatory gates in the planning phase
- Non-compliance blocks merge; no exceptions without explicit documentation

**References:**
- Runtime development guidance: See `CLAUDE.md` for agent-specific instructions
- Template files: `.specify/templates/` for spec, plan, and task templates
- Example code: Follow patterns established in existing codebase

---

**Version**: 1.0.0 | **Ratified**: 2025-12-18 | **Last Amended**: 2025-12-18
