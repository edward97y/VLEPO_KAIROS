from .BaseControllers import BaseControllers
from routes.schemas import eye_feature
from models import ResponseSignal
from core.logging import get_logger

logger=get_logger(__name__)
class FeatureValidation(BaseControllers):
    def __init__(self):
        super().__init__()
    async def feature_validation(self,feature:eye_feature):
        logger.info(f"Feature validation Started | age={feature.age}")

        if feature.age < self.settings.MIN_AGE or feature.age > self.settings.MAX_AGE:
            logger.warning(f"Age validation failed | age={feature.age}")
            return False,ResponseSignal.AGE_RANGE_ERROR.value
        
        if feature.height < self.settings.MIN_HEIGHT_CM or feature.height > self.settings.MAX_HEIGHT_CM :
            logger.warning(f"Height validation failed | height={feature.height}")
            return False,ResponseSignal.HEIGHT_RANGE_ERROR.value
        
        if feature.weight < self.settings.MIN_WEIGHT_KG or feature.weight > self.settings.MAX_WEIGHT_KG :
            logger.warning(f"Weight validation failed | weight={feature.weight}")
            return False,ResponseSignal.WEIGHT_RANGE_ERROR.value
        
        logger.info("feature validation successful")
        return True,ResponseSignal.FEATURE_VALIDATION_SUCCESSFULLY.value