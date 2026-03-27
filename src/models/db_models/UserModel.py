from ..db_schemas.eye_db_schemas import User
from .BaseDataModel import BaseDataModel
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from uuid import UUID
class UserModel(BaseDataModel):
    def __init__(self,db_client:object):
        super().__init__(db_client=db_client)

    async def is_user_exist(self,full_name):
        query = select(User).where(User.Full_Name == full_name)
        async with self.db_client() as session:
            result = await session.execute(query)
            user = result.scalars().first()
            return user 

    async def add_user_by_fullname(self,full_name:str)->User|None:
        exist=await self.is_user_exist(full_name=full_name)
        if not exist:
            async with self.db_client() as session:
                async with session.begin():
                    user=User(Full_Name=full_name)
                    session.add(user)
                    await session.flush()
                    await session.refresh(user)
                   
            return user
        return exist
    async def get_user_by_id(self,user_id:UUID)->User:
        async with self.db_client() as session:
            query=select(User).where(User.User_id==user_id)
            result=await session.execute(query)
            return result.scalars().first()
        
    async def get_all_user_sessions(self,user_id:UUID):
        
        async with self.db_client() as session:
            query = select(User).options(selectinload(User.sessions)).where(User.User_id ==user_id)
            result = await session.execute(query)
            user_with_sessions = result.scalars().first() # returns None if not found
        
        return user_with_sessions.sessions if user_with_sessions else []
        
    async def delete_user_by_id(self,user_id:str)->bool:
        async with self.db_client() as session:
            async with session.begin():
                result = await session.execute(select(User).where(User.User_id==user_id))
                user = result.scalars().first()
                if user:
                    await session.delete(user)
                    return True
                return False
            
   