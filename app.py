for element in dir():
    if element[0:2] != "__":
        del globals()[element]

from flask import Flask, request, redirect, url_for, render_template
from werkzeug.datastructures import CombinedMultiDict
from wtforms import Form, ValidationError
from flask_wtf.file import FileField
import tempfile
import io
import base64
from PIL import Image
import cv2
from numpy import asarray
import detectron2
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from visualizer import Visualizer, ColorMode
from torch import torch
import os

cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 14  
cfg.INPUT.RANDOM_FLIP='none'
cfg.TEST.AUG.FLIP=False

cfg.MODEL.WEIGHTS='/opt/model_final.pth'

cfg.MODEL.DEVICE="cpu"
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.1   # set a custom testing threshold
predictor = DefaultPredictor(cfg)

X_ray_metadata = [
  'Aortic enlargement',
  'Atelectasis',
  'Calcification',
  'Cardiomegaly',
  'Consolidation',
  'ILD',
  'Infiltration',
  'Lung Opacity',
  'Nodule/Mass',
  'Other lesion',
  'Pleural effusion',
  'Pleural thickening',
  'Pneumothorax',
  'Pulmonary fibrosis',
  'No finding']

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)

def encode_image(image):
  image_buffer = io.BytesIO()
  image.save(image_buffer, format='PNG')
  imgstr = 'data:image/png;base64,{:s}'.format(
      base64.b64encode(image_buffer.getvalue()).decode().replace("'", ""))
  return imgstr

@app.route('/')
def upload():
  return render_template('upload.html', result={})

@app.route('/post', methods=['GET', 'POST'])
def post():
  if request.method == 'POST':
    file = request.files['file']
    if not allowed_file(file.filename):
        result={}
        result['original'] = 'File extension should be: %s' % ', '.join(ALLOWED_EXTENSIONS)
        return render_template('upload.html', result=result)

    with tempfile.NamedTemporaryFile() as temp:
      file.save(temp.name)
      temp.flush()
      image = Image.open(temp.name).convert('RGB')
      
      image = asarray(image)
      image= cv2.resize(image,(2748,2393))
      outputs = predictor(image)
      w, h, _ =image.shape
      im_size=600
      bboxes=outputs['instances'].pred_boxes.tensor
      bboxes=[[box[0]*im_size/h, box[1]*im_size/w, box[2]*im_size/h, box[3]*im_size/w] for box in bboxes]
      image=cv2.resize(image,(im_size,im_size))
      image=Image.fromarray(image, 'RGB')

      result = {}
      if len(outputs['instances'].pred_classes)==0:
        result['original']='No disease detected'
      else:
        result['original'] = encode_image(image.copy())
        result['boxes'] = bboxes
        result['labels'] = [X_ray_metadata[l] for l in outputs['instances'].pred_classes]

    return render_template('upload.html', result=result)
  else:
    return redirect(url_for('upload'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True,host='0.0.0.0',port=port)
