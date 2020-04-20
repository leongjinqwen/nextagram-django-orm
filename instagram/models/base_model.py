import os
import datetime
from django.db import models
from django.core.exceptions import ValidationError

class MyModelBase(models.base.ModelBase):
    def __new__(cls, name, bases, attrs, **kwargs):
        if name != "BaseModel":
            class Meta:
                db_table = name.lower()

            attrs["Meta"] = Meta

        r = super().__new__(cls, name, bases, attrs, **kwargs)
        return r


class BaseModel(models.Model, metaclass=MyModelBase):
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super(BaseModel, self).save(*args, **kwargs)
            return True
        except ValidationError as err:
            # self.errors = err.message_dict # return dict >> {'password': ['12345678 need to have minimum eight characters, at least one letter and one number'], 'email': ['User with this Email already exists.']}
            self.errors = err.messages # return a list of error messages
            return False

    class Meta:
        abstract = True
