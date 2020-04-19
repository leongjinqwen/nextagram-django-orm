import os
from django.db import models
from .base_model import BaseModel
from .user import User

class Image(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    image_path = models.TextField(max_length=255)

    def image_path_url(self):
        return os.environ['S3_DOMAIN'] + self.image_path
