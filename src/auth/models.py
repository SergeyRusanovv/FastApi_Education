from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    MetaData,
    Integer,
    TIMESTAMP,
    String,
    ForeignKey,
    Column,
    JSON,
    Boolean,
)
from sqlalchemy.orm import relationship

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Role(Base):
    """Таблица ролей"""

    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    permissions = Column(JSON)
    users = relationship("User", back_populates="role")


class User(Base):
    """Таблица пользователей"""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey(Role.id), nullable=False)
    role = relationship(Role, back_populates="user")
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
