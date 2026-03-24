from .eye_base import SqlBaseModel
from sqlalchemy import Column,String,DateTime,ForeignKey,Index,func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

class Session(SqlBaseModel):
    __tablename__="sessions"
    Session_id=Column(UUID(as_uuid=True),default=uuid.uuid4,primary_key=True)
    Created_at=Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    End_at=Column(DateTime(timezone=True),nullable=True)
    Chat_Summary=Column(String,nullable=True)

    Session_User_id=Column(UUID(as_uuid=True),ForeignKey("users.User_id"),nullable=False)

    user = relationship("User", back_populates="sessions")
    images = relationship("Images", back_populates="session")
    user_features = relationship("User_Feature", back_populates="session")
    prediction_result = relationship("PredictionResult", back_populates="session")
    session_usage = relationship("SessionUsage", back_populates="session", uselist=False)


    
    __table_args__=(
        Index("ix_Session_User_id",Session_User_id),
    )