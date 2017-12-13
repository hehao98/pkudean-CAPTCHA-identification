# gen_label:
# Simple assistant program for manually marking training data

import os

begin = input('Enter the begin of image sequence you want to mark: ')
folder = raw_input('Enter the folder you want to work in: ')
end = input('Enter the max number of file: ')
for i in range(begin, end + 1):
    with open(folder + os.sep + str(i) + '.txt', 'w') as f:
        ch = raw_input('Enter the label of ' + str(i) + ': ')
        f.write(ch)
