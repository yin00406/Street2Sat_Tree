import csv
import os
from PIL import Image

def coord_gopro(src, tgt):
    '''
    Extracts metadata fields from JPEG images in a directory and writes them to a CSV file.

    Args:
    - src (str): Path to the directory containing JPEG images
    - tgt (str): Path to the output CSV file
    '''

    # Open output file and create CSV writer
    with open(tgt, 'w', newline='') as output_file:
        writer = csv.writer(output_file)

        # Write header row to CSV file
        header = ['filename', 'Latitude', 'Longitude', 'Altitude', 'Time']
        writer.writerow(['filename', 'Latitude', 'Longitude', 'Altitude', 'Time'])

        # Loop over JPEG files in directory and extract metadata
        for filename in os.listdir(src):
            if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
                # Open image and extract metadata
                try:
                    with Image.open(os.path.join(src, filename)) as img:
                        exif_data = img._getexif()
                        if 34853 in exif_data: # gps info
                            gps_info = exif_data[34853]

                            globals()[header[1]] = round(
                                float(gps_info[2][0]) + float(gps_info[2][1]) / 60 + float(gps_info[2][2]) / 3600, 7)
                            if gps_info[1] == 'S':
                                globals()[header[1]] = - round(
                                    float(gps_info[2][0]) + float(gps_info[2][1]) / 60 + float(gps_info[2][2]) / 3600,
                                    7)
                            globals()[header[2]] = round(
                                float(gps_info[4][0]) + float(gps_info[4][1]) / 60 + float(gps_info[4][2]) / 3600, 7)
                            if gps_info[3] == 'W':
                                globals()[header[2]] = - round(
                                    float(gps_info[4][0]) + float(gps_info[4][1]) / 60 + float(gps_info[4][2]) / 3600,
                                    7)
                            globals()[header[3]] = gps_info[6]
                            globals()[header[4]] = gps_info[29].replace(":", "/")

                            # Write metadata to CSV file
                            writer.writerow([filename, Latitude, Longitude, Altitude, Time])
                except:
                    print(f"damaged img: {filename}")

def merge_csv(src, tgt):
  # Open the output file in write mode
  with open(tgt, 'w', newline='') as outfile:
      writer = csv.writer(outfile)
      writer.writerow(['filename', 'Latitude', 'Longitude', 'Altitude', 'Time'])

      filenames = os.listdir(src)
      for filename in filenames:
        if filename.endswith(".csv") and filename != tgt.split("/")[-1]:
          with open(os.path.join(src, filename), 'r') as infile:
            reader = csv.reader(infile)
            next(reader, None) # skip the 1st row
            writer.writerows(reader)

# root = "/scratch.global/yin00406/streetImgtoLbl/images_cssv_mz_2023"
# folders = os.listdir(root)
# img_folders = []
# for folder in folders[4:]:
#     if folder != "resized":
#         print(folder, end=" ")
#         coord_gopro(os.path.join(root,folder), os.path.join(root, f"coord_{folder}.csv"))

merge_csv("/scratch.global/yin00406/streetImgtoLbl/images_cssv_mz_2023", "/scratch.global/yin00406/streetImgtoLbl/images_cssv_mz_2023/coord_2023.csv")