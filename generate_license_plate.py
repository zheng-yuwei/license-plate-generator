# -*- coding: utf-8 -*-
"""
Created on 2019/4/17
File generate_license_plate
@author:ZhengYuwei
1. 产生车牌号：generate_license_plate_number
    1.1 定义车牌号中每一位车牌元素：license_plate_elements
    2.1 产生车牌号标签：针对特定类型的车牌，从车牌元素中选择元素组成车牌号
2. 产生车牌图片：generate_license_plate_image
    2.1 为车牌号产生车牌号图形：generate_chars_image
    2.2 加车牌类型底牌
3. 加扰动元素进行数据增强： augment_image
4. 保存图片
"""
import cv2
import os
import numpy as np
from generate_license_plate_number import LicensePlateNoGenerator
from generate_license_plate_image import LicensePlateImageGenerator
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
        # 生成车牌号
        license_plate_no_generator = LicensePlateNoGenerator(plate_type)
        plate_nums = license_plate_no_generator.generate_license_plate_numbers(batch_size)
        # 生成车牌
        license_plate_image_generator = LicensePlateImageGenerator(plate_type)
        plate_images = license_plate_image_generator.generate_license_plate_image(plate_nums)
        # 数据增强，并保存
        save_path = os.path.join(save_path, plate_type)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        prefix_len = len(str(int(batch_size)))  # 图片前缀位数
        augmentation = ImageAugmentation()
        for index, plate_image in enumerate(plate_images):
            image_name = str(index).zfill(prefix_len) + '_' + plate_nums[index] + '.jpg'
            image_path = os.path.join(save_path, image_name)
            cv2.imencode('.jpg', augmentation.augment(plate_image))[1].tofile(image_path)
            
        return plate_images
    
    
if __name__ == '__main__':
    LicensePlateGenerator.generate_license_plate_images('single_blue',
                                                        batch_size=10,
                                                        save_path=os.path.join(os.getcwd(), 'plate_images'))
    LicensePlateGenerator.generate_license_plate_images('single_yellow',
                                                        batch_size=10,
                                                        save_path=os.path.join(os.getcwd(), 'plate_images'))
    LicensePlateGenerator.generate_license_plate_images('small_new_energy',
                                                        batch_size=10,
                                                        save_path=os.path.join(os.getcwd(), 'plate_images'))
