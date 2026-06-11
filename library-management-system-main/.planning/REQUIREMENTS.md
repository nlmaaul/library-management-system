# Requirements: Library Management System

**Defined:** 2026-06-11
**Core Value:** Students can reliably find and borrow available library books through a clear digital workflow.

## v1 Requirements

### Authentication

- [x] **AUTH-01**: Student can register with email and password.
- [x] **AUTH-02**: Registered user can log in and log out.
- [x] **AUTH-03**: System restricts features according to student or librarian role.

### Catalog

- [x] **CAT-01**: Student can browse the book catalog.
- [x] **CAT-02**: Student can search books by title, author, or ISBN.
- [x] **CAT-03**: Student can filter books by category and availability.
- [x] **CAT-04**: Student can view book details and current availability.
- [x] **CAT-05**: Librarian can add, edit, and remove books.

### Borrowing

- [x] **LOAN-01**: Student can request an available book.
- [x] **LOAN-02**: Librarian can approve or reject a borrowing request.
- [x] **LOAN-03**: Student can view request status, active loans, and due dates.
- [x] **LOAN-04**: Librarian can record returned books.
- [x] **LOAN-05**: System marks loans overdue after their due date.
- [x] **LOAN-06**: Librarian can view active and overdue loans.

### Notifications

- [x] **NOTF-01**: System emails a student when their loan becomes overdue.

### Dashboard

- [x] **DASH-01**: Librarian can view borrowing totals and overdue statistics.

## v2 Requirements

Deferred to a future release; no additional v2 requirements are currently committed.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Payment and fine processing | Not required for the four-week physical-book circulation MVP |
| E-book reading | The project manages physical library inventory and loans only |
| Native mobile application | The initial release is a responsive web application |

## Traceability

Roadmap phase mappings will be added during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| AUTH-01 | Phase 1 | Implemented |
| AUTH-02 | Phase 1 | Implemented |
| AUTH-03 | Phase 1 | Implemented |
| CAT-01 | Phase 1 | Implemented |
| CAT-02 | Phase 1 | Implemented |
| CAT-03 | Phase 1 | Implemented |
| CAT-04 | Phase 1 | Implemented |
| CAT-05 | Phase 2 | Implemented |
| LOAN-01 | Phase 2 | Implemented |
| LOAN-02 | Phase 2 | Implemented |
| LOAN-03 | Phase 2 | Implemented |
| LOAN-04 | Phase 3 | Implemented |
| LOAN-05 | Phase 3 | Implemented |
| LOAN-06 | Phase 3 | Implemented |
| NOTF-01 | Phase 3 | Implemented |
| DASH-01 | Phase 4 | Implemented |

**Coverage:**
- v1 requirements: 16 total
- Mapped to phases: 16
- Unmapped: 0

---
*Requirements defined: 2026-06-11*
*Last updated: 2026-06-11 after MVP implementation*
