from flask import render_template, request, Blueprint, url_for
from website import db

jobs = Blueprint('jobs', __name__)

@jobs.route("/resume/uofmn")
def uofmn():
    return render_template("uofmn.html", title='University of Minnesota')

@jobs.route("/resume/wellsfargo")
def wellsfargo():
    return render_template("wellsfargo.html", title='Wells Fargo')

@jobs.route("/resume/thrivent")
def thrivent():
    return render_template("thrivent.html", title='Thrivent Financial')