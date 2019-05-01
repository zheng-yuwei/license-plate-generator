# -*- coding: utf-8 -*-
"""
Created on 2019/4/17
File generate_template_image
@author:ZhengYuwei
"""
import cv2


class LicensePlateImageGenerator(object):
    """ 根据车牌类型和车牌号，生成车牌图片 """
    single_blue_plate_bg = './images/single_blue1.bmp'
    small_new_energy_plate_bg = './images/small_new_energy.jpg'
    single_yellow1_plate_bg = './images/single_yellow1.bmp'
    police1_plate_bg = './images/police1.bmp'
    
    def __init__(self, plate_type):
        """ 初始化定义车牌类型，以及不同类型的车牌底牌图片 """
        self.plate_type = plate_type
        
        if plate_type == 'single_blue':
            plate_image = cv2.imread(LicensePlateImageGenerator.single_blue_plate_bg)
        elif plate_type == 'small_new_energy':
            plate_image = cv2.imread(LicensePlateImageGenerator.small_new_energy_plate_bg)
        elif plate_type == 'single_yellow':
            plate_image = cv2.imread(LicensePlateImageGenerator.single_yellow1_plate_bg)
        elif plate_type == 'police':
            plate_image = cv2.imread(LicensePlateImageGenerator.police1_plate_bg)
        else:
            raise ValueError('该类型车牌目前功能尚未完成！')
            
        self.bg = plate_image
    
    def generate_template_image(self, width, height):
        """ 根据车牌类型，生成对应的车牌底牌
        :param width: 模板宽度
        :param height: 模板高度
        :return:
        """
        return cv2.resize(self.bg, (width, height))
