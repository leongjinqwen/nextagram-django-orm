from .base_model import BaseModel
from .user import User
from django.db import models

class FanIdol(BaseModel):
    fan = models.ForeignKey(User, related_name='idols',on_delete=models.CASCADE)
    idol = models.ForeignKey(User, related_name='fans',on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
   
  