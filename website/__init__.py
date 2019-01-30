from flask import Flask
from flask_pymongo import PyMongo
from website.config import Config
from flask_track_usage import TrackUsage
from flask_track_usage.storage.mongo import MongoStorage

db = PyMongo()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    t = TrackUsage(app, [MongoStorage('PersonalWebsite', 'tracking', Config.MONGO_URI)])

    from website.main.routes import main
    from website.jobs.routes import jobs
    from website.analytics.routes import analytics_bp
    app.register_blueprint(main)
    app.register_blueprint(jobs)
    app.register_blueprint(analytics_bp)
    t.include_blueprint(main)
    
    return app