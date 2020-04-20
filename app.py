import os
import config
from flask import Flask
from django.apps import apps
from django.conf import settings
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

apps.populate(settings.INSTALLED_APPS)

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


# @app.before_request
# def before_request():
#     db.connect()


# @app.teardown_request
# def _db_close(exc):
#     if not db.is_closed():
#         print(db)
#         print(db.close())
#     return exc

csrf = CSRFProtect()
csrf.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "sessions.new" 
login_manager.login_message = "Please log in before proceeding"
login_manager.login_message_category = "danger"

@login_manager.user_loader
def load_user(user_id):
    from instagram.models.user import User
    return User.objects.get(id=user_id)