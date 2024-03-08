from ultralytics import YOLO
import config
import utils
import os

# CONFIGURATION
swith_train = False
swith_pred = True

if swith_train == True:
    # BUILD AND LOAD YOLOv8
    model = YOLO(config.YOLO_pretrained)  # load a pretrained model (recommended for training)

    # TRAIN
    model.train(data=f'{config.DATA_DIR}/data.yaml',
                epochs=config.epochs,
                save_period = config.save_period,
                optimizer=config.optimizer,
                lr0=config.lr0,
                cos_lr=config.cos_lr,
                project=config.project,
                name=config.name)

if swith_pred == True:
    # PREDICTION
    utils.prediction(model_dir=config.MODEL_DIR, img_dir=os.path.join(config.ROOT, "images_cssv_mz_2023/resized"), pred_dir=os.path.join(config.ROOT, "cssv_mz_1/test/PRED_1"), switch_saveImg=True)
    
    # DISTANCE
    utils.distance(pred_dir=os.path.join(config.ROOT, "cssv_mz_1/test/PRED_1"), intercroppedCLS=4, intercropped_thrshld=0)

    # BEARING
    utils.bearing(os.path.join(config.ROOT, "cssv_mz_1/test/PRED_1", "PRED_DIST_CLS_unique.csv"), os.path.join(config.ROOT, "images_cssv_mz_2023/coord_2023.csv"), os.path.join(config.ROOT, "cssv_mz_1/test/PRED_1"))

    # FINAL COORDINATES
    utils.coord_infer(os.path.join(config.ROOT, "cssv_mz_1/test/PRED_1/bearing.csv"), os.path.join(config.ROOT, "cssv_mz_1/test/PRED_1/label.csv"))