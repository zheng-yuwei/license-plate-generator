# -*- coding: utf-8 -*-
"""
Created on 2019/4/17
File generate_chars_image
@author:ZhengYuwei
功能：生成车牌号字符图像：背景为白色，字体为黑色
"""
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np
import cv2


class CharsImageGenerator(object):
    """ 生成字符图像：背景为白色，字体为黑色 """
    # 数字和英文字母列表
    numerals = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                'U', 'V', 'W', 'X', 'Y', 'Z']
    
    def __init__(self, plate_type):
        """ 一些参数的初始化
        :param plate_type: 需要生成的车牌类型
        """
        self.plate_type = plate_type
        # 字符图片参数
        self.font_ch = ImageFont.truetype("./font/platech.ttf", 180, 0)  # 中文字体格式
        self.font_en = ImageFont.truetype('./font/platechar.ttf', 240, 0)  # 英文字体格式
        self.bg_color = (255, 255, 255)  # 车牌背景颜色
        self.fg_color = (0, 0, 0)  # 车牌号的字体颜色

        self.plate_height = 280  # 车牌高度
        self.left_offset = 32  # 车牌号左边第一个字符的偏移量
        self.height_offset = 10  # 高度方向的偏移量
        self.char_height = 180  # 字符高度
        self.chinese_original_width = 180  # 中文字符原始宽度
        self.english_original_width = 90  # 非中文字符原始宽度
        if plate_type in ['single_blue', 'single_yellow']:
            self.char_num = 7
            self.char_width = 90  # 字符校正后的宽度
            self.plate_width = 880  # 车牌的宽度
            self.char_interval = 24  # 字符间的间隔
            self.point_size = 20  # 第2个字符与第三个字符间有一个点，该点的尺寸
        elif plate_type == 'small_new_energy':
            self.char_num = 8
            self.first_char_width = 90  # 第一个字符校正后的宽度
            self.char_width = 86  # 其余字符校正后宽度
            self.plate_width = 960  # 车牌的宽度
            self.char_interval = 18  # 字符间的间隔
            self.point_size = 62  # 第2个字符与第三个字符间有一个点，该点的尺寸
        else:
            raise ValueError('目前不支持该类型车牌！')
    
    def generate_images(self, plate_nums):
        """ 根据车牌号列表，生成车牌号图片：背景为白色，字体为黑色
        :param plate_nums: 车牌号
        :return:
        """
        if self.plate_type in ['single_blue', 'single_yellow', ]:
            plate_images = self.generate_440_140_plate(plate_nums)
        elif self.plate_type == 'small_new_energy':
            plate_images = self.generate_480_140_plate(plate_nums)
        else:
            raise ValueError('该类型车牌目前功能尚未完成！')
        
        return plate_images
    
    def generate_440_140_plate(self, plate_nums):
        """ 生成440 * 140尺寸的7位车牌字符图片
        :param plate_nums:
        :return:
        """
        plate_images = list()
        for plate_num in plate_nums:
            # 创建空白车牌号图片
            img = np.array(Image.new("RGB", (self.plate_width, self.plate_height), self.bg_color))
            # 每个字符的x轴起始、终止位置
            char_width_start = self.left_offset
            char_width_end = char_width_start + self.char_width
            img[:, char_width_start:char_width_end] = self.generate_char_image(plate_num[0])

            char_width_start = char_width_end + self.char_interval
            char_width_end = char_width_start + self.char_width
            img[:, char_width_start:char_width_end] = self.generate_char_image(plate_num[1])
            # 隔开特殊间隙，继续添加车牌的后续车牌号
            char_width_end = char_width_end + self.point_size + self.char_interval
            for i in range(2, len(plate_num)):
                char_width_start = char_width_end + self.char_interval
                char_width_end = char_width_start + self.char_width
                img[:, char_width_start:char_width_end] = self.generate_char_image(plate_num[i])
                
            plate_images.append(img)
        return plate_images
    
    def generate_480_140_plate(self, plate_nums):
        """ 生成480 * 140尺寸的8位车牌字符图片
        :param plate_nums:
        :return:
        """
        plate_images = list()
        for plate_num in plate_nums:
            # 创建空白车牌号图片
            img = np.array(Image.new("RGB", (self.plate_width, self.plate_height), self.bg_color))
            # 第一个字符有差异，8位车牌第一个字符是45宽，后续是43宽
            char_width = self.char_width
            self.char_width = self.first_char_width
            # 每个字符的x轴起始、终止位置
            char_width_start = self.left_offset
            char_width_end = char_width_start + self.char_width
            img[:, char_width_start:char_width_end] = self.generate_char_image(plate_num[0])
            self.char_width = char_width
    
            char_width_start = char_width_end + self.char_interval
            char_width_end = char_width_start + self.char_width
            img[:, char_width_start:char_width_end] = self.generate_char_image(plate_num[1])
            # 隔开特殊间隙，继续添加车牌的后续车牌号
            char_width_end = char_width_end + self.point_size + self.char_interval
            for i in range(2, len(plate_num)):
                char_width_start = char_width_end + self.char_interval
                char_width_end = char_width_start + self.char_width
                img[:, char_width_start:char_width_end] = self.generate_char_image(plate_num[i])
    
            plate_images.append(img)
        return plate_images
    
    def generate_char_image(self, char):
        """ 生成字符图片
        :param char: 字符
        :return:
        """
        # 根据是否中文字符，选择生成模式
        if char in CharsImageGenerator.numerals or char in CharsImageGenerator.alphabet:
            img = self.generate_en_char_image(char)
        else:
            img = self.generate_ch_char_image(char)
        return img
    
    def generate_ch_char_image(self, char):
        """ 生成中文字符图片
        :param char: 待生成的中文字符
        """
        img = Image.new("RGB", (self.chinese_original_width, self.plate_height), self.bg_color)
        ImageDraw.Draw(img).text((0, self.height_offset), char, self.fg_color, font=self.font_ch)
        img = img.resize((self.char_width, self.plate_height))
        return np.array(img)
    
    def generate_en_char_image(self, char):
        """" 生成英文字符图片
        :param char: 待生成的英文字符
        """
        img = Image.new("RGB", (self.english_original_width, self.plate_height), self.bg_color)
        ImageDraw.Draw(img).text((0, self.height_offset), char, self.fg_color, font=self.font_en)
        img = img.resize((self.char_width, self.plate_height))
        return np.array(img)
