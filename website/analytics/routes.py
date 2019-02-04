from flask import render_template, request, Blueprint, url_for, jsonify, redirect, current_app
from website import db
from website.analytics.forms import ClassificationForm
from website.analytics.utils import get_model_response, prepare_img
from rq.job import Job
from worker import conn
from rq import Queue
import secrets
from PIL import Image
import os
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

analytics_bp = Blueprint('analytics', __name__)

q = Queue(connection=conn)

@analytics_bp.route("/analytics", methods=['GET', 'POST'])
def analytics():
    form = ClassificationForm()
    if form.validate_on_submit():
        print(form)
        if form.picture.data:
            img=form.picture.data
            upload_result = upload(img)
            thumbnail_url1, options = cloudinary_url(upload_result['public_id'], format='jpg', crop='fill', width=299, height=299)
            result = q.enqueue_call(func=prepare_img, args=([thumbnail_url1]), result_ttl=600)
            return redirect(f'/analytics/{result.get_id()}')
        # return jsonify(picture_file)
        return render_template('results.html', results=picture_file, form=form, picture_path=picture_path)
    return render_template("analytics.html", title='Data Analytics', form=form)

@analytics_bp.route('/analytics/<jobID>', methods=['GET'])
def analytics_response(jobID):
    form = ClassificationForm()
    job = Job.fetch(jobID, connection=conn)
    while not job.is_finished and not job.is_failed:
        job = Job.fetch(jobID, connection=conn)
        return 'Currently processing image. Please wait!', 202
    if job.is_failed:
        return str('Sorry. We experienced an error when processing your image.')
    print(job.result[0]['predictions'])
    return render_template('results.html', form=form, results=job.result[0], picture_path=jsonify(job.result[1]))

@analytics_bp.route('/analytics/<jobID>/done', methods=['GET'])
def analytics_done(jobID):
    job = Job.fetch(jobID, connection=conn)
    return str(job.result)