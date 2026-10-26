from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from .database import Base

class ClientRequest(Base):
    __tablename__ = "client_requests"
    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(150), nullable=False)
    client_email = Column(String(255), nullable=False)
    business_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(30), default="pending", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    project = relationship("WebsiteProject", back_populates="request", uselist=False)

class WebsiteProject(Base):
    __tablename__ = "website_projects"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("client_requests.id"), nullable=False, unique=True)
    name = Column(String(200), nullable=False)
    status = Column(String(30), default="draft", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    request = relationship("ClientRequest", back_populates="project")
