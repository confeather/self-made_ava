'''
批量提取视频的所有帧
'''
import os
import cv2
import argparse
from torch._C import Size
#存放视频的地址
videos_src_path = r'C:\dataset\custom_ava\talk01.avi'
#videos_src_path = r'C:\dataset\custom_ava'

#存放图片的地址
videos_save_path = r'C:\dataset\rawframe'

'''统一高度'''
H = 240

def parse_args():
    parser = argparse.ArgumentParser(description='get video frames')
    parser.add_argument(
        '--input',
        nargs='+',
        default=videos_src_path,
        help='A list of space separated input videos'
    )
    parser.add_argument('--output', default= videos_save_path, help='output directory')
    parser.add_argument('--height', default= H, help='output image height')
    parser.add_argument('--fps', default=30, help='input video fps')
    parser.add_argument('--time', default=4, help='input video duration seconds')
    args = parser.parse_args()
    return args

def get_frames(video_name):
    # 获取每个视频的名称
    each_video_name, _ = video_name.split('.')
    # 创建目录，来保存图片帧
    if os.path.exists(videos_save_path + r'/' + each_video_name) == False:
        os.mkdir(videos_save_path + r'/' + each_video_name)
    # 获取保存图片的完整路径，每个视频的图片帧存在以视频名为文件名的文件夹中
    each_video_save_full_path = os.path.join(videos_save_path, each_video_name) + r'/'
    # 获取每个视频的完整路径
    if os.path.isfile(args.input):
        each_video_full_path = os.path.join(os.path.dirname(args.input), video_name)
    else:
        each_video_full_path = os.path.join(args.input, video_name)
    # 读入视频
    cap = cv2.VideoCapture(each_video_full_path)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    frame_count = 1
    success = True
    while (success) and frame_count <= args.fps * args.time:
        # 提取视频帧，success为是否成功获取视频帧（true/false），第二个返回值为返回的视频帧
        success, frame = cap.read()
        if success == True:
            # 裁剪
            scale = height / args.height
            size = (int(width / scale), args.height)
            frame = cv2.resize(frame, size)
            # 存储视频帧
            cv2.imwrite(each_video_save_full_path + "img_" + "%05d.jpg" % frame_count, frame)
        frame_count = frame_count + 1


if __name__ == '__main__':
    args = parse_args()
    if os.path.isfile(args.input):
        get_frames(os.path.basename(args.input))
    else:
        # 返回videos_src_path路径下包含的文件或文件夹名字的列表（所有视频的文件名），按字母顺序排序
        videos = os.listdir(args.input)
        for each_video in videos:
            get_frames(each_video)
