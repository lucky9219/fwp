from django.db import models
from django.contrib.auth.models import User
class Link(models.Model):
	url=models.URLField(unique=True)
	def __str__(self):
		return self.url

class bookmark(models.Model):
	title=models.CharField(max_length=200)
	user=models.ForeignKey(User)
	link=models.ForeignKey(Link)
	def __str__(self):
		return '%s,%s'%(self.user.username,self.link.url)	

class Tag(models.Model):
	name=models.CharField(max_length=200)
	bookmarks=models.ManyToManyField(bookmark)
	def __str__(self):
		return self.name

class SharedBookmark(models.Model):
	bookmark=models.OneToOneField(bookmark)
	date=models.DateTimeField(auto_now_add=True)
	votes=models.IntegerField(default=1)
	users_voted=models.ManyToManyField(User)
	def __str__(self):
		return '%s,%s' %self.bookmark,self.votes
		