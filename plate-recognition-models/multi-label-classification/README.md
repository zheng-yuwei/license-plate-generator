# 基于多标签模型的车牌号识别

### 文件说明：
1. resnet18文件夹：将resnet18作为基础结构，设计多标签分类模型；
1. resnet50文件夹：将resnet50作为基础结构，设计多标签分类模型；
2. file_tools.py：提供文件搜索功能，在generate_txt.py中调用；
3. generate_txt.py：读取车牌图片目录下的图片，根据图片名称中的车牌号、license_plate_elements.py中车牌号字符与标签的映射关系，生成标签txt文件（7和8位车牌的全量、训练、测试、验证集，7位车牌全量数据集，8位车牌全量数据集），每一行格式为：图片路径 char1 char2 char3 char4 char5 char6 char7 char8 is_8_char plate_color；
4. generate_lmdb.sh：根据生成的txt文件，找到图片数据，然后调用caffe中改造过的generate_imageset二进制执行文件生成lmdb格式的数据集；
5. recognization_engine.py：检测模型测试代码。

### 模型结构
[Netscope Editor](http://ethereon.github.io/netscope/#/editor)

### 训练过程
1. 训练时，需要将7位车牌的第8位字符标记为-1，生成lmdb，然后在训练网络时，第8位的softmaxWithLoss层添加设置以忽略该类标签：
```
loss_param{
    ignore_label: -1
}
```
2. 训练时，记得平衡实际数据与生成的数据；
3. 车牌号的截取方式会影响模型的识别精度，所以最好是添加了检测模型检测出来的车牌；
