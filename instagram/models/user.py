import re
import os
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from werkzeug.security import generate_password_hash
from .base_model import BaseModel
from flask_login import UserMixin
# from django_hybrid_attributes import hybrid_metho, HybridQuerySet

class UserValidation():
    @classmethod
    def validate_length(klass, value):
        if len(value) < 8:
            raise ValidationError(
                _('%(value)s is too short'),
                params={'value': value},
            )

    @classmethod
    def validate_regex(klass, value):
        password_regex = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
        if re.search(password_regex,value) == None:
            raise ValidationError(
                _('Password need to have minimum eight characters, at least one letter and one number'),
                params={'value': value},
            )
        
class User(UserMixin,BaseModel):
    username = models.CharField(max_length=255,unique=True,null=False,validators=[UserValidation.validate_length])
    email =  models.CharField(max_length=255,unique=True,null=False)
    password = models.CharField(max_length=255,validators=[UserValidation.validate_regex])
    role = models.CharField(max_length=255, default="user")
    profile_image = models.TextField(max_length=255,default="blank-profile-picture.png")
    private = models.BooleanField(default=False)


    @classmethod
    def get_or_none(self, **kwargs):
        try:
            return User.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    def profile_image_url(self):
        return os.environ['S3_DOMAIN'] + self.profile_image

    def follow(self,idol):
        from .fanidol import FanIdol
        # check if has relationship in database
        if self.follow_status(idol)==None:
            FanIdol(fan=self,idol=idol).save()
            return True
        else:
            return 0

    def unfollow(self,idol):
        from .fanidol import FanIdol
        return FanIdol.objects.get(fan=self,idol=idol).delete() # return (1, {'instagram.FanIdol': 1})

    def approve_request(self,fan):
        from .fanidol import FanIdol
        relationship = FanIdol.objects.get(fan=fan,idol=self)
        relationship.approved = True
        relationship.save()
        # FanIdol.update(approved=True).where(FanIdol.fan==fan.id,FanIdol.idol==self.id).execute()
        return True

    def follow_status(self,idol):
        from .fanidol import FanIdol
        try:
            return FanIdol.objects.get(fan=self,idol=idol)
        except ObjectDoesNotExist:
            return None

    def get_request(self):
        from .fanidol import FanIdol
        return FanIdol.objects.filter(idol=self,approved=False)
        # return FanIdol.select().where(FanIdol.idol==self.id,FanIdol.approved==False)

    def followers(self):
        from .fanidol import FanIdol
        # to get all fans
        fans = FanIdol.objects.filter(idol=self,approved=True)
        # fans = FanIdol.select(FanIdol.fan).where(FanIdol.idol==self.id,FanIdol.approved==True)
        return [ fan.fan for fan in fans ]

    def followings(self):
        from .fanidol import FanIdol
        # to get all idols
        idols = FanIdol.objects.filter(fan=self,approved=True)
        # idols = FanIdol.select(FanIdol.idol).where(FanIdol.fan==self.id,FanIdol.approved==True)
        return [ idol.idol for idol in idols ]
        # return User.select().where(User.id.in_(idols))

    