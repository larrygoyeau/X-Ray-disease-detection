import gdown
import os

MODEL_PATH='/opt/model_final.pth'
if not os.path.exists(MODEL_PATH):
  url = 'https://drive.google.com/uc?id=10PSd9TROaVdRGXH3sy3L_7nHqPB0Hu30'
  gdown.download(url, MODEL_PATH, quiet=False)
