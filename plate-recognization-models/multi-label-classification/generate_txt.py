# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
import random
import datetime
from file_tools import FileTools

sys.path.insert(0, '..')

from license_plate_elements import LicensePlateElements

# 车牌图片所在根目录
#plate_images_root_dir = '/data1/annotation/car_plate/for_train/ocr/plate_images_0420/'
plate_images_root_dir = '/home/data_160/data1/license_plate/license-plate-generator/plate_images/'
# 所有车牌图片路径list
images_path = FileTools.search_file(plate_images_root_dir, '.jpg')

print('开始产生标签列表...')
# 产生4个数据集：all，train，test，validate = 1:0.8:0.1:0.1
all_num = len(images_path)
random.shuffle(images_path)

# 生成标签数据
elements = LicensePlateElements()
char8_labels = len(elements.get_char_label(7)) - 1
lines = list()
line = [None] * 10
for index, image_path in enumerate(images_path):
    file_name = os.path.basename(image_path)
    plate_no = os.path.splitext(file_name)[0].split('_')[1]  # 00000001_xxxxxx.jpg
    # print(plate_no)
    # relative_path char1 char2 char3 char4 char5 char6 char7 char8 char_num
    line[0] = image_path[len(plate_images_root_dir):]
    if len(plate_no) == 7:
        line[8] = str(random.randint(0, char8_labels))  # 第8位随机选择
        line[9] = str(elements.char_number_enum.get('7'))
    else:
        line[8] = str(elements.get_label(7, plate_no[7]))
        line[9] = str(elements.char_number_enum.get('8'))
    for i in range(7):
        line[i+1] = str(elements.get_label(i, plate_no[i]))
    
    lines.append([' '.join(line), '\n'])
    if (index + 1) % 10000 == 0:
        print('{}: {}/{} done...'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), index + 1, all_num))

# print(lines)
print('生成全量数据标签文件...')
all_txt = 'all.txt'
with open(all_txt, 'w+') as file:
    for line in lines:
        file.writelines(line)

print('生成训练数据标签文件...')
train_txt = 'train.txt'
with open(train_txt, 'w+') as file:
    for line in lines[(int(all_num * 0.1)+int(all_num * 0.1)):all_num]:
        file.writelines(line)

print('生成测试数据标签文件...')
test_txt = 'test.txt'
with open(test_txt, 'w+') as file:
    for line in lines[:int(all_num * 0.1)]:
        file.writelines(line)

print('生成验证数据标签文件...')
validate_txt = 'validate.txt'
with open(validate_txt, 'w+') as file:
    for line in lines[int(all_num * 0.1):(int(all_num * 0.1)+int(all_num * 0.1))]:
        file.writelines(line)
