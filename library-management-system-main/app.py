from __future__ import annotations

import os
import smtplib
from datetime import UTC, date, datetime, timedelta
from email.message import EmailMessage
from functools import wraps

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="student")

    loans = db.relationship("Loan", back_populates="student", cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    author = db.Column(db.String(160), nullable=False, index=True)
    isbn = db.Column(db.String(40), unique=True, nullable=False, index=True)
    category = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text, default="")
    total_copies = db.Column(db.Integer, nullable=False, default=1)
    available_copies = db.Column(db.Integer, nullable=False, default=1)

    loans = db.relationship("Loan", back_populates="book", cascade="all, delete-orphan")

    @property
    def is_available(self) -> bool:
        return self.available_copies > 0


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default="pending", index=True)
    requested_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))
    approved_at = db.Column(db.DateTime)
    due_date = db.Column(db.Date)
    returned_at = db.Column(db.DateTime)
    overdue_notified_at = db.Column(db.DateTime)

    student = db.relationship("User", back_populates="loans")
    book = db.relationship("Book", back_populates="loans")

    @property
    def is_overdue(self) -> bool:
        return self.status == "active" and self.due_date is not None and self.due_date < date.today()


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-change-me"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "sqlite:///library.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        LOAN_DAYS=int(os.environ.get("LOAN_DAYS", "14")),
    )
    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    @app.context_processor
    def inject_globals() -> dict:
        return {"current_user": current_user()}

    @app.cli.command("init-db")
    def init_db_command() -> None:
        init_db(app)
        print("Database initialized with sample data.")

    @app.cli.command("send-overdue-alerts")
    def send_overdue_alerts_command() -> None:
        with app.app_context():
            sent = send_overdue_alerts()
            print(f"Sent {sent} overdue alert(s).")

    register_routes(app)
    return app


def init_db(app: Flask) -> None:
    with app.app_context():
        db.create_all()
        seed_data()


def seed_data() -> None:
    if not User.query.filter_by(email="librarian@example.com").first():
        librarian = User(name="Main Librarian", email="librarian@example.com", role="librarian")
        librarian.set_password("password")
        db.session.add(librarian)

    if Book.query.count() == 0:
        db.session.add_all(
            [
                Book(
                    title="Introduction to Algorithms",
                    author="Thomas H. Cormen",
                    isbn="9780262046305",
                    category="Computer Science",
                    description="A comprehensive reference for algorithms and data structures.",
                    total_copies=3,
                    available_copies=3,
                ),
                Book(
                    title="Clean Code",
                    author="Robert C. Martin",
                    isbn="9780132350884",
                    category="Software Engineering",
                    description="Practical guidance for writing readable and maintainable code.",
                    total_copies=2,
                    available_copies=2,
                ),
                Book(
                    title="Database System Concepts",
                    author="Abraham Silberschatz",
                    isbn="9780078022159",
                    category="Database",
                    description="Core concepts for relational databases and transaction systems.",
                    total_copies=2,
                    available_copies=2,
                ),
            ]
        )
    db.session.commit()


def current_user() -> User | None:
    user_id = session.get("user_id")
    if not user_id:
        return None
    return db.session.get(User, user_id)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if current_user() is None:
            flash("Please log in first.", "warning")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


def role_required(role: str):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            user = current_user()
            if user is None:
                flash("Please log in first.", "warning")
                return redirect(url_for("login", next=request.path))
            if user.role != role:
                flash("You do not have permission to access that page.", "danger")
                return redirect(url_for("catalog"))
            return view(*args, **kwargs)

        return wrapped

    return decorator


