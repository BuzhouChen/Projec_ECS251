import os
import random
import numpy as np
from PIL import Image

''' 
Function for choosing random image from folder path.
Finds path of random image and returns the Image object specified in the path.
'''
def pick_random_image_path(folder_path):
    
    image_paths = [f for f in os.listdir(folder_path)]    
    random_image_path = random.choice(image_paths)
    return os.path.join(folder_path, random_image_path)

'''
Function for generating random 256x256 white noise image with error handling.
Saves generated image into directory.
'''
def generate_white_noise_image():
    try: 
        noise = np.random.randint(0, 256, (256, 256, 3), dtype = np.uint8)
        image = Image.fromarray(noise)
        path = "white_noise.jpg"
        image.save(path)
        return path
    except Exception as e:
        print(f"Error in generating image: {e}")
        return None
