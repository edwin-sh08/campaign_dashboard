from sqlmodel import SQLModel, Field
from typing import Optional

class Campaign(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    status: str
    budget: float

class CampaignCreate(SQLModel):
    name: str
    status: str
    budget: float
