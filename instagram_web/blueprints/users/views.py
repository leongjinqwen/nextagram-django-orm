from flask import Blueprint, render_template,request,redirect,url_for,flash
from instagram.models.user import User
from flask_login import current_user,login_required,login_user
import datetime
from werkzeug.utils import secure_filename
from instagram_web.util.aws_helper import upload_file_to_s3,allowed_file

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = User(username=username,email=email,password=password)
    if user.save():
        login_user(user)
        flash("successfully create a new user",'info')
        return redirect(url_for('users.new'))
    else:
        for error in user.errors:
            flash(error,'danger')
        return render_template('users/new.html')

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.objects.get(username=username)
    return render_template("users/show.html",user=user)

@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.objects.get(id=id)
    return render_template("users/edit.html",user=user)
    

@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    user = User.objects.get(id=id)
    if current_user == user :
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.password = request.form.get('password')
        if user.save():
            flash("Successfully updated.","success")
            return redirect(url_for('users.edit',id=id))
        else:
            errors = user.errors
            for error in errors:
                flash(error,"danger")
            return render_template("users/edit.html",user=user)
    else:
        flash(f"You are not allowed to update {user.username}'s profile",'danger')
        return render_template("users/edit.html",user=user)


@users_blueprint.route('/upload', methods=['POST'])
def upload():
    # check whether an input field with name 'user_file' exist
    if 'user_file' not in request.files:
        flash('No user_file key in request.files')
        return redirect(url_for('users.edit',id=current_user.id))

    # after confirm 'user_file' exist, get the file from input
    file = request.files['user_file']

    # check whether a file is selected
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('users.edit',id=current_user.id))

    # check whether the file extension is allowed (eg. png,jpeg,jpg,gif)
    if file and allowed_file(file.filename):
        file.filename = secure_filename(f"{str(datetime.datetime.now())}{file.filename}")
        output = upload_file_to_s3(file) 
        if output:
            user = User.objects.get(id=current_user.id)
            user.profile_image = file.filename
            user.save()
            # User.update(profile_image=file.filename).where(User.id==current_user.id).execute()
            flash("Profile image successfully uploaded","success")
            return redirect(url_for('users.show',username=current_user.username))
        else:
            flash(output,"danger")
            return redirect(url_for('users.edit',id=current_user.id))

    # if file extension not allowed
    else:
        flash("File type not accepted,please try again.")
        return redirect(url_for('users.edit',id=current_user.id))