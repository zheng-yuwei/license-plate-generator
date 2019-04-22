#!/usr/bin/env sh

CAFFE_HOME=/home/zhengyuwei/software/multi_label_caffe/build/

SOLVER=./RMSProp-solver.prototxt
WEIGHTS=/home/data_160/data1/license_plate/models/resnet-9label-RMSProp/lp_recognization1_iter_30000.caffemodel

$CAFFE_HOME/tools/caffe train --solver=$SOLVER --gpu=3 --weights=$WEIGHTS 
