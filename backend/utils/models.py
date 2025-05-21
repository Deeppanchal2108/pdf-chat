import uuid
from db import Base
from sqlalchemy import TIMESTAMP, Column, String, Boolean, Float, ForeignKey, Text
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now(datetime.UTC))
    updated_at = Column(TIMESTAMP, default=datetime.now(datetime.UTC), onupdate=datetime.now(datetime.UTC))

    # Relationships
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="user", cascade="all, delete-orphan")
    files = relationship("File", back_populates="user", cascade="all, delete-orphan")
    embeddings = relationship("Embedding", back_populates="user", cascade="all, delete-orphan")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id"), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.now(datetime.UTC))
    updated_at = Column(TIMESTAMP, default=datetime.now(datetime.UTC), onupdate=datetime.now(datetime.UTC))

    # Relationships
    user = relationship("User", back_populates="sessions")
    file = relationship("File", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now(datetime.UTC))
    updated_at = Column(TIMESTAMP, default=datetime.now(datetime.UTC), onupdate=datetime.now(datetime.UTC))

    # Relationships
    user = relationship("User", back_populates="messages")
    session = relationship("Session", back_populates="messages")


class File(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    file_name = Column(String, nullable=False)
    content_type = Column(String)
    file_size = Column(Float)
    created_at = Column(TIMESTAMP, default=datetime.now(datetime.UTC))
    updated_at = Column(TIMESTAMP, default=datetime.now(datetime.UTC), onupdate=datetime.now(datetime.UTC))

    # Relationships
    user = relationship("User", back_populates="files")
    sessions = relationship("Session", back_populates="file", cascade="all, delete-orphan")
    embeddings = relationship("Embedding", back_populates="file", cascade="all, delete-orphan")


class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chunk = Column(Text, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id"), nullable=False)
    embedding = Column(Vector(1536), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now(datetime.UTC))
    updated_at = Column(TIMESTAMP, default=datetime.now(datetime.UTC), onupdate=datetime.now(datetime.UTC))

    # Relationships
    user = relationship("User", back_populates="embeddings")
    file = relationship("File", back_populates="embeddings")
