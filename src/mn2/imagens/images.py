import numpy as np
import os
import sys
from os import path
from PIL import Image
from typing import List
from skimage.metrics import mean_squared_error as mse
from skimage.metrics import structural_similarity as ssim

class Images: 

    def __init__(self):
        pass
    
    @staticmethod
    def to_vector(file_path: str, height: int = 0, width: int = 0) -> np.ndarray:
        """
            It receives an absolute path to an image file and retreives a vector
            height or width, if passed, resize the vector.
        """
        img = Image.open(file_path)

        #convert image to grey scale
        img = img.convert("L")

        #resize image
        if height > 0 and width > 0:
            img = img.resize( (width, height) )

        matrix: np.ndarray = np.array(img)

        return matrix

    @staticmethod
    def split_images(matrix: np.ndarray, vertical: int = 1, horizontal: int = 1) -> List[np.ndarray]:
        """
            Splits an image matrix evenly in vertical * horizontal pieces
            If those arguments are not specified the matrix is not altered
        """
        height, width = matrix.shape

        h_delta = height/horizontal
        w_delta = width/vertical

        matrices = []

        for i in range(horizontal):
            h_start = round( i * h_delta )
            h_end = round( (i + 1) * h_delta )

            for j in range(vertical):
                w_start = round( j * w_delta )
                w_end = round( (j + 1) * w_delta )

                matrices.append(matrix[h_start:h_end, w_start:w_end])
        
        return matrices

    @staticmethod
    def split_and_save_main_img(img_path: str, vertical: int, horizontal: int):
        """
            Split and save the received image path
        """
        matrices = Images.split_images(Images.to_vector(img_path), vertical, horizontal)

        i = 0

        for M in matrices:
            
            img = Image.fromarray()

            img.show()

            img_path = path.join(path.abspath(os.curdir), "main/imgs/part_{0}.png".format(i))

            i += 1

            img.save(fp=img_path, format="PNG")
    
    @staticmethod
    def is_image(file_path: str) -> bool:
        """
            Check if an image path ends with 
            the following extensions: (jpeg, jpg and png)
        """
        img_exts = [
            "jpeg", 
            "jpg",
            "png"
        ]

        for ext in img_exts:
            if file_path.endswith("." + ext):
                return True

        return False

    @staticmethod
    def get_imgs() -> List[str]:
        """
            Adds all images passed as arguments
            to a list 
        """
        if len(sys.argv) <= 1:
            print("there is no arguments")

            exit(2)

        imgs = []

        for i in range(len(sys.argv)):
            if i <= 0:
                continue

            Images.verify_image(sys.argv[i])
            
            imgs.append(sys.argv[i])

        return imgs

    @staticmethod
    def verify_image(file_path: str) -> None:
        """
            Checks if a file exists and
            is a valid image format
        """

        if not path.isfile(file_path):
            print("not a file")
            exit(1)
        
        if not Images.is_image(file_path):
            print("not an image")
            exit(1)
    
    def compare_images(img_a: str, img_b: str):

        """
            Compares two images with mean squared error 
            and structural similarity index measure
            and retrieves both values respectively
        """

        img_a_vector = Images.to_vector(img_a)
        img_b_vector = Images.to_vector(img_b, img_a_vector.shape[0], img_a_vector.shape[1])


        return mse(img_a_vector, img_b_vector), ssim(img_a_vector, img_b_vector)
        