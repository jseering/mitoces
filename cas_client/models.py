from django.db import models
from django.contrib.auth.models import User

class Outcome(models.Model):
    name        = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    def __unicode__(self):
        return self.name

class Keyword(models.Model):
    name     = models.CharField(max_length=40)
    class Meta:
		ordering = ['name']
    def __unicode__(self):
        return self.name

class Module(models.Model):
    name     = models.CharField(max_length=60)
    # logo     = models.ImageField(path="", match=".*\.png$")
    description = models.TextField()
    link     = models.URLField(max_length=180)
    date     = models.DateTimeField(auto_now_add=True, blank=True)
    creator  = models.ForeignKey(User)
    outcomes = models.ManyToManyField(Outcome)
    keywords = models.ManyToManyField(Keyword)
    def __unicode__(self):
        return self.name

