"""Database models matching actual schema from Alembic migrations.

NOTE: Division and School models have been moved to app.ncaa.db_models
to reflect their ownership by the NCAA domain.
"""

from sqlalchemy import JSON, TIMESTAMP, Column, String
from sqlalchemy.ext.declarative import declarative_base

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
