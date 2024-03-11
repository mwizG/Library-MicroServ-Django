from django.db import models

# Create your models here.
class Books(models.Model):
    title = models.CharField(max_length=200)
    pub_year = models.DateField("date published")
    coverimg = models.CharField(max_length=200, blank=True)
    rating = models.IntegerField(blank=True)
    genre = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

class Authors(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200, blank=True)
    rating = models.IntegerField()
    summary = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name
