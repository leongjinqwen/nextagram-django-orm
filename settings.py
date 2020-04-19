import os
import dj_database_url

DATABASES = { 
    'default': dj_database_url.config(default=os.environ['DATABASE_URL']) 
}

INSTALLED_APPS = ( 'instagram', )

SECRET_KEY = os.environ['SECRET_KEY']


# do we still need database.py?
# how to generate hash password with model validator?
# if using self.validate() can generate hash pw as usual
# do we need to keep hybrid property? (import from playhouse)
# replace backref with related_name, but need to use all() >> eg. for image in user.images.all()