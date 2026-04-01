from .eye_base import SqlBaseModel
from sqlalchemy import Column,ForeignKey,Index,DateTime,func,String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

class Images(SqlBaseModel):
    __tablename__="images"
    Image_id=Column(UUID(as_uuid=True),default=uuid.uuid4,primary_key=True)
    Uploaded_at=Column(DateTime(timezone=True),nullable=False,server_default=func.now())
    image_type=Column(String,nullable=False)
    image_path=Column(String,nullable=False)
    grad_cam_image_path=Column(String,nullable=True)
    

    Image_Session_id=Column(UUID(as_uuid=True),ForeignKey("sessions.Session_id"),nullable=False)
    
    session=relationship("Session",back_populates="images")

    __table_args__=(
        Index("ix_Image_Session_id",Image_Session_id),
    )