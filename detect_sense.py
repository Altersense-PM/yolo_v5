import argparse
import cv2
import os
import sys
import numpy as np
from pathlib import Path
import torchvision
import torch
import torch.backends.cudnn as cudnn

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from root.models.common import DetectMultiBackend
from root.utils.dataloaders import  LoadImages

from root.utils.torch_utils import select_device, time_sync
from root.utils.general import (check_img_size, check_requirements, non_max_suppression,xyxy2xywh)

@torch.no_grad()

def run(frame):

    weights=ROOT / 'root/weight/activity_best.pt'  # model.pt path(s)
    data=ROOT / 'root/cfg/custom.yaml'  # dataset.yaml path
    imgsz=(448, 448)  # inference size (height, width)
    conf_thres=0.25  # confidence threshold
    iou_thres=0.45 # NMS IOU threshold
    max_det=1000  # maximum detections per image
    device="cpu"  # cuda device, i.e. 0 or 0,1,2,3 or cpu
    classes=None  # filter by class: --class 0, or --class 0 2 3

    device = select_device(device)
    model = DetectMultiBackend(weights, device=device,data=data)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size
    # print(imgsz)

    pred=model(frame)
    pred = non_max_suppression(pred, conf_thres, iou_thres, classes, max_det)
    


    # Process predictions
    for i, det in enumerate(pred):  # per image
        # p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

        gn = torch.tensor(frame.shape)[[1, 0, 1, 0]]  # normalization gain whwh

        count=0

    


        for *xyxy, conf, cls in reversed(det):
            # print(xyxy)
            xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
            c = int(cls)
            print(names[c])
            count+=1
            
    
        
        # print(count) 
        # return count 
        # print(len(det))  
        return count






# if __name__ == "__main__":
#     source=ROOT / 'video/401.mp4'
#     run(source)
