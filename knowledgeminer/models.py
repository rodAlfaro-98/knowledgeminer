from django.db import models
from django.conf import settings

# Create your models here.
class File(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    path = models.CharField(max_length=200)
    columns = models.TextField()

    def get_columns(self):
        string = self.columns[1:-1]
        list = string.split(',')
        toReturn = []
        for i in list:
            toReturn.append(i.replace('\'',''))
        return toReturn