from .Modelinterface import Model_interface
import cv2
import numpy as np
from fastapi import Request
from helpers.config import get_settings
import io
from PIL import Image
class DeepEyeClassifier(Model_interface):
    def __init__(self,content):
        self.content=content
        self.settings=get_settings()

    async def retina(self):
        image =  np.array(Image.open(io.BytesIO(self.content)))
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        coords = np.column_stack(np.where(thresh > 0))
        if coords.size == 0:
            return self.content
        y_min, x_min = coords.min(axis=0)
        y_max, x_max = coords.max(axis=0)
        cropped_image = img_rgb[y_min:y_max, x_min:x_max]
        return cropped_image
    
    async def resize_image(self,image):
        img=cv2.resize(image,(300,300))
        return img
    
    async def ben_graham(self,image):
         blur = cv2.GaussianBlur(image,(0,0),30)
         result = cv2.addWeighted(image,4,blur,-4,128)
         return result
    
    async def apply_clahe(self,image):
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        l,a,b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
        l = clahe.apply(l)
        merged = cv2.merge((l,a,b))
        img = cv2.cvtColor(merged, cv2.COLOR_LAB2RGB)
        return img
    
    async def normalize_image(self,image):
        img=image/255.0
        return img
    
    async def preprocess(self):
        img=await self.retina()
        img=await self.resize_image(img)
        img=await self.ben_graham(img)
        img=await self.apply_clahe(img)
        img=await self.normalize_image(img)
        img= np.expand_dims(img, axis=0)# add batch dim to the image
        return img
    
    async def predict(self,data,request:Request):
        binary_class_prob=request.app.deep_eye_classifier.predict(data)
        class_index=int(np.argmax(binary_class_prob))
        classes=self.settings.EYE_CLASS_LIST
        class_predict=classes[class_index]
        confidence=float(np.max(binary_class_prob))
        if class_predict=="Diabetic Retinopathy":
            all_classes_prob=request.app.deep_eye_diseases(data)
            class_index=int(np.argmax(all_classes_prob))
            classes=self.settings.EYE_DISEASES_CLASS_LIST
            class_predict=classes[class_index]
            confidence=float(np.max(all_classes_prob))
        return class_predict,confidence