from enum import Enum
from helpers import get_settings
class ResponseSignal(Enum):
    validation_object=get_settings()
    # eye image enums
    IMAGE_TYPE_NOT_SUPPORTED=f"image type not supported it must be (png,jpg,jpeg)"
    IMAGE_SIZE_EXCEEDED=f"image size exceeded size must be less than {validation_object.EYE_IMAGE_SIZE} mb"
    IMAGE_RESOLUTION_ERROR=f"image resolution must be ({validation_object.EYE_IMAGE_DIMENSION[0]} x {validation_object.EYE_IMAGE_DIMENSION[1]})"
    IMAGE_VALIDATION_SUCCESSFULLY="image validation successfully"
    IMAGE_PREPROCESS_ERROR="error while preprocess the image"
    IMAGE_PREDICT_ERROR="error while predicting the image"
    IMAGE_PREDICT_SUCCESSFULLY="image predict successfully"

    #eye Feature enums
    AGE_RANGE_ERROR=f"age must be between {validation_object.MIN_AGE} and {validation_object.MAX_AGE} "
    HEIGHT_RANGE_ERROR=f"height must be between {validation_object.MIN_HEIGHT_CM} cm and {validation_object.MAX_HEIGHT_CM} cm"
    WEIGHT_RANGE_ERROR=f"weight must be between {validation_object.MIN_WEIGHT_KG} Kg and {validation_object.MAX_WEIGHT_KG} Kg"
    FEATURE_VALIDATION_SUCCESSFULLY="feature validation successfully"
    FEATURE_PREDICT_SUCCESSFULLY="eye machine model predict successfully"