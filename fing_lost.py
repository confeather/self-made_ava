import os


if __name__ == '__main__':
    video_path = r'E:\dataset\videos\CallingUp'
    anno_path = r'E:\dataset\videos_ann\call'
    l_v = []
    l_a = []
    for root, dirs, files in os.walk(anno_path):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            #print(f)
            l_a.append(f.split('.')[0])
    for root, dirs, files in os.walk(video_path):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            #print(f)
            l_v.append(f.split('.')[0])

    for n in l_a:
        if n in l_v:
            continue
        else:
            print(n)
