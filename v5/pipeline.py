import os
import cv2
import time
from main.src.detector import Detector

from main.src.detect_sense import run

import torch
import numpy as np

import logging
from logging.handlers import RotatingFileHandler
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
errorlogHandler = RotatingFileHandler('./logs/pipeline_error.log', maxBytes=1000, backupCount=3)
errorlogHandler.setLevel(logging.ERROR)
errorlogHandler.setFormatter(formatter)
logger.addHandler(errorlogHandler)


class Activity:

    def __init__(self):

        #initializing directory path
        self.dir_path = os.path.dirname(os.path.dirname(__file__))
        #initializing detector class
        self.detector = Detector()
        #initializing absent time calculation dictionary
        self.inactivity_time_calc={}

    #crop image according to the position of the box
    def crop_position(self, box, image):

        if box and image is not None:
            x, y, w, h = box[0][0], box[0][1], box[1][0], box[1][1] 
            cropped = image[y:y+h, x:x+w]
            return cropped
        else:
            return "image not found", "none"


    #present absent calculation pipeline
    def pipeline(self,camera_id, roi_boxs, image, frame_id, date_time):

        """
        ACTIVITY DETECTION PIPELINE
        Args:
            camera_id: Camera id of the image.
            roi_boxs: List of ROI boxes.
            image_path: Path to the image to detect objects in.
            frame_id: Frame id of the image.
            date_time: Date and time of the image.

        Returns: 
            present_absent: Present or absent status of the person.

        """

        active_time_calc={}
        #loop for each box
        for key in roi_boxs.keys():
            #box position
            box = roi_boxs[key]
            #box id
            person_id = key
            #crop image according to the position of the box
            cropped_input_img = self.crop_position(box, image)

            try:

                frame = cropped_input_img.copy()

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (448, 448))
                frame = np.asarray(frame, dtype=np.float32)
                frame = frame.transpose(2, 0, 1) / 255.0
                frame = torch.from_numpy(frame).unsqueeze(0)
                person_count = run(frame)
                #calling person detector
                person_count,detected_person_image = self.detector.person_detection(cropped_input_img)

                #if person is detected
                if person_count == 1:

                    #calling activity detector
                    activity_class,person_activity_image = run(frame)
                    
                    #if no activity is detected
                    if(activity_class == "no_activity"):
                        #saving inactivity data
                        cv2.imwrite(self.dir_path+"/results/inactivity/frame"+str(frame_id)+"_"+str(time.time())+"_"+str(person_id)+".png", detected_person_image)

                        if person_id not in self.inactivity_time_calc.keys():
                            #saving inactivity time data in dictionary for first time
                            self.inactivity_time_calc[person_id] = {"camera_id":camera_id,"total_inactive_time":1, "date_time":date_time} 

                        else:
                            #updating inactivity time data in dictionary 
                            self.inactivity_time_calc[person_id]["camera_id"] = camera_id
                            self.inactivity_time_calc[person_id]["total_inactive_time"] += 1
                            self.inactivity_time_calc[person_id]["date_time"] = date_time
                    else:
                        #saving activity data
                        # cv2.imwrite(self.dir_path+"/results/activity/"+str(activity_class)+"_frame_"+str(frame_id)+"_"+str(time.time())+"_"+str(person_id)+".png", person_activity_image)
                        if person_id in self.inactivity_time_calc.keys():
                            #copying inactive time data from dictionary to active time data dictionary
                            active_time_calc=self.inactivity_time_calc.copy()
                            
                            del self.inactivity_time_calc[person_id]
                            
                            if active_time_calc[person_id]["total_inactive_time"]>=2:  
                                return active_time_calc
                                
                elif person_count > 1:
                    #saving multiple person data
                    cv2.imwrite(self.dir_path+"/results/multiperson/frame"+str(frame_id)+"_"+str(time.time())+"_"+str(person_id)+".png", detected_person_image)
            
            except Exception as e:
                logger.error(str(e))



            




            

            







                    

                    








        


        # return self.absent_time_calc, self.inactive_time_calc, detected_person_image, person_activity_image

     
                        
 