# dataset.py
# The Dataset Object of images and labels in \train folder
# By He Hao, 1600012742@pku.edu.cn

import numpy as np
from PIL import Image
from proc_image import split_image
import os


# Dataset: The class used to store training data.
# Members: label - a list of all the labels (index start from 0)
#          image - a list of 0-1 matrix representing the images
#                  image[i]'s label is label[i]
#          total - total number of images
class DataSet:
    def __init__(self, folder, total_image):
        self.label = []
        self.images = []
        self.total = total_image
        for i in range(1, total_image + 1):
            with open(folder + os.sep + str(i) + '.txt', 'r') as f:
                self.label.append(f.readline())
            im = Image.open(folder + os.sep + str(i) + '.png')
            w = im.size[0]  # width
            h = im.size[1]  # height
            # construct a h * w matrix to store the image
            mat = np.zeros((h, w))
            for x in range(0, w):
                for y in range(0, h):
                    val = im.getpixel((x, y))
                    if val > 0:
                        mat[y][x] = 0
                    else:
                        mat[y][x] = 1
            self.images.append(mat)


# SingleTestData: Store one image of test data
# Members:        images - dict with 4 pairs {x_begin: mat}
#                          x_begin is the begin of the character in original image
#                          mat is the matrix representation of this character
class SingleTestData:
    def __init__(self, image_file, answer_file):
        self.images = {}
        if answer_file != '':
            with open(answer_file, 'r') as f:
                self.answer = f.readline()
        im = Image.open(image_file)
        split_images = split_image(im)
        for key in split_images:
            tmp = split_images[key]
            w = tmp.size[0]
            h = tmp.size[1]
            mat = np.zeros((h, w), dtype=np.float64)
            for x in range(0, w):
                for y in range(0, h):
                    val = tmp.getpixel((x, y))
                    if val > 0:
                        mat[y][x] = 0
                    else:
                        mat[y][x] = 1
            self.images[key] = mat






