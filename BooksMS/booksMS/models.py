from django.db import models

class Authors(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200, blank=True)
    rating = models.IntegerField(null=True,blank=True)
    summary = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class Books(models.Model):
    title = models.CharField(max_length=200)
    pub_year = models.DateField("date published")
    coverimg = models.CharField(max_length=200, blank=True)
    rating = models.IntegerField(blank=True,null=True)
    genre = models.CharField(max_length=200, blank=True)
    author=models.ForeignKey(Authors,on_delete=models.SET_NULL,null=True,blank=True)

    @property
    def author_name(self):
        return self.author.name

    def __str__(self):
        return self.title

