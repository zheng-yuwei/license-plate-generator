# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
import random
import datetime
from file_tools import FileTools
sys.path.insert(0, '../../license-plate-generator')
from license_plate_elements import LicensePlateElements


# 所有车牌号图片的根目录
plate_images_root_dir = '/home/data_160/data3/smart_home/xiongxin-yuwei/plate_recognition/new_plate_images/'

blue_dir = [plate_images_root_dir + 'CCPD/blue', plate_images_root_dir + 'generate/blue']
yellow_dir = [plate_images_root_dir + 'generate/yellow']
green_dir = [plate_images_root_dir + 'generate/green', ]
white_dir = []
big_green_dir = []
black_dir = []

# 所有车牌图片路径list
blue_paths = list()
for path in blue_dir:
    print('搜索路径', path)
    blue_paths.extend(FileTools.search_file(path, '.jpg'))

yellow_paths = list()
for path in yellow_dir:
    print('搜索路径', path)
    yellow_paths.extend(FileTools.search_file(path, '.jpg'))

green_paths = list()
for path in green_dir:
    print('搜索路径', path)
    green_paths.extend(FileTools.search_file(path, '.jpg'))

white_paths = list()
for path in white_dir:
    print('搜索路径', path)
    white_paths.extend(FileTools.search_file(path, '.jpg'))

# 生成标签数据（其中图片路径是相对根目录的路径）
print('开始产生车牌号标签列表...')
plate_nums = (len(blue_paths), len(yellow_paths), len(green_paths), len(white_paths), )
print('blue, yellow, green, white:{}'.format(plate_nums))
elements = LicensePlateElements()
all_paths = (blue_paths, yellow_paths, green_paths, white_paths, )
types = (str(elements.plate_colors['blue']), str(elements.plate_colors['yellow']), 
         str(elements.plate_colors['green']), str(elements.plate_colors['white']), )
lines = list()
char8_labels = '-1'
plate7_type = str(elements.char_number_enum.get('7'))
plate8_type = str(elements.char_number_enum.get('8'))
line = [None] * 11
for path_index, paths in enumerate(all_paths):
    for image_index, image_path in enumerate(paths):
        plate_no = os.path.splitext(os.path.basename(image_path))[0].split('_')[-1]  # 00000001_xxxxxxxx.jpg
        # print(plate_no)
        # relative_path char1 char2 char3 char4 char5 char6 char7 char8 char_num plate_color
        line[0] = image_path[len(plate_images_root_dir):]
        if len(plate_no) == 7:
            line[8] = char8_labels  # 第8位标记为-1
            line[9] = plate7_type
        elif len(plate_no) == 8:
            line[8] = str(elements.get_label(7, plate_no[7]))
            line[9] = plate8_type
        else:
            print('Warn: checke ', image_path)
            continue
        for i in range(7):
            line[i+1] = str(elements.get_label(i, plate_no[i]))
        line[10] = types[path_index]

        lines.append([' '.join(line), '\n'])
        if (image_index + 1) % 10000 == 0:
            print('{}: {}/{} done...'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                             image_index + 1, plate_nums[path_index]))

random.shuffle(lines)
all_num = len(lines)
# print(all_num)
if not os.path.exists('multi_label_lmdb'):
    os.makedirs('multi_label_lmdb')
    
print('生成全量数据标签文件...')
all_txt = 'multi_label_lmdb/all.txt'
with open(all_txt, 'w+') as file:
    for line in lines:
        file.writelines(line)

print('生成测试数据标签文件...')
test_txt = 'multi_label_lmdb/test.txt'
with open(test_txt, 'w+') as file:
    for line in lines[:int(all_num * 0.1)]:
        file.writelines(line)

print('生成验证数据标签文件...')
validate_txt = 'multi_label_lmdb/validate.txt'
with open(validate_txt, 'w+') as file:
    for line in lines[int(all_num * 0.1):(int(all_num * 0.1)+int(all_num * 0.1))]:
        file.writelines(line)

print('生成训练数据标签文件...')
train_txt = 'multi_label_lmdb/train.txt'
with open(train_txt, 'w+') as file:
    for line in lines[(int(all_num * 0.1)+int(all_num * 0.1)):all_num]:
        file.writelines(line)
