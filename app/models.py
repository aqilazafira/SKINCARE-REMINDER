from typing import Optional, List
from flask_login import UserMixin
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from . import db

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(120), unique=True, nullable=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    role: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    created_at: Mapped[Optional[DateTime]] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[Optional[DateTime]] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    reminders: Mapped[List["Reminder"]] = relationship(back_populates="user")
    feedbacks: Mapped[List["Feedback"]] = relationship(back_populates="user")
    timelines: Mapped[List["Timeline"]] = relationship(back_populates="user")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User: {self.username}>"

class Reminder(db.Model):
    __tablename__ = "reminders"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    day: Mapped[int] = mapped_column(Integer, nullable=False)
    hour: Mapped[int] = mapped_column(Integer, nullable=False)
    minute: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="reminders")

    def __repr__(self):
        return f"<Reminder: {self.content[:20]}>"

class Feedback(db.Model):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="feedbacks")

    def __repr__(self):
        return f"<Feedback: {self.content[:20]}>"

class Timeline(db.Model):
    __tablename__ = "timelines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=False)
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="timelines")

    def __repr__(self):
        return f"<Timeline: {self.image_url}>"

class Product(db.Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    brand: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recommendation_id: Mapped[int] = mapped_column(ForeignKey("recommendations.id"), nullable=True)
    type_id: Mapped[int] = mapped_column(ForeignKey("skincare_types.id"), nullable=False)

    recommendation: Mapped["Recommendation"] = relationship(back_populates="products")
    skincare_type: Mapped["SkincareType"] = relationship(back_populates="products")

    def __repr__(self):
        return f"<Product: {self.name}>"

class Recommendation(db.Model):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)

    products: Mapped[List["Product"]] = relationship(back_populates="recommendation")

    def __repr__(self):
        return f"<Recommendation: {self.title}>"

class SkincareType(db.Model):
    __tablename__ = "skincare_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)

    products: Mapped[List["Product"]] = relationship(back_populates="skincare_type")

    def __repr__(self):
        return f"<SkincareType: {self.title}>"
