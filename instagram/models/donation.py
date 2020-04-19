from .base_model import BaseModel
from .user import User
from .image import Image
from django.db import models

class Donation(BaseModel):
    donor = models.ForeignKey(User, related_name='endorsements', on_delete=models.CASCADE)
    image = models.ForeignKey(Image, related_name='endorsements', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20,decimal_places=2,default=0)
   
  

   