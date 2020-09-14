from django.db import models

# Create your models here.

class DramaInfo(models.Model):
    title = models.CharField(max_length=100)
    image = models.TextField()
    plot = models.TextField()
    site = models.TextField()

class Character(models.Model):
    drama =  models.ForeignKey(DramaInfo)
    name = models.CharField(max_length=30)
    poster = models.TextField()
    description = models.TextField()
    personal = models.TextField()
    mbti = models.CharField(max_length=5)
