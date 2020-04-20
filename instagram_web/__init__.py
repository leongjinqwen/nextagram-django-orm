from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
from instagram_web.blueprints.followings.views import followings_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from flask_login import current_user, login_required

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(donations_blueprint, url_prefix="/donations")
app.register_blueprint(followings_blueprint, url_prefix="/followings")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
@login_required
def home():
    from instagram.models.image import Image
    from instagram.models.user import User
    from instagram.models.fanidol import FanIdol
    # show all idols
    idols = current_user.followings()
    # idols = User.select().join(FanIdol,on=(FanIdol.idol==User.id)).where(FanIdol.fan==current_user.id)
    idol_list = [x.id for x in idols]
    idol_list.append(current_user.id)
    images = Image.objects.filter(user__in=idol_list)
    # images = Image.select().where((Image.user.in_(idol_list))).order_by(Image.created_at.desc())
    not_following = User.objects.exclude(id__in=idol_list)
    # not_following = User.select().where(User.id.not_in(idol_list))
    return render_template('home.html',images=images,users=idols,not_following=not_following)
