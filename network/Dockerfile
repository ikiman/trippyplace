FROM python:2.7-slim

WORKDIR /root

RUN apt-get update && apt-get install -y wget && \
    pip install http://download.pytorch.org/whl/cu75/torch-0.2.0.post3-cp27-cp27mu-manylinux1_x86_64.whl && \
    pip install torchvision && \
    pip install -U numpy && \
    pip install scipy && \
    wget https://raw.githubusercontent.com/csailvision/places365/master/categories_places365.txt && \
    wget https://raw.githubusercontent.com/csailvision/places365/master/labels_sunattribute.txt && \
    wget http://places2.csail.mit.edu/models_places365/W_sceneattribute_wideresnet18.npy && \
    wget https://raw.githubusercontent.com/csailvision/places365/master/wideresnet.py && \
    rm -rf /root/.cache

COPY . .

EXPOSE 8000

CMD ["python", "run2.py"]
