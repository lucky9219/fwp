from django.db import models
from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from django.core.mail import send_mail

class Link(models.Model):
	url=models.URLField(unique=True)
	def __unicode__(self):
		return self.url


class bookmark(models.Model):
	title=models.CharField(max_length=200)
	user=models.ForeignKey(User)
	link=models.ForeignKey(Link)
	def __unicode__(self):
		return '%s'%(self.user.username)	
	

class Tag(models.Model):
	name=models.CharField(max_length=200)
	bookmarks=models.ManyToManyField(bookmark)
	def __unicode__(self):
		return self.name

class SharedBookmark(models.Model):
	bookmark=models.OneToOneField(bookmark)
	date=models.DateTimeField(auto_now_add=True)
	votes=models.IntegerField(default=1)
	users_voted=models.ManyToManyField(User)
	def __unicode__(self):
		return '%s %s' %(self.bookmark,self.date)

class Friendship(models.Model):
  from_friend = models.ForeignKey(
    User, related_name='friend_set'
  )
  to_friend = models.ForeignKey(
    User, related_name='to_friend_set'
  )
  def __str__(self):
    return '%s, %s' % (
      self.from_friend.username,
      self.to_friend.username
    )
    class Meta:
    	unique_together = (('to_friend', 'from_friend'), )

class Invitation(models.Model):
  name = models.CharField(max_length=50)
  email = models.EmailField()
  code = models.CharField(max_length=20)
  sender = models.ForeignKey(User)
  def send(self):
  	subject='Invitation to join MovieMania'
  	link='http://%s/friend/accept/%s/'%(settings.SITE_HOST,
  		self.code
  		)
  	template=get_template('invitation_email.txt')
  	context=Context({
  		'name':self.name,
  		'link':link,
  		'sender':self.sender.username,
  		})
  	message=template.render(context)
  	send_mail(
  		subject,message,
  		settings.DEFAULT_FROM_EMAIL,[self.email]
  		)
  def __str__(self):
    return '%s, %s' % (self.sender.username, self.email)
 