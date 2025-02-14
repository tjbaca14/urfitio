from sqlalchemy import JSON, TIMESTAMP, Boolean, Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Feedback(Base):
    __tablename__ = "feedback"
    __table_args__ = {"schema": "app"}

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    feedback = Column(String, index=True)
    category = Column(String)
    created_date = Column(TIMESTAMP(timezone=True))


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "priv"}

    user_id = Column(String)
    username = Column(String, primary_key=True, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=True)
    tos = Column(Boolean, nullable=False)
    is_verified = Column(Boolean, nullable=False)
    created_date = Column(TIMESTAMP(timezone=True))
    updated_date = Column(TIMESTAMP(timezone=True), nullable=True)


class UserVerify(Base):
    __tablename__ = "user_verify"
    __table_args__ = {"schema": "priv"}

    username = Column(String, primary_key=True, index=True)
    token = Column(String, nullable=False)
    expires_at = Column(TIMESTAMP(timezone=True))


class UserProfile(Base):
    __tablename__ = "user_profile"
    __table_args__ = {"schema": "priv"}

    user_id = Column(String, primary_key=True, index=True)
    persona = Column(String)
    meta = Column(JSON)
    created_date = Column(TIMESTAMP(timezone=True))


class CoachIndex(Base):
    __tablename__ = "coach_index"
    __table_args__ = {"schema": "app"}

    coach_id = Column(String, primary_key=True, index=True)
    division = Column(String)
    data = Column(JSON)


class ChatHistory(Base):
    __tablename__ = "chat_history"
    __table_args__ = {"schema": "app"}

    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    messages = Column(JSON)
    created_date = Column(TIMESTAMP(timezone=True))
    updated_date = Column(TIMESTAMP(timezone=True), nullable=True)
