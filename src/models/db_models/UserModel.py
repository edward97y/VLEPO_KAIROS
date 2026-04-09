from ..db_schemas.eye_db_schemas import User
from .BaseDataModel import BaseDataModel
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from uuid import UUID
from core.logging import get_logger

logger=get_logger(__name__)
class UserModel(BaseDataModel):
    def __init__(self,db_client:object):
        super().__init__(db_client=db_client)

    async def is_user_exist(self,full_name):
        logger.info(f"Checking user existence | full_name={full_name}")
        try:
            query = select(User).where(User.Full_Name == full_name)
            async with self.db_client() as session:
                result = await session.execute(query)
                user = result.scalars().first()
                if user:
                     logger.info(f"User exists | full_name={full_name} | user_id={user.User_id}")
                else:
                     logger.info(f"User not found | full_name={full_name}")

                return user 
            
        except Exception:
            logger.error(
            f"Failed to check user existence | full_name={full_name} ",
            exc_info=True
        )
        raise
    async def add_user_by_fullname(self,full_name:str)->User|None:

        logger.info(f"Add user requested | full_name={full_name}")
        try:
            exist=await self.is_user_exist(full_name=full_name)

            if not exist:
                async with self.db_client() as session:
                    async with session.begin():
                        user=User(Full_Name=full_name)
                        session.add(user)
                        await session.flush()
                        await session.refresh(user)
                logger.info(f"User created | full_name={full_name} | user_id={user.User_id}")    
                return user
            logger.info(f"User already exists | full_name={full_name} | user_id={exist.User_id}")

            return exist
        except Exception:
            logger.error(
            f"Failed to create user | full_name={full_name}",
            exc_info=True
        )
            raise
    async def get_user_by_id(self,user_id:UUID)->User:
        logger.info(f"Fetching user by id | user_id={user_id}")
        try:
            async with self.db_client() as session:
                query=select(User).where(User.User_id==user_id)
                result=await session.execute(query)
                user= result.scalars().first()
            if user:
                 logger.info(f"User found | user_id={user_id}")
            else:
                 logger.info(f"User not found | user_id={user_id}")
            return user
        except Exception:
            logger.error(
            f"Failed to fetch user | user_id={user_id}",
            exc_info=True
        )
            raise
        
    async def get_all_user_sessions(self,user_id:UUID):
        logger.info(f"Fetching user sessions | user_id={user_id}")
        try:
            async with self.db_client() as session:
                query = select(User).options(selectinload(User.sessions)).where(User.User_id ==user_id)
                result = await session.execute(query)
                user_with_sessions = result.scalars().first() # returns None if not found

            session_count = len(user_with_sessions.sessions) if user_with_sessions else 0
            logger.info(f"Sessions fetched | user_id={user_id} | count={session_count}")
            return user_with_sessions.sessions if user_with_sessions else []
        except Exception:
            logger.error(
                f"Failed to fetch user sessions | user_id={user_id}",
                exc_info=True)
            raise   
    async def delete_user_by_id(self,user_id:str)->bool:
        logger.info(f"Deleting user | user_id={user_id}")
        try:
            async with self.db_client() as session:
                async with session.begin():
                    result = await session.execute(select(User).where(User.User_id==user_id))
                    user = result.scalars().first()
                    if user:
                        await session.delete(user)
                        logger.info(f"User deleted successfully | user_id={user_id}")
                        return True
                    logger.info(f"User not found for deletion | user_id={user_id}")
                    return False
        except Exception:
            logger.error(
            f"Failed to delete user | user_id={user_id}",
            exc_info=True
        )
            raise
            
   