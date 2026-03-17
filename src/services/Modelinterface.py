from abc import ABC,abstractmethod
from fastapi import Request

class Model_interface(ABC):

    @abstractmethod
    def preprocess(self):
        pass
    @abstractmethod
    def predict(self,data,request:Request):
        pass