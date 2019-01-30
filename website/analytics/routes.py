from flask import render_template, request, Blueprint, url_for, jsonify
from website import db
from website.analytics.forms import ClassificationForm
from website.analytics.utils import get_model_response

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route("/analytics", methods=['GET', 'POST'])
def analytics():
    form = ClassificationForm()
    if form.validate_on_submit():
        print(form)
        if form.picture.data:
            picture_file, picture_path = get_model_response(form.picture.data)
        # return jsonify(picture_file)
        return render_template('results.html', results=picture_file, form=form, picture_path=picture_path)
    return render_template("analytics.html", title='Data Analytics', form=form)