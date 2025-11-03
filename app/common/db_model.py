from sqlalchemy import (JSON, TIMESTAMP, Boolean, Column, ForeignKey, String,
                        UniqueConstraint)
from sqlalchemy.ext.declarative import declarative_base

# from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """
    User entity - core authentication and user data.
    Note: Currently uses username (email) as PK for compatibility.
    Consider migrating to user_id as PK in future refactor.
    """

    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("user_id", name="uq_user_id"),)

    user_id = Column(String, nullable=False, unique=True, index=True)
    username = Column(String, primary_key=True, index=True)  # Email address
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=True)
    tos = Column(Boolean, nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    created_date = Column(TIMESTAMP(timezone=True), nullable=False)
    updated_date = Column(TIMESTAMP(timezone=True), nullable=True)

    # Relationships
    # profile = relationship(
    #     "UserProfile",
    #     back_populates="user",
    #     uselist=False,
    #     cascade="all, delete-orphan",
    # )
    # verify_tokens = relationship(
    #     "UserVerify", back_populates="user", cascade="all, delete-orphan"
    # )
    # chats = relationship(
    #     "ChatHistory", back_populates="user", cascade="all, delete-orphan"
    # )
    # feedback = relationship(
    #     "Feedback", back_populates="user", cascade="all, delete-orphan"
    # )


class UserProfile(Base):
    """User profile with persona and metadata"""

    __tablename__ = "user_profile"

    user_id = Column(
        String,
        # ForeignKey("priv.users.user_id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    persona = Column(String, nullable=False)
    meta = Column(JSON, nullable=False, default={})
    created_date = Column(TIMESTAMP(timezone=True), nullable=False)

    # Relationships
    # user = relationship("User", back_populates="profile")


class UserVerify(Base):
    """Email verification tokens for user accounts"""

    __tablename__ = "user_verify"

    username = Column(
        String,
        # ForeignKey("priv.users.username", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    token = Column(String, nullable=False)
    expires_at = Column(TIMESTAMP(timezone=True), nullable=False)

    # Relationships
    # user = relationship("User", back_populates="verify_tokens")


class ChatHistory(Base):
    """Chat conversation history for users"""

    __tablename__ = "chat_history"

    id = Column(String, primary_key=True)
    user_id = Column(
        String,
        # ForeignKey("priv.users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    messages = Column(JSON, nullable=False, default=[])
    created_date = Column(TIMESTAMP(timezone=True), nullable=False)
    updated_date = Column(TIMESTAMP(timezone=True), nullable=True)

    # Relationships
    # user = relationship("User", back_populates="chats")


class Feedback(Base):
    """User feedback submissions"""

    __tablename__ = "feedback"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(
        String,
        # ForeignKey("priv.users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    feedback = Column(String, nullable=False)
    category = Column(String, nullable=True)
    created_date = Column(TIMESTAMP(timezone=True), nullable=False)

    # Relationships
    # user = relationship("User", back_populates="feedback")


class CoachIndex(Base):
    """Coach index data - standalone entity without user relationship"""

    __tablename__ = "coach_index"

    coach_id = Column(String, primary_key=True, index=True)
    division = Column(String, nullable=True)
    data = Column(JSON, nullable=False, default={})


class Division(Base):
    """NCAA Division entity"""

    __tablename__ = "division"

    id = Column(String, primary_key=True, index=True)
    division_type = Column(String, nullable=False)


class School(Base):
    """School entity with division relationship"""

    __tablename__ = "school"

    id = Column(String, primary_key=True)
    division_id = Column(
        String, ForeignKey("division.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String, nullable=False)
    created_date = Column(TIMESTAMP(timezone=True))


class Coach(Base):
    """Coach entity with school relationship"""

    __tablename__ = "coach"

    id = Column(String, primary_key=True)
    school_id = Column(
        String, ForeignKey("school.id", ondelete="CASCADE"), nullable=False
    )
    context = Column(String, nullable=False)
    created_date = Column(TIMESTAMP(timezone=True))
