from models import UserModel
from uuid import UUID
class UserService:
    def __init__(self, db_client):
        self.models = UserModel(db_client=db_client)

    async def create_user(self, full_name: str):
        user = await self.models.add_user_by_fullname(full_name=full_name)
        
        
        return user

    async def get_user_info(self, user_id: UUID):
        user_info = await self.models.get_user_by_id(user_id=user_id)
        
        return user_info
      

    async def get_user_sessions(self, user_id: UUID):
        user_sessions = await self.models.get_all_user_sessions(user_id=user_id)
        if not user_sessions:
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
        return sessions_list
    
    async def delete_user_by_id(self, user_id: UUID)->bool:
        delete_user = await self.models.delete_user_by_id(user_id=user_id)
        if not delete_user:
            return False
        return True