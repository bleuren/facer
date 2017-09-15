import _init_paths
from flask import Flask
from flask_socketio import SocketIO, send, emit
from fast_rcnn.config import cfg
from fast_rcnn.nms_wrapper import nms
from fast_rcnn.test import im_detect
import caffe
import os
import time
from matplotlib import pyplot as plt
import numpy as np
import StringIO
import urllib
import base64
import cv2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'facer'
socketio = SocketIO(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in set(['png','jpg','jpeg','gif'])

def vis_detections(img, rec_cls, emo_cls, dets, thresh=0.5):
    height, width, channels = img.shape
    inds = np.where(dets[:, -1] >= thresh)[0]
    img = img[:, :, (2, 1, 0)]
    try:
        fig, ax = plt.subplots(figsize=(int(15*width/(height+width)), int(15*height/(height+width))))
        ax.imshow(img, aspect='equal')
        for i in inds:
            bbox = dets[i, :4]
            score = dets[i, -1]
            ax.add_patch(
                plt.Rectangle((bbox[0], bbox[1]),
                            bbox[2] - bbox[0],
                            bbox[3] - bbox[1], fill=False,
                            edgecolor='red', linewidth=3.5)
                )
            ax.text(bbox[0], bbox[1] - 2,
                    '{:s} {:s} {:.1%}'.format(rec_cls[i], emo_cls[i], score),
                    bbox=dict(facecolor='blue', alpha=0.5),
                    fontsize=8, color='white')
        ax.set_title(('face recognition with p(face | box) >= {:.1f}').format(thresh),
                    fontsize=14)
        plt.axis('off')
        plt.tight_layout()
        imgdata = StringIO.StringIO()
        fig.savefig(imgdata, format='jpg')
        imgdata.seek(0)
        uri = 'data:image/jpeg;base64,' + urllib.quote(base64.b64encode(imgdata.buf))
        return uri
    except:
        return 0

def detect(img):
    caffe.set_mode_gpu()
    CONF_THRESH = 0.75
    NMS_THRESH = 0.15
    scores, boxes = im_detect(classifier['vgg16'], img)
    cls_ind = 1
    cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
    cls_scores = scores[:, cls_ind]
    dets = np.hstack((cls_boxes,
                      cls_scores[:, np.newaxis])).astype(np.float32)
    keep = nms(dets, NMS_THRESH)
    dets = dets[keep, :]
    keep = np.where(dets[:, 4] > CONF_THRESH)
    dets = dets[keep]
    return dets

def convert_mean(mean):
    sub = os.path.splitext(mean)
    if sub[1] == ".binaryproto":
        blob = caffe.proto.caffe_pb2.BlobProto()
        data = open(mean, 'rb').read()
        blob.ParseFromString(data)
        arr = np.array(caffe.io.blobproto_to_array(blob))
        mean = arr[0]
    else:
        mean = np.load(mean)
    mean = mean.mean(1).mean(1)
    return mean

def predict(classifier,capture,tresh,course):
    data = {'images':[], 'rec_cls':[], 'accuracy':[], 'emo_cls':[], 'people':[], 'output':[], 'dtime':{}}
    det_start = time.time()
    dets = detect(capture)
    data['dtime']['det'] = float('{:.2f}'.format(time.time() - det_start))
    inds = np.where(dets[:, -1] >= 0.5)[0]
    if len(inds) == 0:
        return
    for i in dets:
        pic = capture[int(i[1]):int(i[3]), int(i[0]):int(i[2])]
        data['images'].append([pic.astype(np.float32)])
    rec_start = time.time()
    for pic in data['images']:
        predictions = {'rec': classifier['rec'][0].predict(pic, oversample=False),
                       'emo': classifier['emo'][0].predict(pic, oversample=False)}
        emo_top_k = predictions['emo'].flatten().argsort()[-1:-4:-1]
        rec_top_k = predictions['rec'].flatten().argsort()[-1:-4:-1]
        data['rec_cls'].append(classifier['rec'][1][rec_top_k[0]])
        data['emo_cls'].append(classifier['emo'][1][emo_top_k[0]])
        accuracy = predictions['rec'][0, rec_top_k[0]]
        data['accuracy'].append(accuracy)
        if(float(accuracy)>tresh):
            data['people'].append({'id':classifier['rec'][1][rec_top_k[0]], 'emo': classifier['emo'][1][emo_top_k[0]], 'accuracy': float(accuracy)})
    data['dtime']['rec'] = float('{:.2f}'.format(time.time() - rec_start))
    dets[:, -1] = data['accuracy']
    view = vis_detections(capture, data['rec_cls'], data['emo_cls'], dets, tresh)
    data['dtime']['timestamp'] = int(time.time())
    data['output'] = {'course':course,
                      'people':data['people'],
                      'tresh':tresh,
                      'view':view,
                      'dtime': data['dtime']}
    return data['output']

@socketio.on('sendmsg')
def handleSendmsg(json):
    emit('message', json, broadcast=True, json=True)
   
@socketio.on('labels')
def handleGetlabels():
    labels = [line.rstrip() for line in open(NETS['rec'][2], 'r')]
    emit('labels', labels)

@socketio.on('predict')
def handlePredict(json):
    tresh = json['tresh']
    course = json['course']
    cam = cv2.VideoCapture(0)
    s, capture = cam.read()
    cam.release()
    pred = predict(classifier, capture, tresh, course)
    #pred = {'course': course, 'dtime': {'rec': 1.45, 'det': 1.98, 'timestamp': int(time.time())}, 'tresh': tresh, 'view': '', 'people': [{'emo': 'Neutral', 'id': '10461115', 'accuracy': 0.9995684027671814}]}
    send(pred, broadcast=True, json=True)

if __name__ == '__main__':
    caffe.set_mode_gpu()
    cfg.TEST.HAS_RPN = True
    NETS = {'vgg16': ('../../../models/face/detection/deploy.prototxt',
                      '../../../models/face/detection/model.caffemodel'),
            'rec': ('../../../models/face/recognition_stu/deploy.prototxt',
                    '../../../models/face/recognition_stu/model.caffemodel',
					'../../../models/face/recognition_stu/labels.txt',
                    '../../../models/face/recognition_stu/mean.binaryproto'),
            'emo': ('../../../models/face/emotion/deploy.prototxt',
                    '../../../models/face/emotion/model.caffemodel',
					'../../../models/face/emotion/labels.txt',
                    '../../../models/face/emotion/mean.binaryproto'
                    )}
    classifier = {'vgg16': caffe.Net(NETS['vgg16'][0], NETS['vgg16'][1], caffe.TEST),
                  'rec': (caffe.Classifier(NETS['rec'][0], NETS['rec'][1], image_dims=(224,224), mean=convert_mean(NETS['rec'][3])), np.loadtxt(NETS['rec'][2], str, delimiter='\t')),
                  'emo': (caffe.Classifier(NETS['emo'][0], NETS['emo'][1], image_dims=(224,224), mean=convert_mean(NETS['emo'][3])), np.loadtxt(NETS['emo'][2], str, delimiter='\t'))}
    socketio.run(app, host='0.0.0.0', debug=True)
