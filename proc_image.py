# proc_image.py:
# Process the CAPTCHA into separated small character images
# Then it can be used for training network
# By He Hao, 1600012742@pku.edu.cn

from __future__ import print_function
from PIL import Image
import Queue
import copy
import os

# Image width
IM_W = 37
# Image height
IM_H = 18
# Image background color index
IM_BG = 2


def in_range(x, y):
    return 0 <= x < IM_W and 0 <= y < IM_H


# remove_noise: Remove small color blocks using Breadth First Search
# Parameters:   image - The PIL image to process
# Returns:      PIL Image with small color blocks removed
def remove_noise(image):
    # Offset X and Offset Y
    offsetx = [1, -1, 0, 0, 1, 1, -1, -1]
    offsety = [0, 0, 1, -1, 1, -1, 1, -1]
    # visited is a 37*18 2d array initialized to 0
    visited = [[0 for i in range(18)] for i in range(37)]
    # For each pixel in the image
    # Do breadth first search to compute its connected component
    # If too small, paint it to the background colour
    for x in range(0, IM_W):
        for y in range(0, IM_H):
            if visited[x][y] == 1:
                continue
            visited[x][y] = 1
            size = 0
            q = Queue.Queue()
            q2 = Queue.Queue()
            q.put([x, y])
            q2.put([x, y])
            while not q.empty():
                curr = q.get()
                size += 1
                for i in range(0, 8):
                    nextx = curr[0] + offsetx[i]
                    nexty = curr[1] + offsety[i]
                    if in_range(nextx, nexty) \
                            and image.getpixel((nextx, nexty)) != IM_BG \
                            and visited[nextx][nexty] == 0:
                        q.put([nextx, nexty])
                        q2.put([nextx, nexty])
                        visited[nextx][nexty] = 1
            if size <= 5:
                while not q2.empty():
                    curr = q2.get()
                    image.putpixel((curr[0], curr[1]), IM_BG)
    return image


# compute_occurences: Count occurences of colors in image
# Parameters:         image: PIL image object
# Returns:            A list of 2-element list [color, cnt],
#                     where cnt is the total occurence of color in image.
#                     This list is sorted from highest cnt to lowest.
def compute_occurences(image):
    occurrences = []
    for x in range(0, IM_W):
        for y in range(0, IM_H):
            color = image.getpixel((x, y))
            exist = False
            for i in occurrences:
                if i[0] == color:
                    i[1] += 1
                    exist = True
                    break
            if not exist:
                occurrences.append([color, 1])
    occurrences.sort(key=lambda occur: occur[1])
    occurrences.reverse()
    return occurrences


