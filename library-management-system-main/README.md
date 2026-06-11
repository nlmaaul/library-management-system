# Library Management System

A simple Flask and SQLite library management application for students and librarians.

## Features

- Student registration, login, logout, and role-based access control
- Book catalog browsing, search, category filter, and availability filter
- Student borrowing requests with duplicate and availability checks
- Librarian catalog management, request approval or rejection, return recording, and loan views
- Overdue detection, overdue email command, and librarian dashboard statistics

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app init-db
flask --app app run
```

Open `http://127.0.0.1:5000`.

The seed librarian account is:

- Email: `librarian@example.com`
- Password: `password`

## Email Configuration

Overdue email alerts are sent by:

```bash
flask --app app send-overdue-alerts
```

Set these environment variables for SMTP delivery:

- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `SMTP_FROM`

If `SMTP_HOST` is not set, the command logs skipped email output locally and still marks overdue loans as notified.

## Tests

```bash
pytest
```
