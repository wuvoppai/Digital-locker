from django.db import models
import datetime

class Customer(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField(default=10)
    gender = models.CharField(max_length=10)
    email = models.EmailField(max_length=30)
    mobile = models.CharField(max_length=15)
    profile = models.FileField(default=None,null=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30,default='')
    memory = models.IntegerField(default=0)
    total_memory = models.IntegerField(default=5242880)

    def __str__(self):
        return self.username

    def delete(self,*args,**kwargs):
        self.profile.delete()

class Upload(models.Model):
    username = models.CharField(max_length=30)
    file_name = models.CharField(max_length=100)
    storage = models.CharField(max_length=20)
    file = models.FileField()
    date = models.DateField(default=datetime.datetime.now())

    def __str__(self):
        return self.username +' - '+ self.file_name

    def delete(self,*args,**kwargs):
        self.file.delete()
        super().delete(*args,**kwargs)
