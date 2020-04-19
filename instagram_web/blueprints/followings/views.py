from flask import Blueprint, render_template,request,redirect,url_for,flash
from instagram.models.user import User
from instagram.models.fanidol import FanIdol
from flask_login import current_user, login_required
import os


followings_blueprint = Blueprint('followings',
                            __name__,
                            template_folder='templates')

@followings_blueprint.route('/<idol_id>')
@login_required
def create(idol_id):
    idol = User.objects.get(id=idol_id)
    if current_user.follow(idol):
        flash(f"You send follow request to {idol.username}","success")
        return redirect(url_for('users.show',username=idol.username))
    else:
        flash(f"You not yet follow {idol.username}","danger")
        return render_template('users/show.html',username=idol.username)

@followings_blueprint.route('/<idol_id>/unfollow')
@login_required
def unfollow(idol_id):
    idol = User.objects.get(id=idol_id)
    if current_user.unfollow(idol):
        flash(f"You unfollow {idol.username}","success")
        return redirect(url_for('users.show',username=current_user.username))
    else:
        flash("Something went wrong, try again later.","danger")
        return render_template('users/show.html',username=current_user.username)

@followings_blueprint.route('/<fan_id>/update')
@login_required
def update(fan_id): # to approve
    fan = User.objects.get(id=fan_id)
    if current_user.approve_request(fan):
        flash(f"You approved follow request from {fan.username}","success")
        return redirect(url_for('users.show',username=current_user.username))
    else:
        flash("Something went wrong, try again later.","danger")
        return render_template('users/show.html',username=current_user.username)


@followings_blueprint.route('/<fan_id>/delete')
@login_required
def destroy(fan_id): # to delete
    idol = User.objects.get(id=current_user.id)
    fan = User.objects.get(id=fan_id)
    if fan.unfollow(idol):
        flash(f"You deleted request from {fan.username}","success")
        return redirect(url_for('users.show',username=current_user.username))
    else:
        flash("Something went wrong, try again later.","danger")
        return render_template('users/show.html',username=current_user.username)
