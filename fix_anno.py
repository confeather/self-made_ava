import json
import cv2 as cv
import os
import csv

anno_path = r"C:\dataset\anno_train\\"
output_path = r"C:\dataset\anno_high\\"

rows = []

def change_json(vname):
    json_path = anno_path + vname + ".json"
    with open(json_path) as f:
        data = json.load(f)
        #置换1和3
        attr = data['attribute']
        tmp = attr['1']
        tmp['type'] = 2
        if '3' in attr.keys():
            attr['1'] = attr['3']
        else:
            attr['1'] = dict(aname='id', type=4, options={'0': '0',
                                                          '1': '1',
                                                          '2': '2',
                                                          '3': '3'},
                             default_option_id='0',
                             anchor_id='FILE1_Z0_XY1')
        attr['3'] = tmp

        img_data = data['metadata']  # The desired coordinates and action ID are under the dictionary
        # print(img_data)
        # print(len(img_data))
        # print(img_data.items())

        for i, (k, v) in enumerate(img_data.items()):
            #if 'score' in v.keys():  # len(img_data) - img_numbers。 Remove useless data
            if '1' in v['av'].keys():
                action_id = v['av']['1']  # Get action ID
                person_id = '0'
                if "3" in v['av'].keys():
                    person_id = v['av']['3']
                # 置换av标签
                v['av']['1'] = person_id
                v['av']['3'] = action_id
        file = open(os.path.join(os.path.dirname(output_path), vname + ".json"), 'w')
        json.dump(data,file)
        file.close()

def fix_timetamp(vname):
    json_path = anno_path + vname + ".json"
    with open(json_path) as f:
        data = json.load(f)

        cur_data = dict()
        img_data = data['metadata']  # The desired coordinates and action ID are under the dictionary

        for i, (k, v) in enumerate(img_data.items()):
            if v['vid'] == '31' or v['vid'] == '61' or v['vid'] == '91':
                cur_data.update({k: v})
        data['metadata'] = cur_data
        file = open(os.path.join(os.path.dirname(output_path), vname + ".json"), 'w')
        json.dump(data, file)
        file.close()

if __name__ == '__main__':
    for root, dirs, files in os.walk(anno_path):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            #print(f)
            #change_json(f.split('.')[0])
            fix_timetamp(f.split('.')[0])
