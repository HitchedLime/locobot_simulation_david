#!/usr/bin/env python3
import os
import sys
import math
from pathlib import Path

import rospy
import cv2
import torch
import torch.backends.cudnn as cudnn
import numpy as np
from cv_bridge import CvBridge


from rostopic import get_topic_type


from sensor_msgs.msg import Image, CompressedImage
from locobot_simulation.msg import BoundingBox, BoundingBoxes
from  nav_msgs.msg import Odometry


from owlready2 import *

TEST =True
# add yolov5 submodule to path
FILE = Path(__file__).resolve()
sys.path.insert(0, './yolov5')
ROOT = FILE.parents[0] / "yolov5"
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative path
data3 = []
# import from yolov5 submodules
from models.common import DetectMultiBackend
from utils.general import (
    check_img_size,
    check_requirements,
    non_max_suppression,
    scale_coords
)
from utils.plots import Annotator, colors
from utils.torch_utils import select_device
from utils.augmentations import letterbox
def filter_nearest(x:float,y:float,id:str,array:list)->list:
    """Finds the nearest item different from current class .That is near our current estimated postion"""
    nearest_items=[]
    for item in array:
       # word = re.sub(r'\d', '',str(item[0]).split('.')[-1]).capitalize()
        distance_from_robot = math.sqrt((x-item[1])**2+(y-item[2])**2)
        if(distance_from_robot<4):
            nearest_items.append(item)
    return nearest_items

def filter_items_close(array:list)->dict:
    distances ={}
    for item in array:
        word = str(item[0]).split('.')[-1]
        for item2 in array:
            word2 = str(item2[0]).split('.')[-1]
            
            distances_between_items=  round(math.sqrt((item2[1]-item[1])**2+(item2[2]-item[2])**2),2)
            if(distances_between_items<3):
                distances[distances_between_items]=(word,word2)
    
    del distances[0]
    return distances
                
            

        




    

def query(query_class:str,default_onto_path ="/home/david/catkin_ws/src/locobot_simulation_david/changed.owl")->list:
    query_base =  f"""
    PREFIX ex: <http://example.org/>
    SELECT ?chair1 ?x ?y
    WHERE {{
        ?chair1 a ex:{query_class}.
        ?chair1 ex:hasX ?x .
        ?chair1 ex:hasY ?y .
    }}
"""
    
    onto = get_ontology(default_onto_path)
    onto.load()
    x =list(default_world.sparql(query_base))
    
    return x 

