import json
import cv2 as cv
import os
import csv
import pickle
import re
import collections
import numpy as np

pkl_dic = {}

def get_json(vname):
    json_path = r"C:\Users\63147\Desktop\self-made_ava_dataset_tool-master\anno_ava\anno_ava\\" + vname + ".json"
    keyframes_path = r"C:\Users\63147\Desktop\self-made_ava_dataset_tool-master\rawframe\\" + vname + r"\\"
    # The image is loaded to get the total keyframes under the file and the image H W to normalize coordinates

    img_dir = os.listdir(keyframes_path)
    img_nums = len(img_dir)   # Get the number of pictures
    img_0 = img_dir[0]   # The H and W of the same video frame are the same
    #name = img_0.split('_')[0]   # Get picture name
    name = vname
    img = cv.imread(keyframes_path+img_0)

    height = img.shape[0]
    width = img.shape[1]

    start_time = 901  # In order to write out the timestamp that you want

    with open(json_path) as f:
        data = json.load(f)
        img_data = data['metadata']  # The desired coordinates and action ID are under the dictionary
        # print(img_data)
        # print(len(img_data))
        # print(img_data.items())

        for i, (k, v) in enumerate(img_data.items()):
            if 'score' in v.keys():   # len(img_data) - img_numbers。 Remove useless data
                # print(k, v)

                bboxes = v['xy']    # obtain x1, y1, x2, y2,
                                # The coordinates in the JSON file are the upper-left coordinates and the width and height of the box
                vid = int(v['vid'])  # To write out the timestamp automatically
                # print(vid)
                score = v['score'][0]
                # print(score)
                t = start_time + vid
                x1 = round(bboxes[1]/width, 3)
                y1 = round(bboxes[2]/height, 3)
                x2 = round((bboxes[3] + x1)/width, 3)
                y2 = round((bboxes[4] + y1)/height, 3)
                # action_id = v['av'].items()   # Get action ID
                if name + "," + "%04d" % t in pkl_dic.keys():
                    np.append(pkl_dic[name + "," + "%04d" % t],[x1, y1, x2, y2,score])
                else:
                    # pkl_dic.update({name + "," + "%04d" % t :[[x1, y1, x2, y2,score]]})
                    pkl_dic[name + "," + "%04d" % t] = np.array([[x1, y1, x2, y2,score]])

if __name__ == "__main__":
    for root, dirs, files in os.walk(r"C:\Users\63147\Desktop\self-made_ava_dataset_tool-master\anno_ava\anno_ava\\"):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            #print(f)
            get_json(f.split('.')[0])
    with open(r"C:\Users\63147\Desktop\self-made_ava_dataset_tool-master\train_ann.pkl", "wb") as fo:  # write
        pickle.dump(pkl_dic, fo)
        fo.close()


