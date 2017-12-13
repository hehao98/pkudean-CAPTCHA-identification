# Naive KNN Algorithm for image recognition
# By He Hao, 1600012742@pku.edu.cn

import numpy as np
from dataset import DataSet
from dataset import SingleTestData
import os

TOTAL_IMAGE = 400

# Read data from train/ folder
data = DataSet('train', TOTAL_IMAGE)

# vec is a dict:
# Its key is the label of each training image
# Its value is a 168d vector representing each character
vecs = {}
for i in range(0, data.total):
    label = data.label[i]
    vec = data.images[i].flatten()
    if vecs.has_key(label):
        vecs[label].append(vec)
    else:
        vecs[label] = []
        vecs[label].append(vec)

# For each label and its images,
# Compute the label's center in the 168d space
centers = {}
for key in vecs:
    total = np.zeros(168, dtype=np.float64)
    cnt = 0
    for vec in vecs[key]:
        total += vec
        cnt += 1
    centers[key] = total / cnt

# Evalulate each image
total_images = 100
total_chars = total_images * 4
right_images = 0
right_chars = 0
for i in range(1, total_images + 1):
    test_data = SingleTestData(image_file='test' + os.sep + str(i) + '.png',
                               answer_file='test' + os.sep + str(i) + '.txt')
    chars = {}
    begins = []
    for im_begin, im in test_data.images.items():
        curr_vec = im.flatten()
        curr_char = ''
        min_dist = 100000
        for key in centers:
            dist = np.linalg.norm(centers[key] - curr_vec)
            if dist < min_dist:
                min_dist = dist
                curr_char = key
        chars[im_begin] = curr_char
        begins.append(im_begin)
    begins.sort()

    result = ''
    for index in begins:
        result += chars[index][0]
    print("Image: " + str(i) + '.png')
    print("The correct answer is: " + test_data.answer)
    print("Our predicted answer is : " + result)
    if test_data.answer != result:
        print("Perdiction failed!")
    else:
        right_images += 1
    for tmp in range(0, 4):
        if test_data.answer[tmp] == result[tmp]:
            right_chars += 1
    print("")

print("**********Report**********")
print("Total images: " + str(total_images))
print("Images guessed correct: " + str(right_images))
print("Total chars: " + str(total_chars))
print("Chars guessed correct: " + str(right_chars))


