import os
import secrets
import numpy as np
import keras
from keras.preprocessing.image import img_to_array
from keras.applications.xception import (Xception, preprocess_input, decode_predictions)
from keras import backend as K
from flask import current_app
from PIL import Image

def load_model():
    global model
    global graph
    model = Xception(weights="imagenet")
    graph = K.get_session().graph

def prepare_img(img):
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
    
    global graph
    with graph.as_default():
        preds = model.predict(prepared_img)
        results = decode_predictions(preds)
        data['predictions'] = []
        for (imagenetID, label, prob) in results[0]:
            r = {"label": label, "probability": round(100*float(prob),2)}
            data['predictions'].append(r)
    return data, picture_fname