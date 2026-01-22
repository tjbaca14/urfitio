"""Database models matching actual schema from Alembic migrations."""

from sqlalchemy import JSON, TIMESTAMP, Column, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Get schema from environment variable, default to 'app'
SCHEMA = "app"


class ChatHistory(Base):
    """Chat conversation history for users"""

    __tablename__ = "chat_history"
    __table_args__ = {"schema": SCHEMA}

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    messages = Column(JSON)
    created_date = Column(TIMESTAMP(timezone=True))
    updated_date = Column(TIMESTAMP(timezone=True))


class Feedback(Base):
    """User feedback submissions"""

    __tablename__ = "feedback"
    __table_args__ = {"schema": SCHEMA}

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    feedback = Column(String, index=True)
    category = Column(String)
    created_date = Column(TIMESTAMP(timezone=True))


class Division(Base):
    """NCAA Division entity"""

    __tablename__ = "division"
    __table_args__ = {"schema": SCHEMA}

    id = Column(String, primary_key=True, index=True)
    division_type = Column(String, nullable=False)

    # Relationships
    schools = relationship(
        "School", back_populates="division", cascade="all, delete-orphan"
    )


class School(Base):
    """School entity with division relationship"""

    __tablename__ = "school"
    __table_args__ = {"schema": SCHEMA}

    id = Column(String, primary_key=True)
    division_id = Column(
        String, ForeignKey(f"{SCHEMA}.division.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String, nullable=False)
    context = Column(String)
    created_date = Column(TIMESTAMP(timezone=True))

    # Relationships
    division = relationship("Division", back_populates="schools")
