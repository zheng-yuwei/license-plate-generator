#!/usr/bin/env sh

CAFFE_HOME=/home/zhengyuwei/software/multi_label_caffe/build/

SOLVER=./solver.prototxt
WEIGHTS=/home/data_160/data1/license_plate/models/resnet-9label/lp_recognization_iter_50000.caffemodel

$CAFFE_HOME/tools/caffe train --solver=$SOLVER --gpu=2 #--weights=$WEIGHTS 
