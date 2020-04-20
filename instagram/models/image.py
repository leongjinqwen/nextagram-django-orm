import os
from django.db import models
from .base_model import BaseModel
from .user import User
from django_hybrid_attributes import hybrid_property

class Image(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    image_path = models.TextField(max_length=255)

    @hybrid_property
    def image_path_url(self):
        return os.environ['S3_DOMAIN'] + self.image_path
