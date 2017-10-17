import numpy as np
import sys
import caffe
import pickle
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import random
import json

def classify_scene(im):
	fpath_design = 'models_places/deploy_alexnet_places365.prototxt'
	fpath_weights = 'models_places/alexnet_places365.caffemodel'
	fpath_labels = 'resources/labels.pkl'

	# initialize net
	net = caffe.Net(fpath_design, fpath_weights, caffe.TEST)

	# load input and configure preprocessing
	transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
	transformer.set_mean('data', np.load('python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1)) # TODO - remove hardcoded path
	transformer.set_transpose('data', (2,0,1))
	transformer.set_channel_swap('data', (2,1,0))
	transformer.set_raw_scale('data', 255.0)

	# since we classify only one image, we change batch size from 10 to 1
	net.blobs['data'].reshape(1,3,227,227)

	# load the image in the data layer
	net.blobs['data'].data[...] = transformer.preprocess('data', im)

	# compute
 	print "DEBUG: net.forward"
	out = net.forward()

	result = []

	with open(fpath_labels, 'rb') as f:
	 	print "DEBUG: labels"
		labels = pickle.load(f)
		top_k = net.blobs['prob'].data[0].flatten().argsort()[-1:-6:-1]

	 	print "DEBUG: to list"
		for i, k in enumerate(top_k):
			result.append(labels[k])

	return result

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length)
		tmp_file_name = "img%s" % random.randint(0, 100000)
		print "DEBUG: writing file"
		with open(tmp_file_name, 'wb') as f:
			f.write(post_data)
		print "DEBUG: loading image"
		im = caffe.io.load_image(tmp_file_name)
		print "DEBUG: Classifying"
		result = classify_scene(im)
		print "DEBUG: classified"
		self._set_headers()
		print "DEBUG: headers"
		self.wfile.write(json.dumps(result))
		print "DEBUG: out written"

def run(server_class=HTTPServer, handler_class=S, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'DEBUG: Starting httpd...'
    httpd.serve_forever()

run()
