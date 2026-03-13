from enum import Enum
from helpers import get_settings
class ResponseSignal(Enum):
    validation_object=get_settings()
    IMAGE_TYPE_NOT_SUPPORTED=f"image type not supported it must be (png,jpg,jpeg)"
    IMAGE_SIZE_EXCEEDED=f"image size exceeded size must be less than {validation_object.IMAGE_SIZE} mb"
    IMAGE_RESOLUTION_ERROR=f"image resolution must be ({validation_object.IMAGE_DIMENSION[0]} x {validation_object.IMAGE_DIMENSION[1]})"
    IMAGE_VALIDATION_SUCCESSFULLY="image uploaded successfully"