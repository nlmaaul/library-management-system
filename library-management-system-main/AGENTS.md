<!-- GSD:project-start source:PROJECT.md -->

## Project

**Library Management System**

Library Management System is a web application for university students and librarians. Students use it to find books, request loans, track due dates, and return borrowed books, while librarians manage the catalog, approve requests, monitor overdue loans, and review borrowing statistics.

**Core Value:** Students can reliably find and borrow available library books through a clear digital workflow.

### Constraints

- **Application**: Python with Flask — one simple server-rendered web application.
- **Frontend**: Jinja HTML templates with basic CSS and optional Bootstrap — no separate JavaScript frontend required.
- **Database**: SQLite through SQLAlchemy — no separate database server.
- **Email**: Python SMTP integration with credentials supplied through environment variables.
- **Runtime**: Run locally with Python and a virtual environment; Docker is not required.
- **Timeline**: Four weeks — scope must remain achievable within the course deadline.
- **Team**: Four student developers — work should be divisible with clear ownership and integration boundaries.

<!-- GSD:project-end -->

<!-- GSD:stack-start source:STACK.md -->

## Technology Stack

- Python 3.12+
- Flask for routing, sessions, and server-rendered pages
- Jinja2 templates with basic CSS or Bootstrap
- SQLAlchemy ORM with SQLite
- Werkzeug password hashing for local authentication
- Python `smtplib` or Flask-Mail for overdue email notifications
- `pytest` for automated tests
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->

## Conventions

- Keep the app as a small Flask monolith unless a feature clearly needs extraction.
- Use SQLAlchemy models in `app.py` for the core entities: `User`, `Book`, and `Loan`.
- Protect authenticated routes with `login_required` or `role_required`.
- Student-only workflows must never expose librarian actions in templates or routes.
- Librarian-only workflows live under `/librarian`.
- Use server-rendered Jinja templates and local CSS in `static/style.css`.
- Add focused pytest coverage for each workflow-level change.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->

## Architecture

The application is a single Flask server-rendered app.

- `app.py` contains application setup, SQLAlchemy models, route registration, database seeding, overdue email sending, and CLI commands.
- `templates/` contains Jinja views grouped by workflow: `auth`, `catalog`, `loans`, and `librarian`.
- `static/style.css` contains the local responsive UI styles.
- `tests/test_app.py` verifies the primary student and librarian workflows using an in-memory SQLite database.
- SQLite is the default runtime database through `sqlite:///library.db`.
- SMTP settings are read from environment variables; when `SMTP_HOST` is absent, overdue email delivery is skipped locally.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->

## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->

## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:

- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->

<!-- GSD:profile-start -->

## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
