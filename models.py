from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from typing import List, Optional
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import String, Integer, DateTime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column("user_id", Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(120), unique=True, nullable=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    role: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[Optional[DateTime]] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[Optional[DateTime]] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


    def set_password(self, password: str) -> None:
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check the hashed password."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User: {self.username}>"
