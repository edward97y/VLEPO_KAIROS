from .BaseControllers import BaseControllers
from routes.schemas import eye_feature
from models import ResponseSignal
class FeatureValidation(BaseControllers):
    def __init__(self):
        super().__init__()
    async def feature_validation(self,feature:eye_feature):

        if feature.age < self.settings.MIN_AGE or feature.age > self.settings.MAX_AGE:
            return False,ResponseSignal.AGE_RANGE_ERROR.value
        
        if feature.height < self.settings.MIN_HEIGHT_CM or feature.height > self.settings.MAX_HEIGHT_CM :
            return False,ResponseSignal.HEIGHT_RANGE_ERROR.value
        
        if feature.weight < self.settings.MIN_WEIGHT_KG or feature.weight > self.settings.MAX_WEIGHT_KG :
            return False,ResponseSignal.WEIGHT_RANGE_ERROR.value
        
        return True,ResponseSignal.FEATURE_VALIDATION_SUCCESSFULLY.value