from .Modelinterface import Model_interface
import cv2
import numpy as np
from fastapi import Request
from helpers.config import get_settings
import io
from PIL import Image
from .db_service import PredictionResultService,ImageService
from uuid import UUID
import tensorflow as tf
from core.logging import get_logger

logger=get_logger(__name__)
class DeepEyeClassifier(Model_interface):
    def __init__(self,content,db_client:object,session_id:UUID):
        self.content=content
        self.session_id=session_id
        self.settings=get_settings()
        self.prediction_service=PredictionResultService(db_client=db_client,session_id=session_id)
        self.image_service=ImageService(db_client=db_client,session_id=session_id)
        
    async def retina(self):
        logger.debug(f"retina extraction started | session_id={self.session_id}")
        image =  np.array(Image.open(io.BytesIO(self.content)))
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        coords = np.column_stack(np.where(thresh > 0))
        if coords.size == 0:
            logger.warning(f"empty retina coords | session_id={self.session_id}")

            return self.content
        y_min, x_min = coords.min(axis=0)
        y_max, x_max = coords.max(axis=0)
        cropped_image = img_rgb[y_min:y_max, x_min:x_max]

        logger.debug(f"retina extraction done | session_id={self.session_id}")

        return cropped_image
    
    async def resize_image(self,image):
        logger.debug(f"resize image | session_id={self.session_id}")
        img=cv2.resize(image,(300,300))
        return img
    
    async def ben_graham(self,image):
         logger.debug(f"ben graham enhancement | session_id={self.session_id}")

         blur = cv2.GaussianBlur(image,(0,0),30)
         result = cv2.addWeighted(image,4,blur,-4,128)
         return result
    
    async def apply_clahe(self,image):
        logger.debug(f"CLAHE applied | session_id={self.session_id}")
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        l,a,b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
        l = clahe.apply(l)
        merged = cv2.merge((l,a,b))
        img = cv2.cvtColor(merged, cv2.COLOR_LAB2RGB)
        return img
    
    async def normalize_image(self,image):
        logger.debug(f"normalization started | session_id={self.session_id}")
        img=image/255.0
        return img
    
    async def preprocess(self):
        logger.info(f"preprocess pipeline started | session_id={self.session_id}")

        img=await self.retina()
        img=await self.resize_image(img)
        img=await self.ben_graham(img)
        img=await self.apply_clahe(img)
        img=await self.normalize_image(img)
        img= np.expand_dims(img, axis=0)# add batch dim to the image

        logger.info(f"image tensor prepared | session_id={self.session_id} | shape={img.shape}")

        
        image_for_save=np.squeeze(img, axis=0) 
        image_for_save=(image_for_save * 255).astype("uint8")
        result=await self.image_service.insert_image_info(image=image_for_save)
        
        logger.info(f"image saved | session_id={self.session_id} | image_id={result.Image_id}")

        return img,result.Image_id
    async def generate_gradcam(self, grad_model, image):


        logger.info(f"Grad-CAM generation started | session_id={self.session_id}")

        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(image)
            predictions=predictions[0]
            class_index = tf.argmax(predictions[0])
            loss = predictions[:, class_index]
    
        grads = tape.gradient(loss, conv_outputs)
    
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        conv_outputs = conv_outputs[0]
    
        heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
    
        heatmap = tf.maximum(heatmap, 0) / tf.reduce_max(heatmap)
    
        logger.info(f"Grad-CAM generated | session_id={self.session_id}")
        return heatmap.numpy()
    async def create_gradcam_image(self, heatmap, image):
        logger.info(f"creating Grad-CAM overlay | session_id={self.session_id}")
    

        image = np.squeeze(image, axis=0)
        image = (image * 255).astype("uint8")

        heatmap = cv2.resize(heatmap, (image.shape[1], image.shape[0]))
        heatmap = np.uint8(255 * heatmap)

        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

        result = cv2.addWeighted(image, 0.6, heatmap, 0.4, 0)

        return result


    async def predict(self,data,image_id:UUID,request:Request):
        logger.info(f"prediction started | session_id={self.session_id} | image_id={image_id}")
        try:
            logger.info("Running binary classifier")
            binary_class_prob=request.app.binary_deep_eye_classifier.predict(data)
            class_index=int(np.argmax(binary_class_prob))
            classes=self.settings.BINARY_DEEP_EYE_CLASSIFIER_CLASS_LIST
            class_predict=classes[class_index]
            confidence=float(np.max(binary_class_prob))
            logger.info(f"Binary prediction done | class={class_index} | confidence={confidence}")


            if class_predict=="Diabetic Retinopathy": 
                logger.info("Switching to multi-class model")
                all_classes_prob=request.app.multi_deep_eye_classifier.predict(data)
                class_index=int(np.argmax(all_classes_prob))
                classes=self.settings.MULTI_DEEP_EYE_CLASSIFIER_CLASS_LIST
                class_predict=classes[class_index]
                confidence=float(np.max(all_classes_prob))
                logger.info(
                    f"multi-class prediction done | class={class_predict} | confidence={confidence}"
                )
                result=await self.prediction_service.insert_deep_model_predict(prediction_value=class_predict,confidence_score=confidence,
                                                                     model_name=self.settings.MULTI_DEEP_EYE_CLASSIFIER_NAME,
                                                                     model_version=self.settings.MULTI_DEEP_EYE_CLASSIFIER_VERSION,
                                                                     image_id=image_id)
                logger.info("Grad-CAM using binary grad model")
                grad_cam=await self.generate_gradcam(grad_model=request.app.binary_grad_model,image=data)
                grad_cam_image=await self.create_gradcam_image(heatmap=grad_cam,image=data)
                im_result=await self.image_service.update_grad_cam(image_id=image_id,grad_cam_image=grad_cam_image)

            else:
                logger.info("final decision from binary model")
                result=await self.prediction_service.insert_deep_model_predict(prediction_value=class_predict,confidence_score=confidence,
                                                                     model_name=self.settings.BINARY_DEEP_EYE_CLASSIFIER_NAME,
                                                                     model_version=self.settings.BINARY_DEEP_EYE_CLASSIFIER_VERSION,
                                                                     image_id=image_id)
                logger.info("Grad-CAM using multi grad model")
                grad_cam=await self.generate_gradcam(grad_model=request.app.multi_grad_model,image=data)
                grad_cam_image=await self.create_gradcam_image(heatmap=grad_cam,image=data)
                im_result=await self.image_service.update_grad_cam(image_id=image_id,grad_cam_image=grad_cam_image) 
            logger.info(
                f"prediction pipeline completed | session_id={self.session_id} | prediction_id={result.Prediction_id}"
            )

            predict_result={"prediction_id":str(result.Prediction_id),"model_name":result.model_name,
                            "prediction_value":result.prediction_value,"model_version":result.model_version,
                            "confidence_score":result.confidence_score,"created_at":str(result.created_at),
                            "prediction_session_id":str(result.Prediction_Session_id),"prediction_image_id":str(result.Prediction_Image_id)}


            image_result={"image_id":str(im_result.Image_id),"uploaded_at":str(im_result.Uploaded_at),
                          "image_type":im_result.image_type,"image_path":im_result.image_path,
                          "grad_cam_image_path":im_result.grad_cam_image_path,"image_session_id":str(im_result.Image_Session_id)}

            logger.info(f"prediction request finished successfully | session_id={self.session_id}")

            return predict_result,image_result
        except Exception:
            logger.error(
        f"deep prediction pipeline failed | session_id={self.session_id}",
        exc_info=True
    )
        raise