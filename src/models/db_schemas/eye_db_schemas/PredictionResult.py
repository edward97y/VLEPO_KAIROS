from .eye_base import SqlBaseModel
from sqlalchemy import Column,ForeignKey,Index,DateTime,func,FLOAT,String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

class PredictionResult(SqlBaseModel):
    __tablename__="prediction_result"
    Prediction_id=Column(UUID(as_uuid=True),default=uuid.uuid4,primary_key=True)
    model_name=Column(String,nullable=False)
    prediction_value=Column(String,nullable=False)
    model_version=Column(String,nullable=False)
    confidence_score=Column(FLOAT,nullable=False)
    Updated_at=Column(DateTime(timezone=True),onupdate=func.now(),nullable=True)
    Prediction_Session_id=Column(UUID(as_uuid=True),ForeignKey("sessions.Session_id"),nullable=False)
    Prediction_Image_id = Column(UUID(as_uuid=True), ForeignKey("images.Image_id"))
    session = relationship("Session", back_populates="prediction_result")

    __table_args__=(
        Index("ix_Prediction_Session_id",Prediction_Session_id),
        Index("ix_Prediction_Image_id",Prediction_Image_id)
        )

