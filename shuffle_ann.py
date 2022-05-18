from typing import Tuple
import random
import os
import shutil

def split(full_list, shuffle=False, ratio=0.2) -> Tuple[list,list]:
    n_total = len(full_list)
    offset = int(n_total * ratio)
    if n_total == 0 or offset < 1:
        return [], full_list
    if shuffle:
        random.shuffle(full_list)
    sublist_1 = full_list[:offset]
    sublist_2 = full_list[offset:]
    return sublist_1, sublist_2

if __name__ == '__main__':
    full_l = {}
    train_l = []
    val_l = []
    ann_path = r'E:\dataset\videos_ann'
    val_path = r'E:\dataset\videos_ann_val'
    train_path = r'E:\dataset\videos_ann_train'
    for root, dirs, files in os.walk(ann_path):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            if root not in full_l.keys():
                full_l[root] = [os.path.join(root, f)]
            else:
                full_l[root].append(os.path.join(root, f))
    for item in full_l.values():
        # print(len(item))
        v_l, t_l = split(item, True)
        val_l.extend(v_l)
        train_l.extend(t_l)

    for val in val_l:
        shutil.copyfile(val,os.path.join(val_path,
                                         os.path.basename(val)))
    for train in train_l:
        shutil.copyfile(train,os.path.join(train_path,
                                         os.path.basename(train)))
