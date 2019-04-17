# -*- coding: utf-8 -*-
"""
Created on 2019/4/17
File generate_char_image
@author:ZhengYuwei
@ref: https://github.com/huxiaoman7/mxnet-cnn-plate-recognition, @author Huxiaoman
"""
import cv2
import numpy as np
import math
import os


class ImageAugmentation(object):
    """ 一些图像增强操作操作: 透视变换、HSV变化、添加背景、高斯噪声、污渍 """
    
    def __init__(self):
        """ 一些图像增强参数的默认初值初始化 """
        # 透视变换
        self.angle = 60
        self.factor = 10
        # 色调，饱和度，亮度
        self.hue_keep = 0.8
        self.saturation_keep = 0.3
        self.value_keep = 0.2
        # 自然环境照片的路径列表
        self.env_data_paths = ImageAugmentation.search_file("background")
        # 高斯噪声level
        self.level = 1 + ImageAugmentation.rand_reduce(4)
        # 污渍
        self.smu = cv2.imread("images/smu.jpg")
    
    def angle_perspective_transfer(self, img, angle=None, max_angle=None):
        """ 添加按照指定角度进行投影映射畸变(右倾斜或左倾斜，最大倾斜角度self.angle一半）
        :param img: 输入图像的numpy
        :param angle: 图片投影的倾斜角度(正右倾，负左倾）
        :param max_angle: 图片倾斜的最大角度
        """
        if angle is None:
            angle = self.rand_reduce(self.angle) - self.angle / 2
        if max_angle is None:
            max_angle = self.angle / 2
            
        shape = img.shape
        size_src = [shape[1], shape[0]]
        # 计算图片进行最大角度倾斜后的尺寸
        size = (shape[1] + int(shape[0] * math.cos((float(max_angle) / 180) * math.pi)), shape[0])
        # 计算图片进行投影倾斜后的位置
        interval = abs(int(math.sin((float(angle) / 180) * math.pi) * shape[0]))
        # 源图像四个顶点坐标
        pts1 = np.float32([[0, 0], [0, size_src[1]], [size_src[0], 0], [size_src[0], size_src[1]]])
        # 目标图像上四个顶点的坐标
        if angle > 0:
            pts2 = np.float32([[interval, 0], [0, size[1]], [size[0], 0], [size[0] - interval, size_src[1]]])
        else:
            pts2 = np.float32([[0, 0], [interval, size[1]], [size[0] - interval, 0], [size[0], size_src[1]]])
        # 获取 3x3的投影映射/透视变换 矩阵
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        dst = cv2.warpPerspective(img, matrix, size)
        return dst
    
    @staticmethod
    def rand_reduce(val):
        return int(np.random.random() * val)
    
    def rand_perspective_transfer(self, img, factor=None, size=None):
        """ 添加投影映射畸变
        :param img: 输入图像的numpy
        :param factor: 畸变的参数
        :param size: 图片的目标尺寸，默认维持不变
        """
        if factor is None:
            factor = self.factor
        if size is None:
            size = (img.shape[1], img.shape[0])
        shape = size
        # 源图像四个顶点坐标
        pts1 = np.float32([[0, 0], [0, shape[0]], [shape[1], 0], [shape[1], shape[0]]])
        # 目标图像上四个顶点的坐标
        pts2 = np.float32([[self.rand_reduce(factor), self.rand_reduce(factor)],
                           [self.rand_reduce(factor), shape[0] - self.rand_reduce(factor)],
                           [shape[1] - self.rand_reduce(factor), self.rand_reduce(factor)],
                           [shape[1] - self.rand_reduce(factor), shape[0] - self.rand_reduce(factor)]])
        # 获取 3x3的投影映射/透视变换 矩阵
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        # 利用投影映射矩阵，进行透视变换
        dst = cv2.warpPerspective(img, matrix, size)
        return dst
    
    def rand_hsv(self, img):
        """ 添加饱和度光照的噪声
        :param img: BGR格式的图片
        :return 加了饱和度、光照噪声的BGR图片
        """
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # 色调，饱和度，亮度
        hsv[:, :, 0] = hsv[:, :, 0] * (self.hue_keep + np.random.random() * (1 - self.hue_keep))
        hsv[:, :, 1] = hsv[:, :, 1] * (self.saturation_keep + np.random.random() * (1 - self.saturation_keep))
        hsv[:, :, 2] = hsv[:, :, 2] * (self.value_keep + np.random.random() * (1 - self.value_keep))
        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return img
    
    def rand_environment(self, img, env_data_paths=None):
        """ 添加自然环境的噪声
        :param img: 待加噪图片
        :param env_data_paths: 自然环境图片路径列表
        """
        if env_data_paths is None:
            env_data_paths = self.env_data_paths
        # 随机选取环境照片
        index = self.rand_reduce(len(env_data_paths))
        env = cv2.imread(env_data_paths[index])
        env = cv2.resize(env, (img.shape[1], img.shape[0]))
        # 找到黑背景，反转为白
        bak = (img == 0)
        bak = bak.astype(np.uint8) * 255
        # 环境照片用白掩码裁剪，然后与原图非黑部分合并
        inv = cv2.bitwise_and(bak, env)
        img = cv2.bitwise_or(inv, img)
        return img
    
    def add_gauss(self, img, level=None):
        """ 添加高斯模糊
        :param img: 待加噪图片
        :param level: 加噪水平
        """
        if level is None:
            level = self.level
        return cv2.blur(img, (level * 2 + 1, level * 2 + 1))
    
    def add_single_channel_noise(self, single):
        """ 添加高斯噪声
        :param single: 单一通道的图像数据
        """
        diff = 255 - single.max()
        noise = np.random.normal(0, 1 + self.rand_reduce(6), single.shape)
        noise = (noise - noise.min()) / (noise.max() - noise.min())
        noise = diff * noise
        noise = noise.astype(np.uint8)
        dst = single + noise
        return dst
    
    def add_noise(self, img):
        """添加噪声"""
        img[:, :, 0] = self.add_single_channel_noise(img[:, :, 0])
        img[:, :, 1] = self.add_single_channel_noise(img[:, :, 1])
        img[:, :, 2] = self.add_single_channel_noise(img[:, :, 2])
        return img
    
    def add_smudge(self, img, smu=None):
        """添加污渍"""
        if smu is None:
            smu = self.smu
        # 截取某一部分
        rows = self.rand_reduce(smu.shape[0] - img.shape[0])
        cols = self.rand_reduce(smu.shape[1] - img.shape[1])
        add_smu = smu[rows:rows + img.shape[0], cols:cols + img.shape[1]]
        img = cv2.bitwise_not(img)
        img = cv2.bitwise_and(add_smu, img)
        img = cv2.bitwise_not(img)
        return img
    
    @staticmethod
    def search_file(search_path, file_format='.jpg'):
        """在指定目录search_path下，递归目录搜索指定尾缀的文件
        :param search_path: 指定的搜索目录，如：./2018年收集的素材并已校正
        :param file_format: 文件尾缀，如‘.jpg’
        :return: 该目录下所有指定尾缀文件的路径组成的list
        """
        file_path_list = []
        # 获取：1.父目录绝对路径 2.所有文件夹名字（不含路径） 3.所有文件名字
        for root_path, dir_names, file_names in os.walk(search_path):
            # 收集符合条件的文件名
            for filename in file_names:
                if filename.endswith(file_format):
                    file_path_list.append(os.path.join(root_path, filename))
        return file_path_list

    def augment(self, img):
        """ 综合上面的加载操作，进行全流程加噪
        :param img: 待加噪图片
        :return: 加噪后的图片，numpy数组
        """
        img = self.angle_perspective_transfer(img)
        img = self.rand_perspective_transfer(img)
        img = self.rand_hsv(img)
        img = self.rand_environment(img)
        img = self.add_gauss(img)
        img = self.add_noise(img)
        img = self.add_smudge(img)
        return img
