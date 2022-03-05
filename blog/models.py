from django.db import models

from user.models import User


class Blog(models.Model):
  title = models.CharField(max_length=200)
  text = models.TextField()
  thumbnail = models.TextField(blank=True, null=True)
  created_date = models.DateField(auto_now=True)
  last_modified = models.DateField(auto_now_add=True)
  upvote = models.IntegerField(default=0)
  downvote = models.IntegerField(default=0)
  author = models.ForeignKey(User, models.CASCADE)