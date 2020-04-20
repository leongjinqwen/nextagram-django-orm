import os
import dj_database_url

DATABASES = { 
    'default': dj_database_url.config(default=os.environ['DATABASE_URL']) 
}

INSTALLED_APPS = ( 'instagram', )

SECRET_KEY = os.environ['SECRET_KEY']


