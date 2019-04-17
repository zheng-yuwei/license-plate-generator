# -*- coding: utf-8 -*-
"""
Created on 2019/4/17
File generate_lic_plt_no
@author:ZhengYuwei
功能：
定制不同类型车牌的车牌号规则，生成指定数量的车牌号
"""
import numpy as np
from license_plate_elements import LicensePlateElements
np.random.seed(0)


class LicensePlateNoGenerator(object):
    """ 随机生成车牌号和类型 """
    # 数字和英文字母列表
    numerals = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                'U', 'V', 'W', 'X', 'Y', 'Z']
    
    def __init__(self, plate_type):
        """ 初始化随机生成的比例，用于后续的随机生成方法中
        :param plate_type: 需要生成的车牌类型
        """
        if plate_type not in LicensePlateElements.plate_type_enum.keys():
            print('车牌类型指定错误，请参考license_plate_elements,py里的plate_type_enum变量！')
            self.plate_type = None
            return
        # 车牌类型
        self.plate_type = plate_type
        # 车牌号元素对象
        self.elements = LicensePlateElements()
    
    def generate_license_plate_numbers(self, num):
        """ 生成指定数量的车牌号
        :param num: 数量
        :return: 车牌号及对应label
        """
        license_plate_numbers = None
        # 蓝色底牌、黄色底牌 车牌号为标准车牌规则
        if self.plate_type in ['single_blue', 'single_yellow']:
            license_plate_numbers = self.generate_standard_license_no(num)
        # 小型新能源车牌号规则
        if self.plate_type == 'small_new_energy':
            license_plate_numbers = self.generate_small_new_energy_license_no(num)
        # 大型新能源车牌号规则
        if self.plate_type == 'big_new_energy':
            pass
        # 警车车牌号规则
        if self.plate_type == 'police':
            pass
        # 军区车车牌号规则
        if self.plate_type == 'single_army':
            pass
        # 香港车牌号规则
        if self.plate_type == 'hk':
            pass
        # 澳门车牌号规则
        if self.plate_type == 'macau':
            pass
        # 黑色底牌车牌号规则
        if self.plate_type == 'single_black':
            pass
        
        return license_plate_numbers
    
    def generate_standard_license_no(self, num):
        """ 生成蓝色、黄色等标准规则车牌号
        :param num: 生成车牌的数量
        :return: 生成的车牌号列表
        """
        # 针对车牌的每一位，随机采样
        license_chars = list()
        for char_index in range(7):
            # 对应车牌位上限制的字符范围
            char_range = self.elements.get_chars_sorted_by_label(char_index)
            if char_index == 0:
                char_range = char_range[:31]  # 第一位排除掉‘军’和‘使’
            elif char_index == 1:
                # 第二位的范围还和省份相关，这里没考虑
                char_range = char_range[:24]  # 第二位排除数字
            elif char_index == 6:
                char_range = char_range[:34]  # 第六位排除‘学’、‘警’等特殊字符
            
            license_chars.append(np.random.choice(a=char_range, size=num, replace=True))
    
        # 取每一位，组成7位车牌
        license_plate_numbers = [list(_) for _ in zip(*license_chars)]
        # 在后五位编码可以出现字母，但不能超过两个
        for i, lic_no in enumerate(license_plate_numbers):
            # 找出后5位中英文字母的位置
            alphabet_loc = list()
            for loc in range(2, 7):
                if lic_no[loc] in LicensePlateNoGenerator.alphabet:
                    alphabet_loc.append(loc)
            # 字母数多于两个的，随机保留2个（这样会导致车牌中2位字母数的车牌比较多）
            if len(alphabet_loc) > 2:
                allow = np.random.choice(a=alphabet_loc, size=2, replace=False)
                alphabet_loc.remove(allow[0])
                alphabet_loc.remove(allow[1])
        
                # 多出来的字母，替换为数字
                new_nos = np.random.choice(a=LicensePlateNoGenerator.numerals, size=len(alphabet_loc), replace=True)
                for j, loc in enumerate(alphabet_loc):
                    lic_no[loc] = new_nos[j]
        
        license_plate_numbers = [''.join(_) for _ in license_plate_numbers]
        return license_plate_numbers

    def generate_small_new_energy_license_no(self, num):
        """ 生成小型新能源车牌号
        :param num: 生成车牌的数量
        :return: 生成的车牌号列表
        """
        # 针对车牌的每一位，随机采样
        license_chars = list()
        for char_index in range(8):
            char_range = self.elements.get_chars_sorted_by_label(char_index)
            # 对应车牌位上限制的字符范围
            if char_index == 0:
                char_range = char_range[:31]  # 排除掉‘军’和‘使’
            elif char_index == 1:
                # 第二位的范围还和省份相关，这里没考虑
                char_range = char_range[:24]  # 第二位排除数字
            elif char_index == 2:
                char_range = ['D', 'F']  # 小型新能源第3位为D或F
            elif char_index == 3:
                # 该位规则符合取值范围
                pass
            else:
                char_range = LicensePlateNoGenerator.numerals  # 小型新能源后4位必须用数值
                
            license_chars.append(np.random.choice(a=char_range, size=num, replace=True))
            
        # 取每一位，组成8位车牌
        license_plate_numbers = [''.join(_) for _ in zip(*license_chars)]
        return license_plate_numbers
