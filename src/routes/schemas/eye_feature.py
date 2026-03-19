from pydantic import BaseModel
from typing import Literal

class EyeFeatureSchema(BaseModel):
    age:int
    insulin:Literal[0,1]
    dm_time:float
    smoking:Literal[0,1]
    alcohol_consumption:Literal[0,1]
    oraltreatment_dm:Literal[0,1]
    systemic_hypertension:Literal[0,1]
    vascular_disease:Literal[0,1]
    acute_myocardial_infarction:Literal[0,1]
    weight:int
    height:int
    nephropathy:Literal[0,1]
    neuropathy:Literal[0,1]
    diabetic_foot:Literal[0,1]
