from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class ClientRequestCreate(BaseModel):
    client_name: str = Field(min_length=1, max_length=150)
    client_email: str = Field(min_length=3, max_length=255)
    business_name: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=10, max_length=10000)

class ClientRequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    client_name: str
    client_email: str
    business_name: str
    description: str
    status: str
    created_at: datetime

class ProjectCreate(BaseModel):
    project_name: str = Field(min_length=1, max_length=200)

class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    request_id: int
    name: str
    status: str
    created_at: datetime
