from .eye_base import SqlBaseModel
from sqlalchemy import Column,ForeignKey,Index
from sqlalchemy.dialects.postgresql import UUID,JSONB
from sqlalchemy.orm import relationship
import uuid

class User_Feature(SqlBaseModel):
    __tablename__="user_features"
    Feature_id=Column(UUID(as_uuid=True),default=uuid.uuid4,primary_key=True)
    User_Feature=Column(JSONB,nullable=False)
    Feature_Session_id=Column(UUID(as_uuid=True),ForeignKey("sessions.Session_id"),nullable=False)
    
    session=relationship("Session",back_populates="user_features")

    __table_args__=(
        Index("ix_Feature_Session_id",Feature_Session_id),
    )