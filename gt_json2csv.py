import json
import cv2 as cv
import os
import csv

rawframe_path = r"C:\dataset\rawframe\\"
anno_path = r"C:\dataset\anno_ava\\"
output_path = r"C:\dataset\anno_csv\train.csv"

rows = []

def get_json(vname):
    json_path = anno_path + vname + ".json"
    keyframes_path = rawframe_path + vname + r"\\"
    # # The image is loaded to get the total keyframes under the file and the image H W to normalize coordinates

    img_dir = os.listdir(keyframes_path)
    img_nums = len(img_dir)
    img_0 = img_dir[0]  # The H and W of the same video frame are the same
    # name = img_0.split('_')[0]   # Get picture name
    name = vname
    img = cv.imread(keyframes_path + img_0)

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
            #if 'score' in v.keys():  # len(img_data) - img_numbers。 Remove useless data
            if '1' in v['av'].keys():
                # print(k, v)

                bboxes = v['xy']  # obtain x1, y1, x2, y2,
                # The coordinates in the JSON file are the upper-left coordinates and the width and height of the box
                vid = int(v['vid'])  # To write out the timestamp automatically
                # print(vid)
                t = start_time + vid
                x1 = bboxes[1] / width
                y1 = bboxes[2] / height
                x2 = (bboxes[3] + bboxes[1]) / width
                y2 = (bboxes[4] + bboxes[2]) / height

                if x1 < 0:
                    x1 = 0
                if x1 > 1:
                    x1 = 1

                if x2 < 0:
                    x2 = 0
                if x2 > 1:
                    x2 = 1

                if y1 < 0:
                    y1 = 0
                if y1 > 1:
                    y1 = 1

                if y2 < 0:
                    y2 = 0
                if y2 > 1:
                    y2 = 1

                action_id = v['av']['1']  # Get action ID
                #print(vname+" " + str(vid) + " " +action_id)
                person_id = 0
                if "3" in v['av'].keys():
                    person_id = int(v['av']['3'])
                rows.append([name, t, x1, y1, x2, y2, int(action_id)+1, person_id])
                # print(name, t, x1, y1, x2, y2, id)

if __name__ == '__main__':
    for root, dirs, files in os.walk(anno_path):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            #print(f)
            get_json(f.split('.')[0])
    # Create csv
    csvFile = open(output_path, "w+", encoding="gbk")
    CSVwriter = csv.writer(csvFile, lineterminator='\n')
    for row in rows:
        CSVwriter.writerow(row)
    csvFile.close()