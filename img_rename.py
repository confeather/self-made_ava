import os

def rename(root,f):
    num = int(f.split('.')[0][-4:])
    # print(root + "img_" + "%05d" % num + ".jpg")
    os.rename(root + f, root + "img_" + "%05d" % num + ".jpg")


for root, dirs, files in os.walk(r"C:\Users\63147\Desktop\self-made_ava_dataset_tool-master\rawframe\\stand01\\"):
    # root 表示当前正在访问的文件夹路径
    # dirs 表示该文件夹下的子目录名list
    # files 表示该文件夹下的文件list
    # 遍历文件
    #print(dirs)
    for f in files:
        rename(root,f)
        # print(f)