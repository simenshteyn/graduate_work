from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, condecimal
from sqlmodel import SQLModel, Field


class Payments(SQLModel, table=True):
    """ Class for creation of payments database via SQLModel. """
    payment_id: UUID = Field(primary_key=True, index=True, nullable=False)
    payment_attempts: int | None = Field(default=0, nullable=False)
    is_active: bool | None = Field(default=True, nullable=False)
    is_paid: bool | None = Field(default=False, nullable=False)
    created_at: datetime | None = Field(default=datetime.now(), nullable=False)
