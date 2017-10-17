FROM floydhub/dl-docker:cpu

WORKDIR /root/caffe

RUN wget http://places2.csail.mit.edu/models_places365/alexnet_places365.caffemodel && \
    wget https://raw.githubusercontent.com/metalbubble/places365/master/deploy_alexnet_places365.prototxt && \
    mkdir models_places && \
    mv alexnet_places365.caffemodel deploy_alexnet_places365.prototxt models_places

COPY ./resources /root/caffe/resources
COPY ./run.py /root/caffe/run.py

EXPOSE 8000

CMD ["python", "run.py"]
