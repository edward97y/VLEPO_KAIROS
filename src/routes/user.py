from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from .schemas import UserNameSchema
from services import UserService
from models import DataBaseResponseEnums
from uuid import UUID
user_router = APIRouter(prefix="/api/user",tags=["user"])

@user_router.post("/create_user/")
async def create_user(user_name: UserNameSchema, request: Request):
    service = UserService(db_client=request.app.db_client)
    user = await service.create_user(full_name=user_name.full_name)
    if not user:
     return JSONResponse(content={"success": False, "signal": DataBaseResponseEnums.USER_ADD_ERROR.value}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse(content={"success": True, "signal": DataBaseResponseEnums.USER_ADD_SUCCESSFULLY.value, "user_name": user.Full_Name,"user_id":str(user.User_id),"created__at":str(user.Created_at)})


@user_router.get("/get_user_info/{user_id}")
async def get_user_info(user_id:UUID, request: Request):
    service = UserService(db_client=request.app.db_client)
    user_info = await service.get_user_info(user_id=user_id)
    if not user_info:
            return JSONResponse(content={"success": False, "signal": DataBaseResponseEnums.USER_INFO_ERROR.value},status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse(content={
            "success": True,
            "signal": DataBaseResponseEnums.GET_USER_INFO_SUCCESSFULLY.value,
            "user_info": {
                "user_id": str(user_info.User_id),
                "user_name": user_info.Full_Name,
                "created_at": str(user_info.Created_at)
            }
            },status_code=status.HTTP_200_OK)
    

@user_router.get("/get_user_sessions/{user_id}")
async def get_user_sessions(user_id:UUID, request: Request):
    service = UserService(db_client=request.app.db_client)
    user_sessions = await service.get_user_sessions(user_id=user_id)
    if not user_sessions:
            return JSONResponse(content={"success": False, "signal": DataBaseResponseEnums.NO_SESSION_FOUND_FOR_THIS_USER.value},status_code=status.HTTP_400_BAD_REQUEST)
    
    return JSONResponse(content={"success": True, "signal": DataBaseResponseEnums.GET_USER_SESSIONS_SUCCESSFULLY.value, "sessions": user_sessions,"user_id":str(user_id)},status_code=status.HTTP_200_OK)


@user_router.delete("/delete_user_by_id/{user_id}")
async def delete_user_by_id(user_id:UUID, request: Request):
    service = UserService(db_client=request.app.db_client)
    result = await service.delete_user_by_id(user_id=user_id)
    if not result:
            return JSONResponse(content={"success": False, "signal": DataBaseResponseEnums.ERROR_WHILE_DELETING_USER.value},status_code=status.HTTP_400_BAD_REQUEST)
    
    return JSONResponse(content={"success": True, "signal": DataBaseResponseEnums.USER_DELETED_SUCCESSFULLY.value},status_code=status.HTTP_200_OK)
