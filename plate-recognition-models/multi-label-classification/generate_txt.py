# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
import random
import datetime
from file_tools import FileTools

sys.path.insert(0, '..')

from license_plate_elements import LicensePlateElements

# 所有车牌号图片的根目录
plate_images_root_dir = '/home/data_160/data1/license_plate/license-plate-generator/new_plate_images/'

########################################################################################################
#
#   产生7位车牌号数据的lmdb数据集
#
########################################################################################################
# 7位车牌号图片在根目录下的相对位置
plate7_images_root_dir = [plate_images_root_dir + 'single_blue/', 
                          plate_images_root_dir + 'single_yellow/']
# 所有车牌图片路径list
images7_path = list()
for path in plate7_images_root_dir:
    print('搜索路径', path)
    images7_path.extend(FileTools.search_file(path, '.jpg'))

    
# 生成标签数据（其中图片路径是相对根目录的路径）
print('开始产生7位车牌号标签列表...')

all_num = len(images7_path)
random.shuffle(images7_path)

elements = LicensePlateElements()
char8_labels = len(elements.get_char_label(7)) - 1
lines = list()
line = [None] * 10
for index, image_path in enumerate(images7_path):
    file_name = os.path.basename(image_path)
    plate_no = os.path.splitext(file_name)[0].split('_')[1]  # 00000001_xxxxxxxx.jpg
    # print(plate_no)
    # relative_path char1 char2 char3 char4 char5 char6 char7 char8 char_num
    line[0] = image_path[len(plate_images_root_dir):]
    for i in range(7):
        line[i+1] = str(elements.get_label(i, plate_no[i]))
    line[8] = str(random.randint(0, char8_labels))  # 第8位随机选择
    line[9] = str(elements.char_number_enum.get('8'))
    
    lines.append([' '.join(line), '\n'])
    if (index + 1) % 10000 == 0:
        print('{}: {}/{} done...'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), index + 1, all_num))

# print(lines)
if not os.path.exists('multi_label_lmdb'):
    os.makedirs('multi_label_lmdb')
    
print('生成全量数据标签文件...')
all_txt = 'multi_label_lmdb/all7.txt'
with open(all_txt, 'w+') as file:
    for line in lines:
        file.writelines(line)


########################################################################################################
#
#   产生8位车牌号数据的lmdb数据集
#
########################################################################################################
# 8位车牌号图片在根目录下的相对位置
plate8_images_root_dir = [plate_images_root_dir + 'small_new_energy/',]
# 所有车牌图片路径list
images8_path = list()
for path in plate8_images_root_dir:
    print('搜索路径', path)
    images8_path.extend(FileTools.search_file(path, '.jpg'))

# 生成标签数据
print('开始产生8位车牌号标签列表...')

all_num = len(images8_path)
random.shuffle(images8_path)

elements = LicensePlateElements()
lines = list()
line = [None] * 10
for index, image_path in enumerate(images8_path):
    file_name = os.path.basename(image_path)
    plate_no = os.path.splitext(file_name)[0].split('_')[1]  # 00000001_xxxxxxxx.jpg
    # print(plate_no)
    # relative_path char1 char2 char3 char4 char5 char6 char7 char8 char_num
    line[0] = image_path[len(plate_images_root_dir):]
    for i in range(8):
        line[i+1] = str(elements.get_label(i, plate_no[i]))
    line[9] = str(elements.char_number_enum.get('8'))
    
    lines.append([' '.join(line), '\n'])
    if (index + 1) % 10000 == 0:
        print('{}: {}/{} done...'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), index + 1, all_num))

# print(lines)
if not os.path.exists('multi_label_lmdb'):
    os.makedirs('multi_label_lmdb')
    
print('生成全量数据标签文件...')
all_txt = 'multi_label_lmdb/all8.txt'
with open(all_txt, 'w+') as file:
    for line in lines:
        file.writelines(line)


########################################################################################################
#
#   产生7位和8位车牌号混合数据的lmdb数据集
#
########################################################################################################
# 7位和8位车牌号混合图片数据所在根目录
plate_images_root_dir = [plate_images_root_dir,]
# 所有车牌图片路径list
images_path = list()
images_path.extend(images7_path)
images_path.extend(images8_path)
print('开始产生7位和8位车牌号标签列表...')

all_num = len(images_path)
random.shuffle(images_path)

# 生成标签数据
elements = LicensePlateElements()
char8_labels = len(elements.get_char_label(7)) - 1
lines = list()
line = [None] * 10
for index, image_path in enumerate(images_path):
    file_name = os.path.basename(image_path)
    plate_no = os.path.splitext(file_name)[0].split('_')[1]  # 00000001_xxxxxxx.jpg
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
# 产生4个数据集：all，train，test，validate = 1:0.8:0.1:0.1
if not os.path.exists('multi_label_lmdb'):
    os.makedirs('multi_label_lmdb')
    
print('生成全量数据标签文件...')
all_txt = 'multi_label_lmdb/all.txt'
with open(all_txt, 'w+') as file:
    for line in lines:
        file.writelines(line)

print('生成训练数据标签文件...')
train_txt = 'multi_label_lmdb/train.txt'
with open(train_txt, 'w+') as file:
    for line in lines[(int(all_num * 0.1)+int(all_num * 0.1)):all_num]:
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




