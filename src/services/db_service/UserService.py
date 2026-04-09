from models import UserModel
from uuid import UUID
from core.logging import get_logger

logger=get_logger(__name__)
class UserService:
    def __init__(self, db_client):
        self.models = UserModel(db_client=db_client)

    async def create_user(self, full_name: str):
        logger.info(f"create user request | full_name={full_name}")
        try:
            user = await self.models.add_user_by_fullname(full_name=full_name)

            logger.info(f"create user complete | full_name={full_name}")
            return user
        except Exception:
            logger.error(f"creating user failed| full_name={full_name}",exc_info=True)
            raise


    async def get_user_info(self, user_id: UUID):
        logger.info(f"get user request | user_id={user_id}")
        try:
            user_info = await self.models.get_user_by_id(user_id=user_id)
            logger.info(f"get user complete | user_id={user_id}")
            return user_info
        except Exception:
            logger.error(f"get user failed | user_id={user_id}",exc_info=True)
            raise
      

    async def get_user_sessions(self, user_id: UUID):
        logger.info(f"get user sessions request| user_id={user_id}")
        try:
            user_sessions = await self.models.get_all_user_sessions(user_id=user_id)
            if not user_sessions:

                logger.info(f"user doesn't have any sessions | user_id={user_id}")
                return user_sessions

            sessions_list = [
                {
                    "session_id": str(s.Session_id),
                    "created_at": s.Created_at.isoformat() if s.Created_at else None,
                    "end_at": s.End_at.isoformat() if s.End_at else None,
                    "chat_summary": str(s.Chat_Summary),
                }
                for s in user_sessions
            ]
            logger.info(f"get user session complete||count={len(user_sessions)} | user_id={user_id}")
            return sessions_list
        except Exception:
                logger.error(f"get user session failed| user_id={user_id}",exc_info=True)
                raise
    
    async def delete_user_by_id(self, user_id: UUID)->bool:
        logger.info(f"delete user request | user_id={user_id}")
        try:
            delete_user = await self.models.delete_user_by_id(user_id=user_id)
            if not delete_user:
                logger.info(f"no user found to delete | user_id={user_id}")
                return False
            
            logger.info(f"user deleted complete | user_id={user_id}")
            return True
        except Exception:
            logger.error(f"delete user failed| user_id={user_id}",exc_info=True)
            raise