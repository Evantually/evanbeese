from flask import render_template, request, Blueprint, url_for
from website import db

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    profile_picture = url_for('static', filename='img/profile.jpg')
    return render_template("index.html", profile_picture=profile_picture)

@main.route("/webdev")
def webdev():
    return render_template("webdev.html", title='Web Development')

@main.route("/visualizations")
def visualizations():
    return render_template("visualizations.html", title='Data Visualization')

@main.route("/resume")
def resume():
    return render_template("resume.html", title='Resume')

@main.route("/general-coding")
def general():
    return render_template("general.html", title='General Coding')

@main.route("/contact")
def contact():
    return render_template("general.html", title='General Coding')