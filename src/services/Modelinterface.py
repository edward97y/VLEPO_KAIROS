from abc import ABC,abstractmethod
from fastapi import Request

class Model_interface(ABC):

    @abstractmethod
    async def preprocess(self):
        pass
    @abstractmethod
    async def predict(self,data,request:Request):
        pass