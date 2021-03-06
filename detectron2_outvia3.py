import argparse
import glob
import cv2
import mmcv
import os
from mmdet.apis import inference_detector, init_detector
import numpy as np
from collections import defaultdict
from via3_tool import Via3Json
from tqdm import tqdm
from colorama import Fore

input_imgs = [r'E:\dataset\videos_frame\*\*']
output_dir = r'E:\dataset\videos_ann_prop'
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
default_index = '5'

def parse_args():
    parser = argparse.ArgumentParser(description='MMDetection video demo')
    parser.add_argument('--config',
                        default='faster_rcnn_r50_fpn_2x_coco.py',
                        help='Config file')
    parser.add_argument('--checkpoint',
                        default='faster_rcnn_r50_fpn_2x_coco_bbox_mAP-0.384_20200504_210434-a5d8aa15.pth',
                        help='Checkpoint file')
    parser.add_argument(
        '--input',
        default=input_imgs,
        nargs='+',
        help='A list of space separated input images; '
             'or a single glob pattern such as directory/*.jpg or  directory/*.mp4',
    )
    parser.add_argument('--gen_via3',
                        default=True,
                        action='store_true',
                        help='generate via3 files for images or videos.')
    parser.add_argument('--output',
                        default=output_dir,
                        help='output directory')
    parser.add_argument(
        '--device', default='cuda:0', help='Device used for inference')
    parser.add_argument(
        '--score-thr', type=float, default=0.8, help='Bbox score threshold')
    parser.add_argument('--out', type=str, help='Output video file')
    parser.add_argument('--show',
                        default=True,
                        action='store_true',
                        help='Show video')
    parser.add_argument(
        '--wait-time',
        type=float,
        default=1,
        help='The interval of show (s), 0 is block')
    parser.add_argument(
        '--default-action',
        type=str,
        default=default_index,
        help='The index of person action')

    args = parser.parse_args()
    return args


def process_image(model, image_path, output):
    results = inference_detector(model, image_path)
    return results[0]


def main():
    args = parse_args()
    assert args.out or args.show, \
        ('Please specify at least one operation (save/show the '
         'video) with the argument "--out" or "--show"')

    # args.input ['./Datasets/Interaction/images/train/*/*.jpg']
    # len(args.input) 821
    if len(args.input) == 1:
        # ?????????????????????train?????????2?????????
        args.input = glob.glob(os.path.expanduser(args.input[0]))
        args.input.sort()
        assert args.input, "The input path(s) was not found"

    # ?????????????????????
    model = init_detector(args.config, args.checkpoint, device=args.device)

    if len(args.input) == 1:
        # ?????????????????????
        args.input = glob.glob(os.path.expanduser(args.input[0]))
        assert args.input, "The input path(s) was not found"

    images_results_dict = defaultdict(list)
    # images_results_dict defaultdict(<class 'list'>, {})
    # videos_results_dict defaultdict(<class 'list'>, {})

    for file_path in tqdm(args.input, bar_format='{l_bar}%s{bar}%s{r_bar}' % (Fore.BLUE, Fore.RESET)):
        # file_path ./Datasets/Interaction/images/train/2/001.jpg
        # ????????????????????????
        extension = os.path.splitext(file_path)[-1]
        if extension in ['.png', '.jpg', '.bmp', 'tif', 'gif'] \
                and (int(os.path.basename(file_path).split('_')[1][:5]) == 31
                     or int(os.path.basename(file_path).split('_')[1][:5]) == 61):
            file_dir, file_name = os.path.split(file_path)
            results = process_image(model, file_path, args.output)
            # print(results)
            results = results[results[:, 4] > args.score_thr]
            # print(results)
            results[:, [2, 3]] = results[:, [2, 3]] - results[:, [0, 1]]
            # print(results[:, [2, 3]])
            # print(results)
            images_results_dict[file_dir].append((file_name, results))
            # images_results_dict defaultdict(<class 'list'>, {'./Datasets/Interaction/images/train/2': [('001.jpg', array([[401.9775    , 138.73132   , 307.38522   , 411.7107    ,0.99856526]], dtype=float32)), ('002.jpg', array([[401.1002   , 140.16426  , 308.95303  , 413.97455  ,   0.9984402]], dtype=float32)), ('003.jpg', array([[399.90347  , 140.76791  , 310.91885  , 423.98422  ,   0.9988949]], dtype=float32))]})
            # ????????????????????????????????????????????????????????????????????????????????????

        else:
            #print('???????????? {} ?????????????????? {}'.format(extension, file_path))
            continue
    for images_dir in images_results_dict:
        print("images_dir", images_dir)
        # images_dir ./Datasets/Interaction/images/train/2
        # images_dir ./Datasets/Interaction/images/train/3
        # ??????????????????????????????train??????????????????????????????????????????????????????????????????***_proposal.json???
        images_results = images_results_dict[images_dir]
        if args.output:
            json_path = os.path.join(args.output, os.path.basename(images_dir) + '_proposal.json')
        else:
            json_path = os.path.join(images_dir, os.path.basename(images_dir) + '_proposal.json')
        num_images = len(images_results)
        via3 = Via3Json(json_path, mode='dump')

        vid_list = list(map(str, range(1, num_images + 1)))
        via3.dumpPrejects(vid_list)

        via3.dumpConfigs()

        attributes_dict = {'1': dict(aname='id',type=4,options={'0': '0',
                                                                '1': '1',
                                                                '2': '2',
                                                                '3': '3',
                                                                '4': '4',
                                                                '5': '5',
                                                                '6': '6',
                                                                '7': '7',
                                                                '8': '8',
                                                                '9': '9',
                                                                '10': '10',
                                                                '11': '11'},
                                     default_option_id='0',
                                     anchor_id='FILE1_Z0_XY1'),
                           '2': dict(aname='modify', type=4, options={'0': 'False',
                                                                      '1': 'Ture'},
                                     default_option_id='0',
                                     anchor_id='FILE1_Z0_XY0'),
                           '3': dict(aname='person', type=2, options=action_class,
                                     default_option_id='0',
                                     anchor_id='FILE1_Z0_XY1')
                           }

        via3.dumpAttributes(attributes_dict)

        files_dict, metadatas_dict = {}, {}
        for image_id, (file_name, results) in enumerate(images_results, 1):
            files_dict[str(image_id)] = dict(fname=file_name, type=2)
            for vid, result in enumerate(results, 1):
                metadata_dict = dict(vid=str(image_id),
                                     xy=[2, float(result[0]), float(result[1]), float(result[2]), float(result[3])],
                                     av={'1': '0', '3': args.default_action}, score=[round(float(result[4]), 6)])
                # xy defines spatial location (e.g. bounding box)
                # av defines the value of each attribute for this (z, xy) combination
                #    the value for attribute-id="1" is one of its option with id "1" (i.e. Activity = Break Egg)
                # metadata_dict = dict(vid=vid, xy=[2], av={'1':'0'})
                metadatas_dict['image{}_{}'.format(image_id, vid)] = metadata_dict
        via3.dumpFiles(files_dict)
        via3.dumpMetedatas(metadatas_dict)

        views_dict = {}
        for i, vid in enumerate(vid_list, 1):
            views_dict[vid] = defaultdict(list)
            views_dict[vid]['fid_list'].append(str(i))
        via3.dumpViews(views_dict)

        via3.dempJsonSave()


if __name__ == '__main__':
    main()
