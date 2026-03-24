from .eye_base import SqlBaseModel
from sqlalchemy import Column,ForeignKey,Index,DateTime,func,INTEGER
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

class SessionUsage(SqlBaseModel):
    __tablename__="session_usage"
    Usage_id=Column(UUID(as_uuid=True),default=uuid.uuid4,primary_key=True)
    Input_Tokens=Column(INTEGER)
    Output_Tokens=Column(INTEGER)
    Updated_at=Column(DateTime(timezone=True),onupdate=func.now(),nullable=True)
    Usage_Session_id=Column(UUID(as_uuid=True),ForeignKey("sessions.Session_id"),nullable=False,unique=True)
    session = relationship("Session", back_populates="session_usage")
