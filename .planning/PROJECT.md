# Library Management System

## What This Is

Library Management System is a web application for university students and librarians. Students use it to find books, request loans, track due dates, and return borrowed books, while librarians manage the catalog, approve requests, monitor overdue loans, and review borrowing statistics.

## Core Value

Students can reliably find and borrow available library books through a clear digital workflow.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Users can register and log in with separate student and librarian roles.
- [ ] Students can browse, search, and filter the book catalog.
- [ ] Students can submit borrowing requests and librarians can approve or reject them.
- [ ] The system tracks active loans, returns, due dates, and overdue status.
- [ ] The system sends overdue alerts by email.
- [ ] Librarians can add, edit, and remove catalog books.
- [ ] Librarians can view a dashboard with borrowing statistics and overdue books.

### Out of Scope

- Payment processing — fines and online payments are not part of this project.
- E-book reading — the system manages physical-library circulation only.
- Mobile application — the initial release is a responsive web application.

## Context

University students currently cannot easily discover or borrow available books. Librarians manage catalog and circulation records in spreadsheets, which makes requests, due dates, returns, and overdue tracking difficult to coordinate. This project replaces that manual workflow with one shared digital system.

The project is a university assignment developed by a four-person student team over four weeks. Its primary users are students, whose goal is to locate and borrow books, and librarians, whose goal is to maintain the catalog and control circulation.

## Constraints

- **Backend**: Python with FastAPI preferred — required technology direction for the project.
- **Frontend**: React — required client-side framework.
- **Database**: PostgreSQL — required persistent data store.
- **Deployment**: The full application must run with Docker.
- **Timeline**: Four weeks — scope must remain achievable within the course deadline.
- **Team**: Four student developers — work should be divisible with clear ownership and integration boundaries.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Build a role-based web application | Students and librarians need different capabilities within one system | — Pending |
| Use FastAPI, React, and PostgreSQL | Matches the required technology preferences and supports a conventional API-driven architecture | — Pending |
| Package the system with Docker | The application must run consistently across development and evaluation environments | — Pending |
| Limit v1 to physical-book circulation | Keeps the four-week scope focused on the core library workflow | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `$gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `$gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-06-11 after initialization*
