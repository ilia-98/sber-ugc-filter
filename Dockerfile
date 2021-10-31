# syntax=docker/dockerfile:1

FROM brunneis/python:3.8.3-ubuntu-20.04
COPY requirements.txt requirements.txt
RUN apt-get -y update
RUN apt-get install -y build-essential cmake
#RUN apt-get install -y build-essential cmake pkg-config
#RUN apt-get install -y libx11-dev libatlas-base-dev
#RUN apt-get install -y libgtk-3-dev libboost-python-dev
RUN pip3 install dlib
RUN apt-get install -y ffmpeg
RUN pip3 install -r requirements.txt
COPY . .
WORKDIR "/app"
CMD [ "main.py"]