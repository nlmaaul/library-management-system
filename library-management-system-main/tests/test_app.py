from datetime import date, timedelta

import pytest

from app import Book, Loan, User, create_app, db, seed_data, send_overdue_alerts


@pytest.fixture()
def app():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SECRET_KEY": "test",
        }
    )
    with app.app_context():
        db.create_all()
        seed_data()
        student = User(name="Student One", email="student@example.com", role="student")
        student.set_password("password")
        db.session.add(student)
        db.session.commit()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def login(client, email, password="password"):
    return client.post("/login", data={"email": email, "password": password}, follow_redirects=True)


def test_student_can_register_login_and_view_catalog(client):
    response = client.post(
        "/register",
        data={"name": "New Student", "email": "new@example.com", "password": "secret"},
        follow_redirects=True,
    )
    assert b"Registration successful" in response.data
    assert b"Book Catalog" in response.data

    client.post("/logout", follow_redirects=True)
    response = login(client, "new@example.com", "secret")
    assert b"Logged in successfully" in response.data


def test_role_restrictions_block_student_from_librarian_pages(client):
    login(client, "student@example.com")
    response = client.get("/librarian", follow_redirects=True)
    assert b"You do not have permission" in response.data
    assert b"Book Catalog" in response.data


def test_catalog_search_and_filters(client):
    response = client.get("/catalog?q=Clean&category=Software+Engineering&availability=available")
    assert b"Clean Code" in response.data
    assert b"Introduction to Algorithms" not in response.data


def test_student_request_and_librarian_approval_updates_availability(client, app):
    login(client, "student@example.com")
    with app.app_context():
        book_id = Book.query.filter_by(title="Clean Code").first().id

    response = client.post(f"/books/{book_id}/request", follow_redirects=True)
    assert b"Borrow request submitted" in response.data

    duplicate = client.post(f"/books/{book_id}/request", follow_redirects=True)
    assert b"already have a pending request" in duplicate.data

    client.post("/logout", follow_redirects=True)
    login(client, "librarian@example.com")

    with app.app_context():
        loan = Loan.query.filter_by(book_id=book_id, status="pending").first()
        loan_id = loan.id
        available_before = loan.book.available_copies

    response = client.post(f"/librarian/requests/{loan_id}/approve", follow_redirects=True)
    assert b"Request approved" in response.data

    with app.app_context():
        loan = db.session.get(Loan, loan_id)
        assert loan.status == "active"
        assert loan.due_date == date.today() + timedelta(days=14)
        assert loan.book.available_copies == available_before - 1


def test_return_records_loan_and_restores_copy(client, app):
    with app.app_context():
        student = User.query.filter_by(email="student@example.com").first()
        book = Book.query.filter_by(title="Clean Code").first()
        book.available_copies -= 1
        loan = Loan(student_id=student.id, book_id=book.id, status="active", due_date=date.today())
        db.session.add(loan)
        db.session.commit()
        loan_id = loan.id
        available_before = book.available_copies

    login(client, "librarian@example.com")
    response = client.post(f"/librarian/loans/{loan_id}/return", follow_redirects=True)
    assert b"Return recorded" in response.data

    with app.app_context():
        loan = db.session.get(Loan, loan_id)
        assert loan.status == "returned"
        assert loan.book.available_copies == available_before + 1


def test_overdue_alert_marks_once(app, monkeypatch):
    sent = []

    def fake_send_email(to_email, subject, body):
        sent.append((to_email, subject, body))

    monkeypatch.setattr("app.send_email", fake_send_email)
    with app.app_context():
        student = User.query.filter_by(email="student@example.com").first()
        book = Book.query.first()
        db.session.add(
            Loan(
                student_id=student.id,
                book_id=book.id,
                status="active",
                due_date=date.today() - timedelta(days=1),
            )
        )
        db.session.commit()

        assert send_overdue_alerts() == 1
        assert send_overdue_alerts() == 0

    assert len(sent) == 1
