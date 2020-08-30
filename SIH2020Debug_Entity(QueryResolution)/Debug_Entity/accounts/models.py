from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class extendeduser(models.Model):
    phone=models.CharField(max_length=12)
    cat=models.CharField(max_length=10)
    town=models.CharField(max_length=50)
    user=models.OneToOneField(User,on_delete=models.CASCADE)