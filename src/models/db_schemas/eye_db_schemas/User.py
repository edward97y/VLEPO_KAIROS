from .eye_base import SqlBaseModel
from sqlalchemy import Column,DateTime,func,String,Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
class User(SqlBaseModel):
    __tablename__="users"
    User_id=Column(UUID(as_uuid=True),default=uuid.uuid4,primary_key=True)
    Full_Name=Column(String,unique=True,nullable=False)
    Created_at=Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    sessions = relationship("Session", back_populates="user")


   
    