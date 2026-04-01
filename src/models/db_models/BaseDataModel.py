from helpers.config import get_settings
import os
import random
import string
import cv2
class BaseDataModel:
    def __init__(self,db_client:object):
        self.db_client=db_client
        self.settings=get_settings()

        self.base_dir=os.path.dirname(os.path.dirname(__file__))
        file="assets/files"
        self.files_dir=os.path.join(self.base_dir,file)
        
        
    def generate_image_path(self,length:int=12):
        
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    def get_image_path(self):
        file_path=self.generate_image_path()+".jpg"
        database_path=os.path.join(self.files_dir,file_path)

        if not os.path.exists(self.files_dir):
            os.makedirs(self.files_dir)
        return database_path
    def save_image(self, image, path):
        cv2.imwrite(path, image)
    
        return path
