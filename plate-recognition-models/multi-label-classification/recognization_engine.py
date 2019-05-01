# -*- coding: utf-8 -*-
"""
Created on 2019/03/30

@author:x00472174
"""
import sys
import os
import cv2
import time
import argparse
from file_tools import FileTools
import pdb

sys.path.append('/home/zhengyuwei/software/quhezheng_caffe_yolov2/python')
import caffe


class RecognitionEngine(object):
    """车牌识别caffe模型测试代码"""
    
    # 车牌第1位字符的取值范围及其label
    char1_indices = {
        u"京": 0, u"沪": 1, u"津": 2, u"渝": 3, u"冀": 4, u"晋": 5, u"蒙": 6, u"辽": 7, u"吉": 8, u"黑": 9,
        u"苏": 10, u"浙": 11, u"皖": 12, u"闽": 13, u"赣": 14, u"鲁": 15, u"豫": 16, u"鄂": 17, u"湘": 18, u"粤": 19,
        u"桂": 20, u"琼": 21, u"川": 22, u"贵": 23, u"云": 24, u"藏": 25, u"陕": 26, u"甘": 27, u"青": 28, u"宁": 29,
        u"新": 30, u"军": 31, u"使": 32,
    }

    # 车牌第2位字符的取值范围及其label
    char2_indices = {
        "A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "J": 8, "K": 9,
        "L": 10, "M": 11, "N": 12, "P": 13, "Q": 14, "R": 15, "S": 16, "T": 17, "U": 18, "V": 19,
        "W": 20, "X": 21, "Y": 22, "Z": 23, "0": 24, "1": 25, "2": 26, "3": 27, "4": 28, "5": 29,
        "6": 30, "7": 31, "8": 32, "9": 33,
    }

    # 车牌第3~6位字符的取值范围及其label
    char3_6_indices = {
        "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
        "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15, "G": 16, "H": 17, "J": 18, "K": 19,
        "L": 20, "M": 21, "N": 22, "P": 23, "Q": 24, "R": 25, "S": 26, "T": 27, "U": 28, "V": 29,
        "W": 30, "X": 31, "Y": 32, "Z": 33,
    }

    # 车牌第7位字符的取值范围及其label
    char7_indices = {
        "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
        "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15, "G": 16, "H": 17, "J": 18, "K": 19,
        "L": 20, "M": 21, "N": 22, "P": 23, "Q": 24, "R": 25, "S": 26, "T": 27, "U": 28, "V": 29,
        "W": 30, "X": 31, "Y": 32, "Z": 33, u"学": 34, u"警": 35, u"领": 36, u"挂": 37, u"港": 38, u"澳": 39,
        u"使": 40,
    }

    # 车牌第8位字符的取值范围及其label
    char8_indices = {
        "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "D": 10, "F": 11,
    }
    
    # 车牌号字符数
    char_num_indices = {"7": 0, "8": 1}
    
    # 车牌颜色
    plate_color_indices = {'blue': 0, 'yellow': 1, 'green': 2, 'white': 3, 'black': 4, 'other': 5, }

    char1_indices = {v: k for k, v in char1_indices.items()}
    char2_indices = {v: k for k, v in char2_indices.items()}
    char3_6_indices = {v: k for k, v in char3_6_indices.items()}
    char7_indices = {v: k for k, v in char7_indices.items()}
    char8_indices = {v: k for k, v in char8_indices.items()}
    char_num_indices = {v: k for k, v in char_num_indices.items()}
    plate_color_indices = {v: k for k, v in plate_color_indices.items()}
    
    def __init__(self, root_dir, caffemodel_name, prototxt_name, shape=(48, 144)):
        """ 初始化caffe模型
        :param root_dir: 模型文件所在根目录
        :param caffemodel_name: 模型文件名称
        :param prototxt_name: prototxt文件名称
        :param shape: 模型输入图片的尺寸
        """
        caffe.set_device(0)
        caffe.set_mode_gpu()
        self.net = caffe.Net(os.path.join(root_dir, prototxt_name),
                             os.path.join(root_dir, caffemodel_name), caffe.TEST)
        self.transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
        self.transformer.set_transpose('data', (2, 0, 1))
        self.net.blobs['data'].reshape(1, 3, shape[0], shape[1])

    def recognize(self, plate_image):
        """ 进行车牌号识别
        :param plate_image: 车牌图片，BGR [0, 255]
        :return:
            {'char_num_prob': 车牌号位数概率, 'plate_no': 车牌号, 'confidence': 车牌号每位置信度列表,
            'plate_color': 车牌底色, 'color_confidence': 车牌底色置信度}
            inference_time: 推理时间
        """
        if plate_image is None:
            return None

        plate_image = self.transformer.preprocess('data', plate_image)
        self.net.blobs['data'].data[...] = plate_image / 255
        start_time = time.time()
        self.net.forward()
        inference_time = time.time() - start_time
        
        # 解析模型输出：车牌号字符、位数、底色，及对应概率
        char1 = self.char1_indices[self.net.blobs['prob1'].data[...].argmax(1)[0]]
        char1_prob = self.net.blobs['prob1'].data[...].max()
        char2 = self.char2_indices[self.net.blobs['prob2'].data[...].argmax(1)[0]]
        char2_prob = self.net.blobs['prob2'].data[...].max()
        char3 = self.char3_6_indices[self.net.blobs['prob3'].data[...].argmax(1)[0]]
        char3_prob = self.net.blobs['prob3'].data[...].max()
        char4 = self.char3_6_indices[self.net.blobs['prob4'].data[...].argmax(1)[0]]
        char4_prob = self.net.blobs['prob4'].data[...].max()
        char5 = self.char3_6_indices[self.net.blobs['prob5'].data[...].argmax(1)[0]]
        char5_prob = self.net.blobs['prob5'].data[...].max()
        char6 = self.char3_6_indices[self.net.blobs['prob6'].data[...].argmax(1)[0]]
        char6_prob = self.net.blobs['prob6'].data[...].max()
        char7 = self.char7_indices[self.net.blobs['prob7'].data[...].argmax(1)[0]]
        char7_prob = self.net.blobs['prob7'].data[...].max()
        char8 = self.char8_indices[self.net.blobs['prob8'].data[...].argmax(1)[0]]
        char8_prob = self.net.blobs['prob8'].data[...].max()
        char_num = self.char_num_indices[self.net.blobs['char_num_prob'].data[...].argmax(1)[0]]
        char_num_prob = self.net.blobs['char_num_prob'].data[...].max()
        plate_color = self.plate_color_indices[self.net.blobs['plate_color'].data[...].argmax(1)[0]]
        plate_color_prob = self.net.blobs['plate_color'].data[...].max()
        # pdb.set_trace()
        
        # to check if the plate has 7 or 8 characters.
        if char_num == '7':
            plate = char1 + char2 + char3 + char4 + char5 + char6 + char7
            confidence = [char1_prob, char2_prob, char3_prob, char4_prob, char5_prob, char6_prob, char7_prob]
        else:
            plate = char1 + char2 + char3 + char4 + char5 + char6 + char7 + char8
            confidence = [char1_prob, char2_prob, char3_prob, char4_prob,
                          char5_prob, char6_prob, char7_prob, char8_prob]
        
        return {'char_num_prob': char_num_prob, 'plate_no': plate, 'confidence': confidence,
                'plate_color': plate_color, 'color_confidence': plate_color_prob}, inference_time
        
    def judge(self, plate_image, truth_plate_no, save_dir='', save_fail=False, save_success=False):
        """ 判断车牌号图片是否指定的车牌号，以及是否保存车牌图片
        :param plate_image: 车牌图片
        :param truth_plate_no: 真实车牌号
        :param save_dir: 图片保存路径
        :param save_fail: 是否保存失败图片
        :param save_success: 是否保存成功图片
        :return:
            bool： 车牌号图片是否指定的车牌号
            recognized_result： 车牌号图片识别结果
            recognized_time： 识别模型推理时间
        """
        if truth_plate_no[0] == '挂':
            new_gt_plate_no = ['桂']
            for plate_no_index in range(1, len(truth_plate_no)):
                new_gt_plate_no.append(truth_plate_no[plate_no_index])
            truth_plate_no = ''.join(new_gt_plate_no)
                
        recognized_result, recognized_time = self.recognize(plate_image)
        if truth_plate_no == recognized_result['plate_no']:
            if save_success:
                cv2.imwrite(os.path.join(save_dir, 'success/{}.jpg'.format(truth_plate_no)), plate_image)
            return True, recognized_result, recognized_time
        else:
            if save_fail:
                # 加上检测概率
                score = ['{:.1f}'.format(_) for _ in recognized_result['confidence']]
                cv2.putText(plate_image, score, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0))
                cv2.imwrite(os.path.join(fail_path,
                                         'fail/{}_{}.jpg'.format(truth_plate_no, recognized_result['plate_no'])),
                            plate_image)
            return False, recognized_result, recognized_time


