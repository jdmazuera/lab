from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func


# Database models
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    email = Column(String(100), unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Ticket(Base):
    __tablename__ = "ticket"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, index=True)
    customer_id = Column(String(50), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    channel = Column(String(50))
    subject = Column(String(100))
    description = Column(Text)
    status = Column(String(50))
    priority = Column(String(50))
    short_description = Column(String(141))
    is_urgent = Column(Boolean)
    agent = Column(String(200))
