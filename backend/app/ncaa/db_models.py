"""NCAA database models - Division and School ORM models."""

from sqlalchemy import TIMESTAMP, Column, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Get schema from environment variable, default to 'app'
SCHEMA = "app"


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
