from google_drive_downloader import GoogleDriveDownloader as gdd
import os

MODEL_PATH='/opt/model_final.pth'
if not os.path.exists(MODEL_PATH):
  gdd.download_file_from_google_drive(file_id='10PSd9TROaVdRGXH3sy3L_7nHqPB0Hu30',
                                    dest_path=MODEL_PATH,
                                    unzip=False)