from .BaseDataModel import BaseDataModel
from ..db_schemas.eye_db_schemas import User_Feature
import uuid
from sqlalchemy import select
from core.logging import get_logger

logger=get_logger(__name__)
class UserFeatureModel(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client)
    async def get_user_feature(self,session_id:uuid):
        logger.info(f"get user feature started  | session_id={session_id}")
        try:
            async with self.db_client() as session:
                query=select(User_Feature).where(User_Feature.Feature_Session_id==session_id)
                result= await session.execute(query)
       
                logger.info(f"user feature fetched | session_id={session_id}")
                return result.scalars().first()
        except Exception:
            logger.error(
            f"get user feature failed | session_id={session_id}",
            exc_info=True
        )
            raise 
        
    async def insert_user_feature(self,session_id:uuid,user_feature:dict):
        logger.info(f"insert user feature started | session_id={session_id}")
        try:
            async with self.db_client() as session:
                async with session.begin():
                    new_feature=User_Feature(Feature_Session_id=session_id,
                    User_Feature=user_feature)
                    session.add(new_feature)
                    await session.flush()

                logger.info(f"user feature inserted successfully  | session_id={session_id}")
                return new_feature
        except Exception:
            logger.error(
            f"insert user feature failed | session_id={session_id}",
            exc_info=True
        )
            raise