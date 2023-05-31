# [X-Ray disease detection web app](http://xray.lgoyeau.com/)

This app is based on the method that I used to get my position in Kaggel [competition for disease detection on X-ray images](https://www.kaggle.com/c/vinbigdata-chest-xray-abnormalities-detection/leaderboard) (375st of 1277).

You can find explanations on the method used to train the model in the following notebook:
https://colab.research.google.com/drive/1Gx9JwNFz7LtD0moyVFyPRtl2vfI0vNo8?usp=sharing

This web app use Flask for the communication between the server and the client interface. The server is provided by DigitalOcean. 2 GB of RAM is necessary to run the app. No GPU is used for inference, only CPU.

![alt text](https://github.com/larrygoyeau/X-Ray-disease-detection/blob/master/WebApp.gif)

## In local:
### Building the app

```
docker build -t x-ray-disease-detection .
```

### Running the app

```
docker run -p 80:8080 x-ray-disease-detection
```
And visit http://localhost:80

## Souces

[Detectron2](https://github.com/facebookresearch/detectron2)

[tensorflow-object-detection-example](https://github.com/GoogleCloudPlatform/tensorflow-object-detection-example)
