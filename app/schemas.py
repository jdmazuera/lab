from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: Optional[str] = None
    
    class Config:
        from_attributes = True

class Ticket(BaseModel):
    ticket_id: int
    customer_id: str
    created_at: datetime
    channel: str
    subject: str
    description: str
    status: str
    priority: str
    agent: str
    