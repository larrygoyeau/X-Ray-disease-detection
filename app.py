from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import cv2
import detectron2
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.utils.visualizer import Visualizer
from detectron2.utils.visualizer import ColorMode

cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 14  # only has one class (ballon). (see https://detectron2.readthedocs.io/tutorials/datasets.html#update-the-config-for-new-datasets)
cfg.INPUT.RANDOM_FLIP='none'
cfg.TEST.AUG.FLIP=False

cfg.MODEL.WEIGHTS='/opt/model_final.pth'
#NOTE: this config means the number of classes, but a few popular unofficial tutorials incorrect uses num_classes+1 here.
cfg.MODEL.DEVICE="cpu"
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.3   # set a custom testing threshold
predictor = DefaultPredictor(cfg)

MetadataCatalog.get("vinbigdata").set(thing_classes=['Aortic enlargement',
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
                                                           'No finding'])
balloon_metadata = MetadataCatalog.get("vinbigdata")

UPLOAD_FOLDER = 'target/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            '''
            im = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            im = cv2.resize(im,(700,700))
            outputs = predictor(im)
            v = Visualizer(im[:, :, ::-1],
                   metadata=balloon_metadata, 
                   scale=0.8, 
                   instance_mode=ColorMode.IMAGE_BW   # remove the colors of unsegmented pixels
            )
            v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
            cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], filename), v.get_image()[:, :, ::-1])
            '''
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    else:
        return '''
        <!doctype html>
        <title>Upload new Fillllllle</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Upload>
        </form>
        '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
