FROM python:3

WORKDIR /opt

COPY requirements.txt ./
#RUN pip install --no-cache-dir torch==1.8.0+cpu torchvision==0.9.0+cpu
RUN pip install --no-cache-dir torch torchvision
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app.py" ]