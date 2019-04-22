# 基于多标签模型的车牌号识别

### 文件说明：
1. resnet18文件夹：基于resnet18的building block结构，设计多标签分类模型；
2. file_tools.py：提供文件搜索功能，在generate_txt.py中调用；
3. generate_txt.py：读取车牌图片目录下的图片，根据图片名称中的车牌号、license_plate_elements.py中车牌号字符与标签的映射关系，生成标签txt文件（7和8位车牌的全量、训练、测试、验证集，7位车牌全量数据集，8位车牌全量数据集），每一行格式为：图片路径 char1 char2 char3 char4 char5 char6 char7 char8 is_8_char，其中7个字符的车牌，char8为随机挑选，is8char为0；
4. generate_lmdb.sh：根据生成的txt文件，找到图片数据，然后调用caffe中改造过的generate_imageset二进制执行文件生成lmdb格式的数据集。

### 模型结构
[Netscope Editor](http://ethereon.github.io/netscope/#/editor)

### 训练过程建议
1. 用RMSProp优化方法，全量数据，但第8位车牌号loss低权重（前7位0.1111，第8位0.0001，位数标志位0.2222）进行初始训练；
2. 固定第1步训练好的网络的骨干网络权重、前7位loss层权重、位数标志位层权重（propagate_down : 0），调整第8位车牌号loss权重为1.0，使用8位车牌数据进行训练；
3. 固定第2步训练好的网络的骨干网络权重、第8位loss层权重（propagate_down : 0），使用全量车牌数据进行训练；
4. 融合真实数据集对训练好的模型，进行同样的训练。

tips：
第一步决定了骨干网络的性能；第二步微调了第8位损失层的权重；第三步微调了其他损失层的权重。
