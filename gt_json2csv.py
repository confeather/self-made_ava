import json
import cv2 as cv
import os
import csv

# rawframe_path = r"C:\dataset\rawframe\\"
video_path = r'E:\dataset\custom'
anno_path = r"E:\dataset\videos_ann_val"
output_path = r"E:\dataset\csv\val.csv"

video_dict = {} # name: path
rows = []

def get_video(v_path):
    for root, dirs, files in os.walk(v_path):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            video_dict[f.split('.')[0]] = os.path.join(root,f)

def get_json(vname):
    json_path = anno_path + r'\\' + vname + ".json"
    # keyframes_path = rawframe_path + vname + r"\\"
    # # The image is loaded to get the total keyframes under the file and the image H W to normalize coordinates

    # img_dir = os.listdir(keyframes_path)
    # img_nums = len(img_dir)
    # img_0 = img_dir[0]  # The H and W of the same video frame are the same
    # name = img_0.split('_')[0]   # Get picture name
    # name = vname
    # img = cv.imread(keyframes_path + img_0)

    # height = img.shape[0]
    # width = img.shape[1]
    # 读入视频
    cap = cv.VideoCapture(video_dict[vname])

    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
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

                person_id = int(v['av']['1'])
                action_ids = v['av']['3'].split(',')  # Get action ID
                for action_id in action_ids:
                    rows.append([str(vname), t, x1, y1, x2, y2, int(action_id)+1, person_id])
                # print(name, t, x1, y1, x2, y2, id)

if __name__ == '__main__':
    get_video(video_path)

    for root, dirs, files in os.walk(anno_path):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            #print(f)
            # print(f.split('.')[0])
            get_json(f.split('.')[0])
    # Create csv
    csvFile = open(output_path, "w", encoding="gbk")
    CSVwriter = csv.writer(csvFile, lineterminator='\n')
    for row in rows:
        CSVwriter.writerow(row)
    csvFile.close()
    ###统计各类标注数
    action_class = {'0': 'Standing',
                    '1': 'Walking',
                    '2': 'Running',
                    '3': 'BendingDown',
                    '4': 'FallingDown',
                    '5': 'Jumping',
                    '6': 'Squating',
                    '7': 'Sitting',
                    '8': 'Lying',
                    '9': 'Talking',
                    '10': 'Fighting',
                    '11': 'PlayingWithPhone',
                    '12': 'Kicking',
                    '13': 'ClimbingUp',
                    '14': 'Carrying',
                    '15': 'CallingUp',
                    '16': 'Eating',
                    '17': 'Drinking',
                    '18': 'Smoking'}
    total_dic = {}
    file = open(os.path.join(os.path.dirname(output_path), 'train_count.txt'), 'w')
    for row in rows:
        if action_class[str(row[6]-1)] in total_dic.keys():
            total_dic[action_class[str(row[6]-1)]]+=1
        else:
            total_dic[action_class[str(row[6] - 1)]] = 1
    for key, val in total_dic.items():
        file.write(key + ": " + str(val) + '\n')
        print(key + ": " + str(val))
    file.write("total: " + str(len(rows)) + '\n')
    print("total: " + str(len(rows)))
    file.close()