from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=140)
    bio = models.CharField(max_length=220)

class MicroPost(models.Model):
    author = models.ForeignKey(Author)
    title = models.CharField(max_length=140)
    body = models.TextField()

class Follow(models.Model):
    author = models.ForeignKey(Author, related_name='following')
    follower = models.ForeignKey(Author, related_name='followers')

