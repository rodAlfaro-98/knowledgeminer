from django.db import models
from django.conf import settings

# Create your models here.
class File(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    path = models.CharField(max_length=200)