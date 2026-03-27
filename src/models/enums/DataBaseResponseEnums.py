from enum import Enum

class DataBaseResponseEnums(Enum):
    USER_ADD_ERROR="error while adding the user this user name exist "
    USER_ADD_SUCCESSFULLY="user added successfully"
    USER_INFO_ERROR="user does not exist you must sign in"
    GET_USER_INFO_SUCCESSFULLY="success"
    NO_SESSION_FOUND_FOR_THIS_USER="no session found for this user"
    GET_USER_SESSIONS_SUCCESSFULLY="get user session successfully"
    ERROR_WHILE_DELETING_USER="error while deleting user (username doesn't exist)"
    USER_DELETED_SUCCESSFULLY="user deleted successfully"
    USER_DID_NOT_HAVE_INFO="user didn't have any information"
    