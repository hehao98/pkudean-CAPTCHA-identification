Simple Python Program that recognize CAPTCHA 
from http://dean.pku.edu.cn/student/

Python Language Version: 2.7

Dependencies: 
1. PIL
2. Numpy
3. Tkinter

Executable scripts:

get_data_usage.py: 
Automatically acquire data from http://dean.pku.edu.cn/student/
Store 1000 images in data/ folder as our basic dataset.
Store 100 images in test/ folder for evaluation of our result.
(Optional) Store 10 images in debug/ folder for debugging.

proc_image_usage.py: 
Process image in data/ folder, split it into single characters 
and store it in train/ folder. (Need to be manally marked later)

knn.py:
We use KNN(Kth Nearest Neighbor) Algorithm to recognize CAPTCHA
This is a command line program that 

knn-gui.py:
An interactive GUI program that can acquire an image from PKU Dean online and 
show the result.

gen_label.py: 
This is an assistant program used to manually marking training data

Helper libraries:
proc_image.py
Various functions that helps processing image.

get_data.py:
The function to get data online from dean.pku.edu.cn

dataset.py: 
Define class to read and store data used for recognition and evaluation.






