# knn-gui.py
# This is a simple interactive gui program that displays our training
# process and interactively get images online to test our result.
# By He Hao, 1600012742@pku.edu.cn


import Tkinter as tk
import numpy as np
from PIL import Image
from PIL import ImageTk
from dataset import DataSet
from dataset import SingleTestData
from get_data import get_data
import os

TRAINED = False
centers = {}
images_shown = []
total_images_shown = 0;

class Application(tk.Frame):

    def msg(self, str):
        self.terminal.insert(tk.END, str);

    def start_training(self):
        global TRAINED
        global centers
        if TRAINED:
            app.msg("Dataset already trained!\n")
            return
        TRAINED = True

        TOTAL_IMAGE = 400

        # Read data from train/ folder
        self.msg("Reading Training Data from local train/ folder...\n")
        data = DataSet('train', TOTAL_IMAGE)

        # vec is a dict:
        # Its key is the label of each training image
        # Its value is a 168d vector representing each character
        self.msg("Training center for each label...\n")
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
        self.msg("Training completed!\n")
        # self.msg("The centers are: " + str(centers));
        return

    def test(self):
        global total_images_shown
        global images_shown
        global TRAINED

        if not TRAINED:
            self.msg("The Dataset has not been trained, click train first.\n")
            return

        get_data(num=1, folder="debug")
        im = Image.open("debug" + os.sep + "1.png")
        images_shown.append(ImageTk.PhotoImage(im))
        total_images_shown += 1
        self.msg("This is an image collected from dean.pku.edu.cn: ")
        self.terminal.image_create(tk.END, image=images_shown[total_images_shown - 1])
        self.msg("\n")

        test_data = SingleTestData(image_file='debug' + os.sep + '1.png',
                                   answer_file='')
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

        self.msg("We guess the CAPTCHA is: " + result + "\n")
        return


    def create_widgets(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)

        self.terminal = tk.Text(self)
        self.terminal.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W)

        self.tmp = ImageTk.PhotoImage(Image.open("data/1.png"))
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=1, column=0, sticky=tk.N + tk.E + tk.S + tk.W)

        self.trainBtn = tk.Button(self.button_frame)
        self.trainBtn.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.trainBtn["text"] = "Train"
        self.trainBtn["command"] = self.start_training

        self.testBtn = tk.Button(self.button_frame)
        self.testBtn.grid(row=0, column=1, sticky=tk.N+tk.E+tk.S+tk.W)
        self.testBtn["text"] = "Test"
        self.testBtn["command"] = self.test

        self.QUIT = tk.Button(self.button_frame)
        self.QUIT.grid(row=0, column=2, sticky=tk.N+tk.E+tk.S+tk.W)
        self.QUIT["text"] = "Quit"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.quit


    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        #self.pack()
        self.grid()
        self.create_widgets()


root = tk.Tk()

app = Application(master=root)
app.master.title("PKU Dean CAPTCHA Identifier")
app.mainloop()

root.destory()


