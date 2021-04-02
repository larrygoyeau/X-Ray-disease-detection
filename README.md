# X-Ray disease detection web app

[Link to the app (under development)](http://xray.lgoyeau.com/)

This app is based on the methode that I used to get my position on the kaggel [competition for disease detection on X-ray images](https://www.kaggle.com/c/vinbigdata-chest-xray-abnormalities-detection/leaderboard).


### Building the app

```
docker build -t x-ray-disease-detection .
```

### Running the app

```
docker run -p 5000:5000 x-ray-disease-detection
```
And visit http://localhost:5000
