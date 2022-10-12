# # data move 

import os
import shutil
sourcepath='/home/faisal/Downloads/Banpr_data1/bangla_license_plate_synth'
sourcefiles = os.listdir(sourcepath)
# sourcepath2='anpr_data\\train'
# sourcefiles2 = os.listdir(sourcepath2)

destinationpath = 'trash'
for file in sourcefiles:
    # for file2 in sourcefiles2:
    #     if file!=file2:
            if file.endswith('.jpg'):
                shutil.move(os.path.join(sourcepath,file), os.path.join(destinationpath,file))



import os
import shutil
sourcepath='Banpr_data2/test/test'
sourcefiles = os.listdir(sourcepath)
# destinationpath = 'anpr_data\\images\\val'
file1 = open("test.txt","w")#write mode
for file in sourcefiles:
    if file.endswith('.jpg'):
        file1.write("data/ts/"+file+'\n')
       # file1.close()



# # rename files

import os
from os import path
import shutil

Source_Path = 'json2yolo_input\\sewing'
Destination = 'json2yolo_input\\sewing'
Source_Path2 = 'output'
Destination2 = 'output'

Source_Path3 = 'input\\New folder (2)\\not taken_organized\\frames_25-04-2022_12_25_39_trackID=32\\image'   
Destination3 = 'input\\New folder (2)\\not taken_organized\\frames_25-04-2022_12_25_39_trackID=32\\image'
Source_Path4 = 'input\\New folder (2)\\not taken_organized\\frames_25-04-2022_12_25_39_trackID=32\\label'
Destination4 = 'input\\New folder (2)\\not taken_organized\\frames_25-04-2022_12_25_39_trackID=32\\label'
dst_folder = os.mkdir(Destination)


def main():
    for count, filename in enumerate(os.listdir(Source_Path)):
        jjj=filename.split('.')[0]
        # jjj=filename.split('\\')[1]
        # print(jjj)
    
        dst = "sw_"+str(count) + ".png"
        os.rename(os.path.join(Source_Path, filename),  os.path.join(Destination, dst))

    for count, filename2 in enumerate(os.listdir(Source_Path2)):
        # # rename all the files
        
        jj=filename2.split('.')[0]
        # jjj=filename.split('\\')[1]
        # print(jjj)
    
        dst2 = "sw_"+str(count) + ".txt"

        # # rename all the files
        os.rename(os.path.join(Source_Path2, filename2),  os.path.join(Destination2, dst2))

    for count, filename3 in enumerate(os.listdir(Source_Path3)):
        jjj=filename3.split('.')[0]
        # jjj=filename.split('\\')[1]
        # print(jjj)
    
        dst3 = "abir47_"+jjj + ".jpeg"
        os.rename(os.path.join(Source_Path3, filename3),  os.path.join(Destination3, dst3))

    for count, filename4 in enumerate(os.listdir(Source_Path4)):
        # # rename all the files
        
        jj=filename4.split('.')[0]
        # jjj=filename.split('\\')[1]
        # print(jjj)
    
        dst4 = "abir47_"+jj + ".txt"

        # # rename all the files
        os.rename(os.path.join(Source_Path4, filename4),  os.path.join(Destination4, dst4))


# Driver Code
if __name__ == '__main__':
    main()


# # jpg to png

from glob import glob                                                           
import cv2 
pngs = glob('input/train/non_covid/*.jpeg')

for j in pngs:
    jj=j.split('\\')[1]
    # print(j[:-4])
    img = cv2.imread(j)
    cv2.imwrite(j[:-4] + 'png', img)


# GRAY CONVERSION

from glob import glob
import cv2

src = glob("DE\\*.png")

for j in src:
    jj=j.split('\\')[1]
    img=cv2.imread(j)
    img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(j[:-3]+'png',img)


with open('person_data\\Faisal\\faisal\\label\\faisal1_frame-60.txt') as f:
    lines = f.read()
    print(type(lines))
with open('person_data\\Faisal\\faisal\\label\\faisal1_frame-60.txt','r') as f:
    for line in f:
        print(line.split(' ')[0])




# # search class id from txt file 

import glob
import os
for filename in glob.glob('person_data\\full_test_data\\test\\*.txt'):
   with open(os.path.join(os.getcwd(), filename), 'r') as f:

        for line in f:
            value=line.split(' ')[0]
            if(value!="0"):
                data = value.replace(value, "0")

                with open(os.path.join(os.getcwd(), filename), 'w') as file:

                    # Writing the replaced data in our
                    # text file
                    file.write(data)



import os
import shutil
sourcepath='balanced/test'
sourcefiles = os.listdir(sourcepath)
# sourcepath2='anpr_data\\train'
# sourcefiles2 = os.listdir(sourcepath2)

destinationpath = 'balanced/test_label'
for file in sourcefiles:
    # for file2 in sourcefiles2:
    #     if file!=file2:
            if file.endswith('.txt'):
                shutil.move(os.path.join(sourcepath,file), os.path.join(destinationpath,file))



#move .txt amd image files

import os
from collections import defaultdict
import shutil

EXTENSIONS = {'.jpg', '.txt'}

directory = 'cars_train'

grouped_files = defaultdict(int)

count=0

for f in os.listdir(directory):
    name, ext = os.path.splitext(os.path.join(directory, f))
    if ext in EXTENSIONS:
        grouped_files[name] += 1

for name in grouped_files:
        if grouped_files[name] == len(EXTENSIONS):
                with open('{}.jpg'.format(name)) as image_file, \
                        open('{}.txt'.format(name)) as txt_file:
                    files_to_move = [txt_file, image_file]
                    # print(files_to_move)
                    for file in files_to_move:
                        # print(file.name)
                        count+=1
                        shutil.move(file.name, 'annoted_car_data')
print("\ntotal files moved:",count)


#remove contents of .txt file other than LP


import os
  
# Folder Path
path = "/home/faisal/Helios/data/10000_data_acmeai/car_labels"
  
# Change the directory
os.chdir(path)
  
# Read text File 
def read_text_file(file_path):
    with open(file_path, 'r') as f:
        x=f.read()
        return x
  
# iterate through all file
for file in os.listdir():
    # Check whether file is in text format or not
    if file.endswith(".txt"):
        file_path = f"{path}/{file}"
        file_name=file_path.split("/")[-1]
        print(file_name)
        values=open(file_path,"r")
        x = values.split('\n', 1)[0]
        if (x.endswith(",LP,")):
            remove_last=(x[:-1])
            print(remove_last)
            file_write = open(file_path,"w") #write files
            file_write.write(remove_last)



# # data move while checking the length of file name 

import os
import shutil
sourcepath='/home/faisal/Downloads/Banpr_data1/bangla_license_plate_synth'
sourcefiles = os.listdir(sourcepath)

destinationpath = '/home/faisal/Downloads/trash'
for file in sourcefiles:
    if file.endswith('.jpg'):
        print((file))
        if(len(file)<11):
            shutil.move(os.path.join(sourcepath,file), os.path.join(destinationpath,file))

        



