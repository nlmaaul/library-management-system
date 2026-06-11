# Roadmap: Library Management System

## Overview

The project progresses through four vertical MVP slices. It first delivers secure student access to a searchable catalog, then adds the librarian-controlled borrowing workflow, completes circulation with returns and overdue handling, and finishes with operational visibility and release readiness.

## Phases

- [ ] **Phase 1: Student Access and Catalog Discovery** - Students can authenticate and find available books.
- [ ] **Phase 2: Borrowing Request Workflow** - Students request books and librarians manage catalog and approvals.
- [ ] **Phase 3: Returns and Overdue Control** - The complete loan lifecycle, overdue tracking, and email alerts work.
- [ ] **Phase 4: Librarian Insights and Release Readiness** - Librarians see circulation statistics and the Dockerized system is ready for evaluation.

## Phase Details

### Phase 1: Student Access and Catalog Discovery
**Goal**: Students can securely access the system and discover books they can borrow.
**Mode:** mvp
**Depends on**: Nothing (first phase)
**Requirements**: AUTH-01, AUTH-02, AUTH-03, CAT-01, CAT-02, CAT-03, CAT-04
**UI hint**: yes
**Success Criteria** (what must be TRUE):
  1. A student can register, log in, remain authorized for student-only pages, and log out.
  2. A student can browse the catalog and open complete details for a selected book.
  3. A student can search by title, author, or ISBN and filter results by category and availability.
  4. A librarian account cannot be treated as a student account, and student users cannot access librarian-only actions.
**Plans**: TBD

### Phase 2: Borrowing Request Workflow
**Goal**: Students can request available books while librarians maintain inventory and control approvals.
**Mode:** mvp
**Depends on**: Phase 1
**Requirements**: CAT-05, LOAN-01, LOAN-02, LOAN-03
**UI hint**: yes
**Success Criteria** (what must be TRUE):
  1. A librarian can add, edit, and remove catalog records without exposing those controls to students.
  2. A student can request an available book and cannot create an invalid duplicate or unavailable-book request.
  3. A librarian can approve or reject each pending request and the book availability reflects approved borrowing.
  4. A student can see request status, active loans, and due dates from their account.
**Plans**: TBD

### Phase 3: Returns and Overdue Control
**Goal**: Librarians can complete the circulation lifecycle and students are informed when loans are overdue.
**Mode:** mvp
**Depends on**: Phase 2
**Requirements**: LOAN-04, LOAN-05, LOAN-06, NOTF-01
**UI hint**: yes
**Success Criteria** (what must be TRUE):
  1. A librarian can record a return and the returned book becomes available again.
  2. A loan past its due date is automatically identifiable as overdue.
  3. A librarian can view current active loans and overdue loans separately.
  4. A student receives an email alert when their active loan becomes overdue without duplicate alerts being sent unintentionally.
**Plans**: TBD

### Phase 4: Librarian Insights and Release Readiness
**Goal**: Librarians can assess circulation activity and the integrated application is ready to run consistently for evaluation.
**Mode:** mvp
**Depends on**: Phase 3
**Requirements**: DASH-01
**UI hint**: yes
**Success Criteria** (what must be TRUE):
  1. A librarian can view borrowing totals and current overdue statistics derived from real loan data.
  2. Dashboard statistics update when requests are approved, books are returned, or loans become overdue.
  3. The React frontend, FastAPI backend, PostgreSQL database, and supporting services start through Docker with documented setup steps.
  4. End-to-end verification confirms the primary student and librarian workflows operate together without role or inventory inconsistencies.
**Plans**: TBD

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Student Access and Catalog Discovery | 0/TBD | Not started | - |
| 2. Borrowing Request Workflow | 0/TBD | Not started | - |
| 3. Returns and Overdue Control | 0/TBD | Not started | - |
| 4. Librarian Insights and Release Readiness | 0/TBD | Not started | - |

