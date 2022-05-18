import os
#存放视频的地址
videos_src_path = r'D:\download\Fall\office'


if __name__ == '__main__':
    for root, dirs, files in os.walk(videos_src_path):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            # print(f)
            # change_json(f.split('.')[0])
            n = f.replace(' ','')
            os.rename(os.path.join(videos_src_path,f),os.path.join(videos_src_path,'office_' + n.split('.')[0] + '.mp4'))
            #print(f.split('.')[0])
