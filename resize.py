import os
from PIL import Image

# RESIZE IMGS
def stretch_image(input_path, output_path):
    # Open the image file
    try:
        with Image.open(input_path) as img:
            # Resize the image to 640x640
            stretched_img = img.resize((640, 640))

            # Save the stretched image
            stretched_img.save(output_path)
    except:
        print(f"damaged img: {input_path}")

root = "/scratch.global/yin00406/streetImgtoLbl/images_cssv_mz_2023"
if not os.path.exists(os.path.join(root, "resized")):
    os.mkdir(os.path.join(root, "resized"))
folders = os.listdir(root)
img_folders = []
for folder in folders:
    if (folder == "Oyo_0923") or (folder == "Oyo_0924"):
        print(folder, end=" ")
        imgs = os.listdir(os.path.join(root, folder))
        for img in imgs:
            if img.endswith("jpg") or img.endswith("jpeg") or img.endswith("JPG") or img.endswith("JPEG"):
                stretch_image(os.path.join(root, folder, img),
                              os.path.join(root, "resized", f"{folder}_{img.split('.')[0]}.jpg"))