@torch.no_grad()
class Yolov5Detector:
    def __init__(self):
        self.conf_thres = rospy.get_param("~confidence_threshold")
        self.iou_thres = rospy.get_param("~iou_threshold")
        self.agnostic_nms = rospy.get_param("~agnostic_nms")
        self.max_det = rospy.get_param("~maximum_detections")
        self.classes = rospy.get_param("~classes", None)
        self.line_thickness = rospy.get_param("~line_thickness")
        self.view_image = rospy.get_param("~view_image")
        # Initialize weights 
        weights = rospy.get_param("~weights")
        # Initialize model
        self.device = select_device(str(rospy.get_param("~device","")))
        self.model = DetectMultiBackend(weights, device=self.device, dnn=rospy.get_param("~dnn"), data=rospy.get_param("~data"))
        self.stride, self.names, self.pt, self.jit, self.onnx, self.engine = (
            self.model.stride,
            self.model.names,
            self.model.pt,
            self.model.jit,
            self.model.onnx,
            self.model.engine,
        )

        # Setting inference size
        self.img_size = [rospy.get_param("~inference_size_w", 640), rospy.get_param("~inference_size_h",480)]
        self.img_size = check_img_size(self.img_size, s=self.stride)

        # Half
        self.half = rospy.get_param("~half", False)
        self.half &= (
            self.pt or self.jit or self.onnx or self.engine
        ) and self.device.type != "cpu"  # FP16 supported on limited backends with CUDA
        if self.pt or self.jit:
            self.model.model.half() if self.half else self.model.model.float()
        bs = 1  # batch_size
        cudnn.benchmark = True  # set True to speed up constant image size inference
        self.model.warmup(imgsz=(1 if self.pt else bs, 3, *self.img_size), half=self.half)  # warmup        
        
        # Initialize subscriber to Image/CompressedImage topic
        input_image_type, input_image_topic, _ = get_topic_type(rospy.get_param("~input_image_topic"), blocking = True)
        self.compressed_input = input_image_type == "sensor_msgs/CompressedImage"

        if self.compressed_input:
            self.image_sub = rospy.Subscriber(
                input_image_topic, CompressedImage, self.callback, queue_size=1
            )
        else:
            self.image_sub = rospy.Subscriber(
                input_image_topic, Image, self.callback, queue_size=1
            )

        # Initialize prediction publisher
        self.pred_pub = rospy.Publisher(
            rospy.get_param("~output_topic"), BoundingBoxes, queue_size=10
        )
        # Initialize image publisher
        self.publish_image = rospy.get_param("~publish_image")
        if self.publish_image:
            self.image_pub = rospy.Publisher(
                rospy.get_param("~output_image_topic"), Image, queue_size=10
            )
        
        # Initialize CV_Bridge
        self.bridge = CvBridge()

    def callback(self, data):
        """adapted from yolov5/detect.py"""
        # print(data.header)
        if self.compressed_input:
            im = self.bridge.compressed_imgmsg_to_cv2(data, desired_encoding="bgr8")
        else:
            im = self.bridge.imgmsg_to_cv2(data, desired_encoding="bgr8")
        
        im, im0 = self.preprocess(im)
        # print(im.shape)
        # print(img0.shape)
        # print(img.shape)

        # Run inference
        im = torch.from_numpy(im).to(self.device) 
        im = im.half() if self.half else im.float()
        im /= 255
        if len(im.shape) == 3:
            im = im[None]

        pred = self.model(im, augment=False, visualize=False)
        
        conf_thres=0.10
        iou_thres=0.20
        pred = non_max_suppression(
            pred, conf_thres, iou_thres, self.classes, self.agnostic_nms, max_det=10
        )
        
        
        

        ### To-do move pred to CPU and fill BoundingBox messages
        
        # Process predictions 
        det = pred[0].cpu().numpy()
        
        if (TEST==True):
            for prediction in  det: 
                if(prediction[-1]==56 or prediction[-1]==26):
                    if(prediction[-1]==56):
                        query_string="Suitcase"
                    elif(prediction[-1]==26): 
                        query_string ="Chair"

                    if(data3):
                        x= data3[-1].pose.pose.position.x
                        y= data3[-1].pose.pose.position.y
                    
                        ontology_data =query(query_string)
                        items_near = filter_nearest(x,y,query_string,ontology_data)
                        items_close_to = filter_items_close(items_near)
                        for key in items_close_to:
                            for  x  in items_close_to[key]:
                                    if(query_string==re.sub(r'\d', '', x).capitalize()):
                                            
                                            if(prediction[-2] <0.40):
                                                print(f"pre {prediction}")
                                                prediction[-2]= prediction[-2]+ 0.4
                                                print(f"po {prediction}")



                
       
        bounding_boxes = BoundingBoxes()
        bounding_boxes.header = data.header
        bounding_boxes.image_header = data.header
        
        annotator = Annotator(im0, line_width=self.line_thickness, example=str(self.names))
        if len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

            # Write results
            for *xyxy, conf, cls in reversed(det):
                bounding_box = BoundingBox()
                c = int(cls)
                # Fill in bounding box message
                bounding_box.Class = self.names[c]
                bounding_box.probability = conf 
                bounding_box.xmin = int(xyxy[0])
                bounding_box.ymin = int(xyxy[1])
                bounding_box.xmax = int(xyxy[2])
                bounding_box.ymax = int(xyxy[3])

                bounding_boxes.bounding_boxes.append(bounding_box)

                # Annotate the image
                if self.publish_image or self.view_image:  # Add bbox to image
                      # integer class
                    label = f"{self.names[c]} {conf:.2f}"
                    annotator.box_label(xyxy, label, color=colors(c, True))       

                
                ### POPULATE THE DETECTION MESSAGE HERE

            # Stream results
            im0 = annotator.result()

        # Publish prediction
        self.pred_pub.publish(bounding_boxes)

        # Publish & visualize images
        if self.view_image:
            cv2.imshow(str(0), im0)
            cv2.waitKey(1)  # 1 millisecond
        if self.publish_image:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(im0, "bgr8"))
        

    def preprocess(self, img):
        """
        Adapted from yolov5/utils/datasets.py LoadStreams class
        """
        img0 = img.copy()
        img = np.array([letterbox(img, self.img_size, stride=self.stride, auto=self.pt)[0]])
        # Convert
        img = img[..., ::-1].transpose((0, 3, 1, 2))  # BGR to RGB, BHWC to BCHW
        img = np.ascontiguousarray(img)

        return img, img0 

def callback3(data_odo):
    global data3
    data3.append(data_odo)
    #print(f'{data3}')

  

if __name__ == "__main__":

    check_requirements(exclude=("tensorboard", "thop"))
    
    rospy.init_node("yolov5", anonymous=True)
    detector = Yolov5Detector()
    odometry_sub =rospy.Subscriber("/locobot/odom",Odometry,callback3)
    rospy.spin()
