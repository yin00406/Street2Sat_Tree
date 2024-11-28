import os
import cv2
from ultralytics import YOLO
import pandas as pd
import math
import config
from PIL import Image
import csv
import pandas as pd
import math
from pyproj import Transformer
import pandas as pd

def prediction(model_dir, img_dir, pred_dir, switch_saveImg):
    
    model = YOLO(model_dir)

    # New file to store info
    with open(os.path.join(pred_dir, "PRED.csv"), 'w') as f:
        f.write('img,box,cls,conf,top_left_x_min,top_left_y_min,bottom_right_x_max,bottom_right_y_max\n')

    # Run batched inference on a list of images
    results = model(os.path.join(img_dir, "*jpg"))

    # Process results list
    for idx, result in enumerate(results):
        boxes = result.boxes

        if len(boxes) > 3:
            print(f"Image {idx} - Detected boxes: {len(boxes)}")
            if switch_saveImg==True:
                res_plotted = result.plot()
                cv2.imwrite(os.path.join(pred_dir, f'{result.path.split("/")[-1]}'), res_plotted)
            for i in range(len(boxes)):
                if (boxes.data[i][1] > 0.25):
                    with open(os.path.join(pred_dir, "PRED.csv"), 'a') as f:
                        f.write(f'{result.path.split("/")[-1].split(".")[0]},{i+1}, {boxes.cls[i]},{boxes.conf[i]},{boxes.data[i][0]},{boxes.data[i][1]},{boxes.data[i][2]},{boxes.data[i][3]}\n')

def distance(pred_dir, intercroppedCLS, intercropped_thrshld):

    PRED = pd.read_csv(os.path.join(pred_dir, "PRED.csv"), header=0)

    PRED_Distance = os.path.join(pred_dir, 'PRED_Distance.csv')
    with open(PRED_Distance, 'w') as f:
        f.write("IMG,CLS,Distance,DistanceTotal,DistanceAverage\n")

    rowName_prev = ""
    for idx, row in PRED.iterrows():

        rowName = row.loc['img']
        cls = row.loc['cls']
        
        h_original_cashew = row.loc["bottom_right_y_max"] - row.loc["top_left_y_min"] # unit: px
        l_focal_new = config.h_enlarged_cashew / h_original_cashew * config.l_focal_GoPro
        theta = math.atan(config.h_sensor / (2 * l_focal_new))  # unit: radian
        d = config.h_GoPro / math.tan(theta)  # distance; unit: m

        if rowName != rowName_prev:
            rowName_prev = rowName
            n = 1
            distance_total = 0
            distance_total += d
            distance_ave = distance_total
        elif rowName == rowName_prev:
            n += 1
            distance_total += d
            distance_ave = distance_total / n

        with open(PRED_Distance, 'a') as f:
            f.write(f"{rowName}, {cls}, {d}, {distance_total}, {distance_ave}\n")

    # one distance and one label for one figure
    df = pd.read_csv(PRED_Distance)
    max_distance_rows = df.sort_values('DistanceTotal', ascending=False).drop_duplicates('IMG')
    proportions = df.groupby('IMG')['CLS'].value_counts(normalize=True).unstack()# return frequency/proportion
    # print("proportions: ", proportions)
    multi_class_imgs = proportions[(proportions > intercropped_thrshld).sum(axis=1) > 1].index
    # print("multi_class_imgs: ", multi_class_imgs)
    max_distance_rows['CLS'] = max_distance_rows.apply(lambda row: intercroppedCLS if row['IMG'] in multi_class_imgs else row['CLS'], axis=1) # intercropped code: 4
    max_distance_rows.to_csv(os.path.join(pred_dir, 'PRED_DIST_CLS_unique.csv'), index=False)

def bearing(path_img_label, path_img_coord, output_folder):

    # Get coord for imgs with labels
    output_file = os.path.join(output_folder, 'bearing.csv')

    ## Read the values from the 'IMG' column in file A
    values_to_match = {}
    with open(path_img_label, mode='r', encoding='utf-8-sig') as f_a:
        reader_a = csv.DictReader(f_a)
        for row in reader_a:
            values_to_match[row["IMG"]] = row

    ## Select coord according to 'IMG' column in file A
    coord_all = {}
    columns_coord = ['Latitude', 'Longitude']
    columns_coord_assist = ['Latitude_assist', 'Longitude_assist']
    with open(path_img_coord, mode='r', encoding='utf-8-sig') as f_b:
        reader = csv.DictReader(f_b)
        for row in reader:
            coord_all[row['filename']] = row

        for filename in values_to_match:
            if filename in coord_all:
                for col in columns_coord:
                    values_to_match[filename][col] = coord_all[filename][col]
                filename_prev = f"{filename.split('G')[0]}G{int(filename.split('G')[1]) - 2:07d}"
                filename_prev_2 = f"{filename.split('G')[0]}G{int(filename.split('G')[1]) -3 :07d}"
                if (filename_prev in coord_all):
                    if (coord_all[filename][columns_coord[0]] != coord_all[filename_prev][columns_coord[0]]) & (coord_all[filename][columns_coord[1]] != coord_all[filename_prev][columns_coord[1]]):
                        for col, col_assist in zip(columns_coord, columns_coord_assist):
                            values_to_match[filename][col_assist] = coord_all[filename_prev][col]
                elif (filename_prev_2 in coord_all):
                    if (coord_all[filename][columns_coord[0]] != coord_all[filename_prev_2][columns_coord[0]]) & (coord_all[filename][columns_coord[1]] != coord_all[filename_prev_2][columns_coord[1]]):
                        for col, col_assist in zip(columns_coord, columns_coord_assist):
                            values_to_match[filename][col_assist] = coord_all[filename_prev_2][col]
                else:
                    for col_assist in columns_coord_assist:
                        values_to_match[filename][col_assist] = None

    ## Write the updated rows to a new file
    with open(output_file, mode='w', encoding='utf-8') as f_out:
        fieldnames = reader_a.fieldnames + columns_coord + columns_coord_assist
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in values_to_match.values():
            writer.writerow(row)

def coord_new_points(x, y, x1, y1, distance):

    # Calculate direction vector (dx, dy)
    dx = x1 - x
    dy = y1 - y

    # Normalize the direction vector
    length = math.sqrt(dx ** 2 + dy ** 2)
    dx /= length
    dy /= length

    # Calculate perpendicular vector (to the right)
    perp_dx = dy
    perp_dy = -dx

    # Calculate new point
    new_x = x1 + perp_dx * distance
    new_y = y1 + perp_dy * distance

    return new_x, new_y

def coord_infer(csv_path, new_csv_path):

    df = pd.read_csv(csv_path).dropna()

    # from wgs 1984 to WGS 1984 Web Mercator (auxiliary sphere)
    wgs84 = Transformer.from_proj(4326, 3857, always_xy=True)

    # Calculate new points
    new_points = []
    for index, row in df.iterrows():
        x, y = wgs84.transform(row['Longitude_assist'], row['Latitude_assist'])
        x1, y1 = wgs84.transform(row['Longitude'], row['Latitude'])

        # Calculate new point
        new_x, new_y = coord_new_points(x, y, x1, y1, row['DistanceAverage'])
        new_points.append({'IMG':row['IMG'], 'CLS':row['CLS'], 'LON_ORIGIN':row['Longitude'], 'LAT_ORIGIN':row['Latitude'], 'LON': new_x, 'LAT':new_y})

    new_df = pd.DataFrame(new_points)
    new_df.to_csv(new_csv_path, index=False)