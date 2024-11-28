import os
import utils

YOLO_pretrained = "yolov8x.pt"
ROOT = "/scratch.global/yin00406/streetImgtoLbl"
DATA_DIR = f"{ROOT}/cssv_mz_1"
MODEL_DIR = "/home/jinzn/yin00406/streetImgtoLbl/code_cssv_mz/cshw/detect/weights/last.pt"

VALID_DIR = f"{DATA_DIR}/valid"
TEST_DIR = f"{DATA_DIR}/test"

# TRAINING PARAMETERS
epochs=200
save_period = 5
optimizer="SGD"
lr0=0.001
cos_lr=True
project="cshw" # folder saving the trained model: project/name
name="detect"

h_enlarged_cashew = 640 # unit: px
l_focal_GoPro = 2.84 * 0.01 # unit: m
h_sensor = 4.55 * 0.01 # unit: m
h_GoPro = 1.8 # unit: m