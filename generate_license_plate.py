# -*- coding: utf-8 -*-
"""
Created on 2019/4/17
File generate_license_plate
@author:ZhengYuwei
1. 产生车牌号：generate_license_plate_number
    1.1 定义车牌号中每一位车牌元素：license_plate_elements
    2.1 产生车牌号标签：针对特定类型的车牌，从车牌元素中选择元素组成车牌号
2 为车牌号产生车牌号图形：generate_chars_image
3. 产生车牌底牌图片：generate_plate_template
4. 加扰动元素进行数据增强，拼装底牌和车牌号图片： augment_image
4. 保存图片
"""
import cv2
import os
import sys
import datetime
from generate_license_plate_number import LicensePlateNoGenerator
from generate_chars_image import CharsImageGenerator
from generate_plate_template import LicensePlateImageGenerator
from augment_image import ImageAugmentation


class LicensePlateGenerator(object):
    
    @staticmethod
    def generate_license_plate_images(plate_type, batch_size, save_path):
        """ 生成特定数量的、指定车牌类型的车牌图片，并保存到指定目录下
        :param plate_type: 车牌类型
        :param batch_size: 车牌号数量
        :param save_path: txt文件根目录
        :return:
        """
        sys.stdout.write('\r>> 生成车牌号图片...')
        sys.stdout.flush()
        # 生成车牌号
        license_plate_no_generator = LicensePlateNoGenerator(plate_type)
        plate_nums = license_plate_no_generator.generate_license_plate_numbers(batch_size)
        # 生成车牌号图片：白底黑字
        chars_image_generator = CharsImageGenerator(plate_type)
        chars_images = chars_image_generator.generate_images(plate_nums)
        # 生成车牌底牌
        license_template_generator = LicensePlateImageGenerator(plate_type)
        template_image = license_template_generator.generate_template_image(chars_image_generator.plate_width,
                                                                            chars_image_generator.plate_height)
        # 数据增强及车牌字符颜色修正，并保存
        sys.stdout.write('\r>> 生成车牌图片...')
        sys.stdout.flush()
        augmentation = ImageAugmentation(plate_type, template_image)
        
        save_path = os.path.join(save_path, plate_type)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        prefix_len = len(str(int(batch_size)))  # 图片前缀位数
        global plate_height
        plate_width = int(chars_image_generator.plate_width * plate_height / chars_image_generator.plate_height)
        for index, char_image in enumerate(chars_images):
            image_name = str(index).zfill(prefix_len) + '_' + plate_nums[index] + '.jpg'
            image_path = os.path.join(save_path, image_name)
            image = augmentation.augment(char_image)
            image = cv2.resize(image, (plate_width, plate_height))
            cv2.imencode('.jpg', image)[1].tofile(image_path)
            if (index+1) % 100 == 0:
                sys.stdout.write('\r>> {} done...'.format(index + 1))
                sys.stdout.flush()
        return
    
    
if __name__ == '__main__':
    plate_height = 72
    mini_batch_size = 1000
    iter_times = 100
    sys.stdout.write('{}: total {} iterations ...\n'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                            iter_times))
    sys.stdout.flush()
    for i in range(iter_times):
        sys.stdout.write('\r{}: iter {}...\n'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), i))
        sys.stdout.flush()
        LicensePlateGenerator.generate_license_plate_images('single_blue',
                                                            batch_size=mini_batch_size,
                                                            save_path=os.path.join(os.getcwd(), 'plate_images'))
        LicensePlateGenerator.generate_license_plate_images('single_yellow',
                                                            batch_size=mini_batch_size,
                                                            save_path=os.path.join(os.getcwd(), 'plate_images'))
        LicensePlateGenerator.generate_license_plate_images('small_new_energy',
                                                            batch_size=mini_batch_size,
                                                            save_path=os.path.join(os.getcwd(), 'plate_images'))
    sys.stdout.write('\r{}: done...\n'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), i))
    sys.stdout.flush()