# proc_image: Take raw image from PKU Dean as input(stored in src_folder)
#             split it into 4 character image(12*14 each),
#             and store the images in the destination folder.
# Parameters: src_folder - the folder with raw image, report error if the
#                 folder doesn't exist.
#             dest_folder - the folder with split characters, create one
#                 if the folder doesn't exist.
# Returns:    nothing
def proc_image(src_folder, dest_folder, image_num):
    images = []  # Create an empty list that stores image data
    if not os.path.exists(src_folder):
        print("Source folder '" + src_folder + "' not found!")
        return

    # Load images in dest_folder
    local_path = os.path.abspath('')
    os.chdir(local_path + os.sep + src_folder)
    for i in range(1, image_num + 1):
        im = Image.open(str(i) + '.png')
        images.append(im)

    # Process them and store the split characters one by one
    os.chdir(local_path)
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    os.chdir(local_path + os.sep + dest_folder)
    curr_fileno = 1
    for i in range(0, image_num):
        im = images[i]

        im = remove_noise(image=im)
        occurences = compute_occurences(image=im)

        # occurences[1,2,3,4] are the most probable characters
        for i in range(1, 5):
            color = occurences[i][0]
            im2 = copy.copy(im)
            # Clear the rest pixel into background color
            # Set additional information for cropping
            minx = IM_W - 1
            maxx = 0
            miny = IM_H - 1
            maxy = 0
            # Adjust and map to 12*14 size
            for x in range(0, IM_W):
                for y in range(0, IM_H):
                    curr_color = im2.getpixel((x, y))
                    if curr_color != color:
                        im2.putpixel((x, y), IM_BG)
                    else:
                        if x < minx:
                            minx = x
                        if x > maxx:
                            maxx = x
                        if y < miny:
                            miny = y
                        if y > maxy:
                            maxy = y

            while maxx - minx < 12:
                minx -= 1
                if maxx - minx == 12:
                    break
                maxx += 1
            while maxy - miny < 14:
                miny -= 1
                if maxy - miny == 14:
                    break
                maxy += 1
            while maxx - minx > 12:
                minx += 1
                if maxx - minx == 12:
                    break
                maxx -= 1
            while maxy - miny > 14:
                miny += 1
                if maxy - miny == 14:
                    break
                maxy -= 1
            # (left, upper, right, lower)
            im2 = im2.crop((minx, miny, maxx, maxy))
            for x in range(0, im2.size[0]):
                for y in range(0, im2.size[1]):
                    if im2.getpixel((x, y)) == 0:
                        im2.putpixel((x, y), IM_BG)
            im2 = im2.convert('L')
            for x in range(0, im2.size[0]):
                for y in range(0, im2.size[1]):
                    if im2.getpixel((x, y)) <= 150:
                        im2.putpixel((x, y), 0)
                    else:
                        im2.putpixel((x, y), 255)
            im2.save(str(curr_fileno) + '.png')
            curr_fileno += 1

    # Restore path
    os.chdir(local_path)
# End of proc_image


# split_image: Take a CAPTCHA image as input and split it into 4 characters
# Parameters:  im - PIL Image Object
# Returns:     A 4-element Dict, each element in this form{min_x, image}
#              min_x is this characters' begin in x axis
#              image is the PIL Image Object representation of this character
def split_image(im):
    result = {}
    im = remove_noise(image=im)
    occurences = compute_occurences(image=im)
    # occurences[1,2,3,4] are the most probable characters
    for i in range(1, 5):
        color = occurences[i][0]
        im2 = copy.copy(im)
        # Clear the rest pixel into background color
        # Set additional information for cropping
        minx = IM_W - 1
        maxx = 0
        miny = IM_H - 1
        maxy = 0
        # Adjust and map to 12*14 size
        for x in range(0, IM_W):
            for y in range(0, IM_H):
                curr_color = im2.getpixel((x, y))
                if curr_color != color:
                    im2.putpixel((x, y), IM_BG)
                else:
                    if x < minx:
                        minx = x
                    if x > maxx:
                        maxx = x
                    if y < miny:
                        miny = y
                    if y > maxy:
                        maxy = y

        while maxx - minx < 12:
            minx -= 1
            if maxx - minx == 12:
                break
            maxx += 1
        while maxy - miny < 14:
            miny -= 1
            if maxy - miny == 14:
                break
            maxy += 1
        while maxx - minx > 12:
            minx += 1
            if maxx - minx == 12:
                break
            maxx -= 1
        while maxy - miny > 14:
            miny += 1
            if maxy - miny == 14:
                break
            maxy -= 1
        # (left, upper, right, lower)
        im2 = im2.crop((minx, miny, maxx, maxy))
        for x in range(0, im2.size[0]):
            for y in range(0, im2.size[1]):
                if im2.getpixel((x, y)) == 0:
                    im2.putpixel((x, y), IM_BG)
        im2 = im2.convert('L')
        for x in range(0, im2.size[0]):
            for y in range(0, im2.size[1]):
                if im2.getpixel((x, y)) <= 150:
                    im2.putpixel((x, y), 0)
                else:
                    im2.putpixel((x, y), 255)
        result[minx] = im2
    return result

