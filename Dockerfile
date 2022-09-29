FROM python:3

WORKDIR /opt

COPY requirements.txt ./
COPY model.py ./

RUN pip3 install --no-cache-dir torch==1.11.0 torchvision==0.12.0
RUN pip3 install --no-cache-dir -r requirements.txt
RUN python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'
RUN python model.py

COPY . .

COPY templates ./

CMD [ "python", "./app.py" ]
