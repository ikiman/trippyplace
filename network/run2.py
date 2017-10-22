# PlacesCNN to predict the scene category, attribute, and class activation map in a single pass
# by Bolei Zhou, sep 2, 2017

import torch
from torch.autograd import Variable as V
import torchvision.models as models
from torchvision import transforms as trn
from torch.nn import functional as F
import os
import numpy as np
from scipy.misc import imresize as imresize
from PIL import Image
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import json

def load_labels():
  file_name_category = 'categories_places365.txt'
  classes = list()
  with open(file_name_category) as class_file:
    for line in class_file:
      classes.append(line.strip().split(' ')[0][3:])
  classes = tuple(classes)
  file_name_attribute = 'labels_sunattribute.txt'
  with open(file_name_attribute) as f:
    lines = f.readlines()
    labels_attribute = [item.rstrip() for item in lines]
  file_name_W = 'W_sceneattribute_wideresnet18.npy'
  W_attribute = np.load(file_name_W)

  return classes, labels_attribute, W_attribute

def hook_feature(module, input, output):
  features_blobs.append(np.squeeze(output.data.cpu().numpy()))

def returnTF():
# load the image transformer
  tf = trn.Compose([
    trn.Scale((224,224)),
    trn.ToTensor(),
    trn.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
  ])
  return tf


def load_model():
  model_file = 'whole_wideresnet18_places365.pth.tar'
  useGPU = 0
  if useGPU == 1:
    model = torch.load(model_file)
  else:
    model = torch.load(model_file, map_location=lambda storage, loc: storage) # allow cpu

  model.eval()
  features_names = ['layer4','avgpool'] # this is the last conv layer of the resnet
  for name in features_names:
    model._modules.get(name).register_forward_hook(hook_feature)
  return model

class S(BaseHTTPRequestHandler):
  def _set_headers(self):
    self.send_response(200)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()

  def do_POST(self):
    content_length = int(self.headers['Content-Length'])
    post_data = self.rfile.read(content_length)

    img = Image.open(post_data)
    input_img = V(tf(img).unsqueeze(0), volatile=True)

    # forward pass
    logit = model.forward(input_img)
    h_x = F.softmax(logit).data.squeeze()
    probs, idx = h_x.sort(0, True)


    responses_attribute = W_attribute.dot(features_blobs[1])
    idx_a = np.argsort(responses_attribute)
    attributes = ', '.join([labels_attribute[idx_a[i]] for i in range(-1,-10,-1)])
    categories = ', '.join(classes[idx[i]] for i in range(0, 5))

    result = { 'attributes': attributes, 'categories': categories }
    self._set_headers()
    self.wfile.write(json.dumps(result))

def run(server_class=HTTPServer, handler_class=S, port=8000):
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  httpd.serve_forever()

classes, labels_attribute, W_attribute = load_labels()
features_blobs = []
model = load_model()
tf = returnTF()

params = list(model.parameters())
weight_softmax = params[-2].data.numpy()
weight_softmax[weight_softmax<0] = 0

# img = Image.open('image.jpg')
# input_img = V(tf(img).unsqueeze(0), volatile=True)

# logit = model.forward(input_img)
# h_x = F.softmax(logit).data.squeeze()
# probs, idx = h_x.sort(0, True)


# responses_attribute = W_attribute.dot(features_blobs[1])
# idx_a = np.argsort(responses_attribute)
# attributes = ', '.join([labels_attribute[idx_a[i]] for i in range(-1,-10,-1)])
# categories = ', '.join(classes[idx[i]] for i in range(0, 5))

# print({'attributes': attributes, 'categories': categories })

run()
