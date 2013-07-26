from django.db import models
from django.contrib.auth.models import User

class Module(models.Model):
    name     = models.CharField(max_length=30)
    logo     = models.FilePathField(path="", match=".*\.png$")
    link     = models.URLField(max_length=100)
    date     = models.DateTimeField('date created')
    creator  = models.ForeignKey(User)
    def __unicode__(self):
        return self.name

class Outcome(models.Model):
    name        = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    module      = models.ForeignKey(Module) 
    def __unicode__(self):
        return self.name

class Keyword(models.Model):
    name     = models.CharField(max_length=30)
    module   = models.ForeignKey(Module)
    def __unicode__(self):
        return self.name
