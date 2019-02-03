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

q = Queue(connection=conn)

def get_model_response(img):
    print(f'get_model_response img: {img}')
    result = q.enqueue_call(func=prepare_img, args=([img]), result_ttl=600)
    while result.result is None:
        pass
    return result.result

def reload_model():
    global model
    global graph
    # print(os.path.join(current_app.root_path, 'static','models','xception_model.h5'))
    model = load_model(os.path.join('website','static','models','xception_model.h5'))
    graph = tf.get_default_graph()
    # graph = K.get_session().graph

def prepare_img(img):
    global model
    global graph
    job = Job.fetch(get_current_job(), connection=conn)
    print(f'The current job is {job}.')
    print(f'img: {img}')
    data = {}
    random_hex = secrets.token_hex(8)
    print(f'random_hex: {random_hex}')
    _, f_ext = os.path.splitext(img.filename)
    print(f'f_ext: {f_ext}')
    picture_fname = f'{random_hex}{f_ext}'
    print(f'picture_fname: {picture_fname}')
    picture_path = os.path.join(current_app.root_path, 'static/uploads', picture_fname)
    print(f'picture_path: {picture_path}')
    output_size = (299, 299)
    i = Image.open(img)
    i.thumbnail(output_size)
    i.save(picture_path)
    im = keras.preprocessing.image.load_img(picture_path, target_size=output_size, grayscale=False)
    print(f'im: {im}')
    prepared_img = img_to_array(im)
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