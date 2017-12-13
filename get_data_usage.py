# get_data_usage.py:
# Use this to automatically get data set from PKU Dean website

from get_data import get_data

# Simple folder with 10 random CAPTCHA images for debugging
get_data(num=10, folder='debug')
# data/ stores the raw data images, need to be processed before training
# test/ stores the images to evaluate our model
get_data(num=1000, folder='data')
get_data(num=100, folder='test')