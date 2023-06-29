import os
import numpy as np
from PIL import Image, ImageOps
import shutil
from tqdm import tqdm
import cv2

def resize_and_invert_and_merge_images_in_directory(directory, size=(3360, 3360), dilation_size=5):
    # Open the mask with which all images will be merged
    merge_mask = np.array(Image.open('mask.png').convert("RGB"))  # Convert to RGB

    for foldername in os.listdir(directory):
        subdir = os.path.join(directory, foldername)
        print("Processing {}".format(foldername))
        if os.path.isdir(subdir):
            files = tqdm(os.listdir(subdir))
            for filename in files:
                if filename.endswith('.png'):  # adjust this if you have .jpg or other file types
                    img_path = os.path.join(subdir, filename)
                    
                    # Create new directory structure for resized images
                    new_subdir = subdir.replace("/result/mask", "/result/mask_resized")
                    if not os.path.exists(new_subdir):
                        os.makedirs(new_subdir)
                    
                    new_img_path = os.path.join(new_subdir, filename)
                    
                    # Open, convert to RGB and resize the image
                    img = np.array(Image.open(img_path).convert("RGB").resize(size, Image.LANCZOS))  # Convert to RGB
                    
                    # Invert the image
                    img = 255 - img

                    # Merge with the additional mask
                    img = np.minimum(img, merge_mask)

                    # Expand the masked area by dilation operation
                    kernel = np.ones((dilation_size, dilation_size), dtype='uint8')
                    img = cv2.erode(img, kernel)

                    # Convert back to Image and save
                    img = Image.fromarray(img.astype('uint8'))
                    img.save(new_img_path)
                    
                    # Move the original mask image to the archive directory
                    archive_subdir = subdir.replace("/result/mask", "/result/mask_archive")
                    if not os.path.exists(archive_subdir):
                        os.makedirs(archive_subdir)
                    
                    archive_img_path = os.path.join(archive_subdir, filename)
                    shutil.move(img_path, archive_img_path)

    print("Images resized, inverted, merged with 'mask.png', mask area expanded and original masks moved to archive.")

# Call the function
resize_and_invert_and_merge_images_in_directory('./result/mask')
