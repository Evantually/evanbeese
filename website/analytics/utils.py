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
from website import db

q = Queue(connection=conn)

# def set_task_progress(progress):
#     job = get_current_job()
#     if job:
#         complete = False
#         job.meta['progress'] = progress
#         job.save_meta()
#         if progress >= 100:
#             complete = True
#         newProg = {'id': job.get_id(), 'progress': progress, 'complete': complete}
#         db.tasks.update_one({'id': job.get_id()}, {'$set': newProg}, upsert=False)

def get_model_response(jobID):
    return db.tasks.find_one({'id': jobID})

def reload_model():
    global model
    global graph
    model = load_model(os.path.join('website','static','models','xception_model.h5'))
    graph = tf.get_default_graph()

def prepare_img(picture_path):
    global model
    global graph
    data = {}
    output_size=(299,299)
    response = requests.get(picture_path)
    img = Image.open(BytesIO(response.content))
    prepared_img = img_to_array(img)
    prepared_img = np.expand_dims(prepared_img, axis=0)
    prepared_img = preprocess_input(prepared_img)
    with graph.as_default():
        preds = model.predict(prepared_img, verbose=1)
        results = decode_predictions(preds)
        data['predictions'] = []
        for (imagenetID, label, prob) in results[0]:
            r = {"label": label, "probability": round(100*float(prob),2)}
            data['predictions'].append(r)
    return data, picture_path

reload_model()