#!/usr/bin/env sh

CAFFE_HOME=/home/zhengyuwei/software/multi_label_caffe/build/

SOLVER=./recognition-resnet18-solver.prototxt
WEIGHTS=/home/data_160/data1/license_plate/plate_recognition/models/fushi_xin_resnet18/lp_recognization_iter_10000.solverstate

$CAFFE_HOME/tools/caffe train --solver=$SOLVER --gpu=0 --snapshot=$WEIGHTS 
