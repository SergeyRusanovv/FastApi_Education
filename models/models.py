from datetime import datetime

from sqlalchemy import (
    MetaData, Integer, TIMESTAMP, String,
    ForeignKey, Column, JSON, Table
)
from sqlalchemy.orm import declarative_base


metadata = MetaData()


roles = Table(
    "roles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(255), nullable=False),
    Column("permissions", JSON)
)


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(255), nullable=False),
    Column("username", String(255), nullable=False),
    Column("password", String(255), nullable=False),
    Column("role_id", Integer, ForeignKey("roles.id"), nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow)
)

# class Users(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     email = Column(String, nullable=False, unique=True)
#     username = Column(String, nullable=False)
#     password = Column(String, nullable=False)
#     registered_at = Column(TIMESTAMP, default=datetime.utcnow)
#     role_id = Column(Integer, ForeignKey("roles.id"))
