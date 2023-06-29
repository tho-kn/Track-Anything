import os
import re
import shutil
from tkinter import filedialog
from tkinter import Tk

# Define a function to extract index from a filename
def extract_index(filename):
    # Use a regex to find all groups of digits in the filename
    matches = re.findall(r'\d+', filename)

    # If any groups of digits were found, return the last one as the index (as int)
    if matches:
        return int(matches[-1])

# Define a function to handle directory selection and mask creation
def process_directory():
    # Create a Tk root widget (and immediately hide it)
    root = Tk()
    root.withdraw()

    # Open a directory selection dialog
    print("Choose Image Directory")
    image_directory = filedialog.askdirectory()
    print("Choose Mask Directory")
    mask_directory = filedialog.askdirectory() # Assume masks are in another directory

    # Create a new mask destination directory path
    mask_dest_directory = os.path.join(os.path.dirname(image_directory), 'masks')

    # Create the new mask directory if it does not exist
    if not os.path.exists(mask_dest_directory):
        os.makedirs(mask_dest_directory)

    # Create a dictionary to map from indices to mask filenames
    mask_dict = {extract_index(filename): filename for filename in os.listdir(mask_directory)}

    # Iterate over all image files in the selected directory
    for filename in os.listdir(image_directory):
        if filename.endswith('.jpg') or filename.endswith('.png'): # add or modify the conditions based on your image file types
            # Extract the index from the image filename
            index = extract_index(filename)

            # Find the corresponding mask filename in the dictionary
            mask_filename = mask_dict.get(index)

            if mask_filename:
                # Create paths to the image file and the corresponding mask file
                image_path = os.path.join(image_directory, filename)
                mask_path = os.path.join(mask_dest_directory, filename + ".png") # we'll use the same name as the image but with .png extension
                mask_source_path = os.path.join(mask_directory, mask_filename)

                # Copy the mask file to the new location with the new name
                shutil.copy(mask_source_path, mask_path)

    # Destroy the root widget
    root.destroy()

# Call the function
process_directory()
