# X-Ray disease detection web app

[Link to the app](http://xray.lgoyeau.com/)

<a href="http://xray.lgoyeau.com" target="_blank">http://xray.lgoyeau.com</a>

This app is based on the method that I used to get my position in the Kaggel [competition for disease detection on X-ray images](https://www.kaggle.com/c/vinbigdata-chest-xray-abnormalities-detection/leaderboard) (401st of 1277).

You can find explanations on the method used to train the model in the following notebook:
https://colab.research.google.com/drive/1Gx9JwNFz7LtD0moyVFyPRtl2vfI0vNo8?usp=sharing

This web app use Flask for the communication between the server and the client interface. The server is provided by DigitalOcean. 2 GB of RAM is necessary to run the app. No GPU is used for inference, only CPU.

### Building the app

```
docker build -t x-ray-disease-detection .
```

### Running the app

```
docker run -p 5000:5000 x-ray-disease-detection
```
And visit http://localhost:5000
