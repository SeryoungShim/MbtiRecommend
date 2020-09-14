from django.db import models


# Create your models here.

class DramaInfo(models.Model):
    title = models.CharField(max_length=100)
    image = models.TextField()
    plot = models.TextField()
    site = models.TextField()

    
    def __str__(self):
        return self.title

class Character(models.Model):
    drama =  models.ForeignKey('DramaInfo', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    poster = models.TextField()
    description = models.TextField()
    personal = models.TextField()
    mbti = models.CharField(max_length=5)

    def __str__(self):
        return self.name

    # class Meta:
    # verbose_name = 'character name'
    # verbose_name_plural = 'character name'