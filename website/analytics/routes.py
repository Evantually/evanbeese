from flask import render_template, request, Blueprint, url_for, jsonify, redirect
from website import db
from website.analytics.forms import ClassificationForm
from website.analytics.utils import get_model_response, prepare_img
from rq.job import Job

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route("/analytics", methods=['GET', 'POST'])
def analytics():
    form = ClassificationForm()
    if form.validate_on_submit():
        print(form)
        if form.picture.data:
            job_id = get_model_response(form.picture.data)
            return redirect(f'/analytics/{job_id}')
        # return jsonify(picture_file)
        return render_template('results.html', results=picture_file, form=form, picture_path=picture_path)
    return render_template("analytics.html", title='Data Analytics', form=form)

@analytics_bp.route('/analytics/<jobID>', methods=['GET'])
def analytics_response(jobID):
    job = Job.fetch(jobID)
    if not job.is_finished:
        return 'Not yet', 202
    else:
        return str(job.result)