if __name__ == '__main__':
    model_root_dir = '/home/data_160/data3/smart_home/xiongxin-yuwei/plate_recognition/models/resnet50/'
    model_name = 'lp_recognization_iter_20000.caffemodel'
    prototxt = 'recognition-deploy.prototxt'
    truth_color = 'green'
    recognition_engine = RecognitionEngine(model_root_dir, model_name, prototxt)
    
    images_root_dir = '/home/data_160/data3/smart_home/xiongxin-yuwei/plate_recognition/new_plate_images/'
    parser = argparse.ArgumentParser('Detect objects in image')
    parser.add_argument('--input', type=str, help='Input image',
                        default=images_root_dir + 'fushi/green')
    parser.add_argument('--output', type=str, help='Output image',
                        default=images_root_dir + 'temp2')
    args = parser.parse_args()
    
    if os.path.isfile(args.input):
        img_paths = [args.input]
    elif os.path.isdir(args.input):
        img_paths = FileTools.search_file(args.input, '.jpg')
    else:
        raise ValueError('输入路径不存在')
    
    if not os.path.exists(args.output):
        raise ValueError('输出路径不存在')
    else:
        success_path = os.path.join(args.output, 'success')
        fail_path = os.path.join(args.output, 'fail')
        if not os.path.exists(success_path):
            os.makedirs(success_path)
        if not os.path.exists(fail_path):
            os.makedirs(fail_path)

    inference_time_total_time = 0
    fail_recognize = 0
    success_recognize = 0
    fail_color = 0
    fail_image_paths = list()
    fail_color_paths = dict()
    i = 0
    total = len(img_paths)
    for image_path in img_paths:
        i += 1
        if i % 1000 == 0:
            print('{}/{} done...'.format(i, total))
        
        image = cv2.imread(image_path)
        if image is None:
            total -= 1
            continue
            
        gt_plate_num = os.path.splitext(os.path.basename(image_path))[0].split('_')[-1]
        is_success, result, temp_time = recognition_engine.judge(image, gt_plate_num, args.output)
        inference_time_total_time += temp_time
        if is_success:
            success_recognize += 1
        else:
            fail_image_paths.append(os.path.basename(image_path))
            fail_recognize += 1
        
        if result['plate_color'] != truth_color:
            fail_color += 1
            fail_color_paths[os.path.basename(image_path)] = '{}|{}'.format(result['plate_color'],
                                                                            result['color_confidence'])
            
    print('总检测数量：{}， 检测准确：{}，'.format(total, success_recognize),
          ' 检测错误：{}， 颜色错误：{}'.format(fail_recognize, fail_color))
    print('检测时间(s)：', inference_time_total_time / total)
    print('识别失败', fail_image_paths)
    print('车牌颜色错误', fail_color_paths)
