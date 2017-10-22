# FROM floydhub/dl-docker:cpu
FROM python:2.7-slim

WORKDIR /root

RUN apt-get update && apt-get install -y wget
RUN pip install http://download.pytorch.org/whl/cu75/torch-0.2.0.post3-cp27-cp27mu-manylinux1_x86_64.whl
RUN pip install torchvision
RUN pip install -U numpy
RUN pip install scipy
RUN wget https://raw.githubusercontent.com/csailvision/places365/master/categories_places365.txt
RUN wget https://raw.githubusercontent.com/csailvision/places365/master/labels_sunattribute.txt
RUN wget http://places2.csail.mit.edu/models_places365/W_sceneattribute_wideresnet18.npy
RUN wget https://raw.githubusercontent.com/csailvision/places365/master/wideresnet.py

COPY . .

EXPOSE 8000

CMD ["python", "run2.py"]
