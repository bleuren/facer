# --------------------------------------------------------
# Fast R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""Set up paths for Fast R-CNN."""

import os.path as osp
import sys

def add_path(path):
    """add_path"""
    if path not in sys.path:
        sys.path.insert(0, path)

THIS_DIR = osp.dirname(__file__)

# Add caffe to PYTHONPATH
caffe_path = osp.join(THIS_DIR, '..', '..', 'caffe-fast-rcnn', 'python')
add_path(caffe_path)

# Add lib to PYTHONPATH
LIB_PATH = osp.join(THIS_DIR, '..', '..', 'lib')
add_path(LIB_PATH)