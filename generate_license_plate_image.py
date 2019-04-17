# -*- coding: utf-8 -*-
"""
Created on 2019/4/17
File generate_license_plate_image
@author:ZhengYuwei
"""
import cv2
from generate_chars_image import CharsImageGenerator


class LicensePlateImageGenerator(object):
    """ 根据车牌类型和车牌号，生成车牌图片 """
    single_blue_plate_bg = './images/single_blue1.bmp'
    small_new_energy_plate_bg = './images/small_new_energy.jpg'
    single_yellow1_plate_bg = './images/single_yellow1.bmp'
    
    def __init__(self, plate_type):
        """ 初始化定义车牌类型，以及不同类型的车牌底牌图片 """
        self.plate_type = plate_type
        
        plate_image = None
        if plate_type == 'single_blue':
            plate_image = cv2.imread(LicensePlateImageGenerator.single_blue_plate_bg)
        elif plate_type == 'small_new_energy':
            plate_image = cv2.imread(LicensePlateImageGenerator.small_new_energy_plate_bg)
        elif plate_type == 'single_yellow':
            plate_image = cv2.imread(LicensePlateImageGenerator.single_yellow1_plate_bg)
        else:
            print('该类型车牌目前功能尚未完成！')

        self.chars_image_generator = CharsImageGenerator(plate_type)
        self.bg = cv2.resize(plate_image, (self.chars_image_generator.plate_width,
                                           self.chars_image_generator.plate_height))
    
    def generate_license_plate_image(self, plate_nums):
        """ 根据车牌列表，生成车牌图片
        :param plate_nums: 车牌号列表
        :return:
        """
        # 获取车牌字符串图片列表
        images = self.chars_image_generator.generate_images(plate_nums)
        # 添加底牌
        for index, image in enumerate(images):
            image = cv2.bitwise_not(image)  # 将原来黑字置为白字符，而白底符置为黑底
            images[index] = cv2.bitwise_or(image, self.bg)
        return images
