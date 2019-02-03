import os
import secrets
import numpy as np
import keras
import tensorflow as tf
from keras.preprocessing.image import img_to_array
from keras.applications.xception import (Xception, preprocess_input, decode_predictions)
from keras.models import load_model
from keras import backend as K
from flask import current_app, url_for
from PIL import Image
from rq import Queue, get_current_job
from rq.job import Job
from worker import conn
from io import BytesIO
import requests

q = Queue(connection=conn)

def get_model_response(img):
    print(f'get_model_response img: {img}')
    result = q.enqueue_call(func=prepare_img, args=([img]), result_ttl=600)
    return result.key

def reload_model():
    global model
    global graph
    # print(os.path.join(current_app.root_path, 'static','models','xception_model.h5'))
    model = load_model(os.path.join('website','static','models','xception_model.h5'))
    graph = tf.get_default_graph()
    # graph = K.get_session().graph

def prepare_img(picture_path):
    global model
    global graph
    graph = tf.get_default_graph()
    data = {}
    output_size=(299,299)
    response = requests.get(picture_path)
    img = Image.open(BytesIO(response.content))
    # im = keras.preprocessing.image.load_img(picture_path, target_size=output_size, grayscale=False)
    # print(f'im: {im}')
    prepared_img = img_to_array(img)
    prepared_img = np.expand_dims(prepared_img, axis=0)
    prepared_img = preprocess_input(prepared_img)
    print(f'prepared_img: {prepared_img}')

    print(f'graph: {graph}')
    with graph.as_default():
        preds = model.predict(prepared_img, verbose=1)
        print(f'preds: {preds}')
        results = decode_predictions(preds)
        print(f'results: {results}')
        data['predictions'] = []
        for (imagenetID, label, prob) in results[0]:
            r = {"label": label, "probability": round(100*float(prob),2)}
            data['predictions'].append(r)
        print(f'data: {data}')
    return data, picture_fname