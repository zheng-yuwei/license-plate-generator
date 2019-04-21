# -*- coding: utf-8 -*-
"""
Created on 2019/3/28
File file_tools
@author:ZhengYuwei
"""
import os
import shutil
import sys
import getopt


class FileTools(object):
    """ 文件处理工具类 """
    
    @staticmethod
    def mkdir(new_dir):
        """ 建立文件夹路径 """
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        return

    @staticmethod
    def search_file(search_path, file_format):
        """在指定目录search_path下，递归目录搜索指定尾缀的文件
        :param search_path: 指定的搜索目录，如：./2018年收集的素材并已校正
        :param file_format: 文件尾缀，如‘.txt’
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

    @staticmethod
    def copy_file(file_path_list, destination_file):
        """  将文件列表中的文件拷贝到目的文件夹（为空，不存在则创建，存在则删除再创建）下
        :param file_path_list: 文件路径列表
        :param destination_file: 目的文件夹（为空，不存在则创建，存在则删除再创建）
        """
        # 保证目标目录为空
        if not os.path.exists(destination_file):
            os.removedirs(destination_file)
            os.makedirs(destination_file)
        
        # 复制文件
        for file_path in file_path_list:
            if not os.path.isfile(file_path):
                print("{} doesn't exist!".format(file_path))
            else:
                dst_file_name = os.path.join(destination_file, os.path.basename(file_path))
                # 名字重复的图片，修改名称
                flag = 1
                while os.path.isfile(dst_file_name):
                    dst_file_name = os.path.splitext(os.path.basename(file_path))
                    dst_file_name = dst_file_name[0] + '_' + str(flag) + '.' + dst_file_name[1]
                    dst_file_name = os.path.join(destination_file, dst_file_name)
                    flag += 1
                if flag != 1:
                    print('filename conflict: {}'.format(os.path.basename(file_path)))
                shutil.copy(file_path, dst_file_name)
        return


if __name__ == '__main__':
    """ 从源文件夹中，拷贝特定格式的文件，到目标文件夹（为空，不存在则创建，存在则删除再创建）中:
    -s --src=: 源文件夹
    -t --target=: 目标文件夹
    [-f --format=]: 可选，指定文件格式
    """
    opts, args = getopt.getopt(sys.argv[1:], 's:t:f:', ['src=', 'target=', 'format='])
    src_path = None
    target_path = None
    file_type = ''
    for key, value in opts:
        if key in ['-s', '--src']:
            src_path = value
        elif key in ['-t', '--target']:
            target_path = value
        elif key in ['-f', '--format']:
            file_type = value
        else:
            print("忽略选项 '{}'".format(key))
            
    if (src_path is None or src_path == '') or (target_path is None or target_path == ''):
        print("输入指令有误（e.g. python file_tools.py -s /home/a -t /home/b [-f .txt] )")
    elif not os.path.isdir(src_path) or not os.path.isdir(target_path):
        print('输入-s或-t选项为不合法（必须是存在路径）')
    else:
        print('源文件夹：{}'.format(src_path))
        print('目标文件夹：{}'.format(target_path))
        print('文件格式：{}'.format(file_type))
        FileTools.copy_file(FileTools.search_file(src_path, file_type), target_path)
