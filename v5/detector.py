from ctypes import *
import os
import cv2
from main.scripts import darknet
import logging
from logging.handlers import RotatingFileHandler
main_path = os.path.dirname(os.path.realpath('_file_'))
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logHandler = RotatingFileHandler('./logs/detector_success.log', maxBytes=1000, backupCount=3)
logHandler.setLevel(logging.INFO)
logHandler.setFormatter(formatter)
errorlogHandler = RotatingFileHandler(main_path+'./logs/detector_error.log', maxBytes=1000, backupCount=3)
errorlogHandler.setLevel(logging.ERROR)
errorlogHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.addHandler(errorlogHandler)



class Detector:

    def __init__(self):

        try:

            #initializing directory path
            self.dir_path = os.path.dirname(os.path.dirname(__file__))
            #loading person configuration file
            self.person_config_file=os.path.join(self.dir_path, "model","cfg","cropped_person.cfg")
            #loading person data file
            self.person_data_file= os.path.join(self.dir_path, "model","data","person.data")
            #loading person weights file
            self.person_weights_file=os.path.join(self.dir_path, "model","weights","cropped_person.weights")

            #loading activity configuration file
            self.activity_config_file=os.path.join(self.dir_path,"model","cfg","activity_yolov4.cfg")
            #loading activity data file
            self.activity_data_file= os.path.join(self.dir_path,"model","data","activity.data")
            #loading activity weights file
            self.activity_weights_file=os.path.join(self.dir_path,"model","weights","activity_yolov4.weights")

            #loading person network
            self.person_network, self.person_class_names, self.person_class_colors = darknet.load_network(
                self.person_config_file,
                self.person_data_file,
                self.person_weights_file,
                batch_size=1)

            #loading activity network
            self.activity_network, self.activity_class_names, self.activity_class_colors = darknet.load_network(
                self.activity_config_file,
                self.activity_data_file,
                self.activity_weights_file,
                batch_size=1)
            logger.info("person and activity network loaded")

        except Exception as e:
            logger.error(str(e))

    #object detection from image using darknet
    def image_detection(self,image_path, network, class_names, class_colors, thresh):
        """
        Detect objects in an image with Darknet.
        Args:
            image_path: Path to the image to detect objects in.
            network: The network to use for detection.
            class_names: A list of class names for the network.
            class_colors: A list of colors for the network's classes.
            thresh: The threshold for object detection.

        Returns: 
            The image with detected objects.

        """
        #loading darknet width
        width = darknet.network_width(network)
        #loading darknet height
        height = darknet.network_height(network)
        #convert image to darknet image format
        darknet_image = darknet.make_image(width, height, 3)
        #real image path
        image = image_path
        #converting rgb
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #resize image to darknet image format
        image_resized = cv2.resize(image_rgb, (width, height),
                                interpolation=cv2.INTER_LINEAR)
        #byte image 
        darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
        #detecting objects
        detections = darknet.detect_image(network, class_names, darknet_image, thresh=thresh)
        #converting detections to image
        darknet.free_image(darknet_image)
        image=image_resized
        #bounding box 
        # image = darknet.draw_boxes(detections, image_resized)
        #return image and detections result
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), detections


    #person detection 
    def person_detection(self,images):
        """
        Detect objects in an image with Darknet.
        Args:
            image_path: Path to the image to detect objects in.

        Returns: 
            The image with number of detected person.

        """
        try:
            #calling image detection function
            image, detections = self.image_detection(
            images, self.person_network, self.person_class_names, self.person_class_colors, thresh=0.25)
            count=0
            #if person is detected 
            if(len(detections)>0):

                for label, confidence, bbox in detections:
                    if label == 'person':
                        count+=1
                return count,image
            else:
                return 0,images
        except Exception as e:
            logger.error(str(e))

    #activity detection
    def activity_detection(self,images):

        try:
            #calling image detection function
            image, detections = self.image_detection(
            images, self.activity_network, self.activity_class_names, self.activity_class_colors, thresh=0.25)

            if(len(detections)>0):
                for label, confidence, bbox in detections:
                    label=label
                return label,image
            else:
                return "no_activity",images
        except Exception as e:
            logger.error(str(e))