def register_routes(app: Flask) -> None:
    @app.route("/")
    def index():
        if current_user() and current_user().role == "librarian":
            return redirect(url_for("librarian_dashboard"))
        return redirect(url_for("catalog"))

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            if not name or not email or not password:
                flash("Name, email, and password are required.", "danger")
            elif User.query.filter_by(email=email).first():
                flash("Email is already registered.", "danger")
            else:
                user = User(name=name, email=email, role="student")
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                session["user_id"] = user.id
                flash("Registration successful.", "success")
                return redirect(url_for("catalog"))
        return render_template("auth/register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session["user_id"] = user.id
                flash("Logged in successfully.", "success")
                return redirect(request.args.get("next") or url_for("index"))
            flash("Invalid email or password.", "danger")
        return render_template("auth/login.html")

    @app.route("/logout", methods=["POST"])
    def logout():
        session.clear()
        flash("Logged out successfully.", "success")
        return redirect(url_for("login"))

    @app.route("/catalog")
    def catalog():
        query_text = request.args.get("q", "").strip()
        category = request.args.get("category", "").strip()
        availability = request.args.get("availability", "").strip()

        books_query = Book.query
        if query_text:
            like = f"%{query_text}%"
            books_query = books_query.filter(
                or_(Book.title.ilike(like), Book.author.ilike(like), Book.isbn.ilike(like))
            )
        if category:
            books_query = books_query.filter(Book.category == category)
        if availability == "available":
            books_query = books_query.filter(Book.available_copies > 0)
        elif availability == "unavailable":
            books_query = books_query.filter(Book.available_copies <= 0)

        books = books_query.order_by(Book.title.asc()).all()
        categories = [row[0] for row in db.session.query(Book.category).distinct().order_by(Book.category)]
        return render_template(
            "catalog/index.html",
            books=books,
            categories=categories,
            filters={"q": query_text, "category": category, "availability": availability},
        )

    @app.route("/books/<int:book_id>")
    def book_detail(book_id: int):
        book = db.get_or_404(Book, book_id)
        existing_request = None
        user = current_user()
        if user and user.role == "student":
            existing_request = Loan.query.filter(
                Loan.student_id == user.id,
                Loan.book_id == book.id,
                Loan.status.in_(["pending", "active"]),
            ).first()
        return render_template("catalog/detail.html", book=book, existing_request=existing_request)

    @app.route("/books/<int:book_id>/request", methods=["POST"])
    @role_required("student")
    def request_book(book_id: int):
        book = db.get_or_404(Book, book_id)
        user = current_user()
        duplicate = Loan.query.filter(
            Loan.student_id == user.id,
            Loan.book_id == book.id,
            Loan.status.in_(["pending", "active"]),
        ).first()
        if duplicate:
            flash("You already have a pending request or active loan for this book.", "warning")
        elif not book.is_available:
            flash("This book is not currently available.", "danger")
        else:
            db.session.add(Loan(student_id=user.id, book_id=book.id, status="pending"))
            db.session.commit()
            flash("Borrow request submitted.", "success")
        return redirect(url_for("book_detail", book_id=book.id))

    @app.route("/my-loans")
    @role_required("student")
    def my_loans():
        loans = (
            Loan.query.filter_by(student_id=current_user().id)
            .order_by(Loan.requested_at.desc())
            .all()
        )
        return render_template("loans/my_loans.html", loans=loans)

    @app.route("/librarian")
    @role_required("librarian")
    def librarian_dashboard():
        active_loans = Loan.query.filter_by(status="active").count()
        overdue_loans = Loan.query.filter_by(status="active").filter(Loan.due_date < date.today()).count()
        stats = {
            "books": Book.query.count(),
            "available_copies": db.session.query(db.func.coalesce(db.func.sum(Book.available_copies), 0)).scalar(),
            "pending_requests": Loan.query.filter_by(status="pending").count(),
            "active_loans": active_loans,
            "overdue_loans": overdue_loans,
            "returned_loans": Loan.query.filter_by(status="returned").count(),
        }
        return render_template("librarian/dashboard.html", stats=stats)

    @app.route("/librarian/books")
    @role_required("librarian")
    def manage_books():
        books = Book.query.order_by(Book.title.asc()).all()
        return render_template("librarian/books.html", books=books)

    @app.route("/librarian/books/new", methods=["GET", "POST"])
    @role_required("librarian")
    def new_book():
        if request.method == "POST":
            book = Book()
            if populate_book_from_form(book):
                db.session.add(book)
                db.session.commit()
                flash("Book added.", "success")
                return redirect(url_for("manage_books"))
        return render_template("librarian/book_form.html", book=None)

    @app.route("/librarian/books/<int:book_id>/edit", methods=["GET", "POST"])
    @role_required("librarian")
    def edit_book(book_id: int):
        book = db.get_or_404(Book, book_id)
        if request.method == "POST" and populate_book_from_form(book):
            db.session.commit()
            flash("Book updated.", "success")
            return redirect(url_for("manage_books"))
        return render_template("librarian/book_form.html", book=book)

    @app.route("/librarian/books/<int:book_id>/delete", methods=["POST"])
    @role_required("librarian")
    def delete_book(book_id: int):
        book = db.get_or_404(Book, book_id)
        active_count = Loan.query.filter(
            Loan.book_id == book.id,
            Loan.status.in_(["pending", "active"]),
        ).count()
        if active_count:
            flash("Cannot delete a book with pending requests or active loans.", "danger")
        else:
            db.session.delete(book)
            db.session.commit()
            flash("Book deleted.", "success")
        return redirect(url_for("manage_books"))

    @app.route("/librarian/requests")
    @role_required("librarian")
    def manage_requests():
        loans = Loan.query.filter_by(status="pending").order_by(Loan.requested_at.asc()).all()
        return render_template("librarian/requests.html", loans=loans)

    @app.route("/librarian/requests/<int:loan_id>/<action>", methods=["POST"])
    @role_required("librarian")
    def decide_request(loan_id: int, action: str):
        loan = db.get_or_404(Loan, loan_id)
        if loan.status != "pending":
            flash("This request is no longer pending.", "warning")
        elif action == "approve":
            if loan.book.available_copies <= 0:
                flash("No copies are available for this book.", "danger")
            else:
                loan.status = "active"
                loan.approved_at = datetime.now(UTC)
                loan.due_date = date.today() + timedelta(days=app.config["LOAN_DAYS"])
                loan.book.available_copies -= 1
                db.session.commit()
                flash("Request approved.", "success")
        elif action == "reject":
            loan.status = "rejected"
            db.session.commit()
            flash("Request rejected.", "success")
        else:
            flash("Unknown request action.", "danger")
        return redirect(url_for("manage_requests"))

    @app.route("/librarian/loans")
    @role_required("librarian")
    def manage_loans():
        active_loans = Loan.query.filter_by(status="active").order_by(Loan.due_date.asc()).all()
        overdue_loans = [loan for loan in active_loans if loan.is_overdue]
        current_loans = [loan for loan in active_loans if not loan.is_overdue]
        return render_template(
            "librarian/loans.html",
            current_loans=current_loans,
            overdue_loans=overdue_loans,
        )

    @app.route("/librarian/loans/<int:loan_id>/return", methods=["POST"])
    @role_required("librarian")
    def return_loan(loan_id: int):
        loan = db.get_or_404(Loan, loan_id)
        if loan.status != "active":
            flash("Only active loans can be returned.", "warning")
        else:
            loan.status = "returned"
            loan.returned_at = datetime.now(UTC)
            loan.book.available_copies += 1
            db.session.commit()
            flash("Return recorded.", "success")
        return redirect(url_for("manage_loans"))


def populate_book_from_form(book: Book) -> bool:
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    isbn = request.form.get("isbn", "").strip()
    category = request.form.get("category", "").strip()
    description = request.form.get("description", "").strip()
    try:
        total_copies = int(request.form.get("total_copies", "1"))
        available_copies = int(request.form.get("available_copies", str(total_copies)))
    except ValueError:
        flash("Copies must be valid numbers.", "danger")
        return False

    if not title or not author or not isbn or not category:
        flash("Title, author, ISBN, and category are required.", "danger")
        return False
    if total_copies < 0 or available_copies < 0 or available_copies > total_copies:
        flash("Copy counts are invalid.", "danger")
        return False

    existing = Book.query.filter(Book.isbn == isbn, Book.id != (book.id or 0)).first()
    if existing:
        flash("ISBN is already used by another book.", "danger")
        return False

    book.title = title
    book.author = author
    book.isbn = isbn
    book.category = category
    book.description = description
    book.total_copies = total_copies
    book.available_copies = available_copies
    return True


def send_overdue_alerts() -> int:
    overdue_loans = (
        Loan.query.filter_by(status="active", overdue_notified_at=None)
        .filter(Loan.due_date < date.today())
        .all()
    )
    sent = 0
    for loan in overdue_loans:
        send_email(
            to_email=loan.student.email,
            subject=f"Overdue library book: {loan.book.title}",
            body=(
                f"Hello {loan.student.name},\n\n"
                f"Your loan for '{loan.book.title}' was due on {loan.due_date}. "
                "Please return it to the library as soon as possible.\n"
            ),
        )
        loan.overdue_notified_at = datetime.now(UTC)
        sent += 1
    db.session.commit()
    return sent


def send_email(to_email: str, subject: str, body: str) -> None:
    host = os.environ.get("SMTP_HOST")
    username = os.environ.get("SMTP_USERNAME")
    password = os.environ.get("SMTP_PASSWORD")
    from_email = os.environ.get("SMTP_FROM", username or "library@example.com")
    port = int(os.environ.get("SMTP_PORT", "587"))

    if not host:
        print(f"[email skipped] To: {to_email} | Subject: {subject}")
        return

    message = EmailMessage()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(host, port) as smtp:
        smtp.starttls()
        if username and password:
            smtp.login(username, password)
        smtp.send_message(message)


app = create_app()


if __name__ == "__main__":
    init_db(app)
    app.run(debug=True)
