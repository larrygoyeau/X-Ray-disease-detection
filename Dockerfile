FROM python:3

WORKDIR /opt

COPY requirements.txt ./
COPY model.py ./

RUN pip install --no-cache-dir torch==1.8.1 torchvision==0.9.1
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/torch1.8/index.html
RUN python model.py

COPY . .

CMD [ "python", "./app.py" ]
