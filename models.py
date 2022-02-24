from django.db import models
from django.contrib.auth.forms import User


# Create your models here.
class Blog(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    distription = models.TextField()
    current_time = models.DateField(auto_now_add=True)
    update_time = models.DateField(auto_created=True)


class MyBlog(models.Model):
    author =models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    discription = models.TextField()
