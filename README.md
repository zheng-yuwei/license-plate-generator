# 中国车牌生成
@author **郑煜伟** in 2019-04-18  
目前支持蓝色标准车牌，黄色标准车牌，小型新能源车牌的车牌生成。
![生成的蓝色底牌车牌示例](https://github.com/zheng-yuwei/license-plate-generator/blob/master/plate_images/single_blue/00_%E7%94%98A0W9U9.jpg)
![生成的小型新能源车牌示例](https://github.com/zheng-yuwei/license-plate-generator/blob/master/plate_images/small_new_energy/00_%E4%BA%91HD40984.jpg)

### 文件夹目录说明
1. background: 车牌生成时，随机选取其中一张作为背景照片放置在车牌后面，类似于车头部分；
2. doc：放置了车牌号的国家规定文档；
3. font：车牌号的英文/中文字体；
4. images：各种车牌底牌（蓝色底牌等），污渍图片（图像增强使用）；
5. plate_images：生成的车牌图片的存放路径。
6. plate-recognition-models：车牌识别模型
    - multi-label-classification：多标签分类模型，下面包含了生成lmdb的脚本和参考resnet18写的多标签分类模型；

### 程序结构说明
- license_plate_elements.py: 车牌号元素，其中定义：
1. 车牌号中，不同车牌位的取值范围；
2. 不同的车牌类型。
- generate_license_plate_number.py: 根据车牌类型，生成指定数量的车牌号
1. 定义不同车牌类型中，对应车牌位的取值规则；（当前只定义了标准车牌和小型新能源车牌的车牌号取值规则）
2. 从license_plate_elements.py中，读取不同车牌位的初始初值范围。
  
- generate_chars_image.py: 指定车牌类型，根据给定的车牌号列表，生成车牌号文字图片
1. 根据实际车牌号字体大小，生成相应的中英文字符；
2. 依照车牌号不同位字符的分布规则，将生成的字符放置在对应的位置上，得到最终的车牌号文字图片。
- generate_plate_template.py: 指定车牌类型，生成车牌底牌图片
1. 根据车牌类型，加载底牌图片；
2. 根据指定尺寸resize。

- augment_image.py: 根据车牌类型，组合车牌底牌、车牌号图片，并进行数据增强
1. 根据车牌类型，判断车牌号图片为白字黑底 或 黑字白底；
2. 对车牌号图片、底牌，进行同样的透视视角变换，对底牌加背景；
3. 组合车牌底牌、车牌号图片
2. 对车牌图片进行剩余数据增强，包含HSV变化、高斯噪声、添加污渍。

- generate_license_plate.py: 主函数，按照流程调用以上Python脚本，生成图像增强后的车牌图片
1. 生成指定类型、指定数量的车牌号；
2. 生成车牌图片；
3. 进行数据增强；
4. 保存图片。

### 生成lmdb格式数据集及模型训练
参考plate-recognition-models文件夹下README.md。

### TODO:
1. 将其他车牌类型的规则定义好，以生成其他类型的车牌；
2. 车牌底牌图片分辨率不统一，且不太标准，待改善。


