#!/usr/bin/env sh

CAFFE_HOME=/home/zhengyuwei/software/multi_label_caffe/build/

SOLVER=./recognition-resnet50-solver.prototxt
WEIGHTS=/home/data_160/data3/smart_home/xiongxin-yuwei/plate_recognition/models/resnet50/lp_recognization_iter_10000.caffemodel

$CAFFE_HOME/tools/caffe train --solver=$SOLVER --gpu=3 #--weights=$WEIGHTS 
