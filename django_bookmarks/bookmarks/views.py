from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
def main_page(request):
	return render_to_response('main_page.html',RequestContext(request))


def user_page(request,username):
	user=get_object_or_404(User,username=username)
	bookmarks=user.bookmark_set.order_by('-id')
	var=RequestContext(request,{
		'username':username,
		'bookmarks':bookmarks,
		'show_tags':True,
		'show_edit':username==request.user.username
		})
	return render_to_response('user_page.html',var)

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')

def tag_page(request,tag_name):
	tag=get_object_or_404(Tag,name=tag_name)
	bookmarks=tag.bookmarks.order_by('-id')
	var=RequestContext(request,{

		'tag_name':tag_name,
		'bookmarks':bookmarks,
		'show_tags':True,
		'show_user':True
		})
	return render_to_response('tag_page.html',var)

def register_page(request):
	if request.method=='POST':
		form=RegistrationForm(request.POST)
		if form.is_valid():
			user=User.objects.create_user(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password1'],
				email=form.cleaned_data['email']
				)
			return HttpResponseRedirect('/register/success/')
	else:
		form=RegistrationForm()
	variables=RequestContext(request,{'form':form})
	return render_to_response(
			'registration/register.html',variables)


def bookmark_save_page(request):
  if request.method == 'POST':
    form = BookmarkSaveForm(request.POST)
    if form.is_valid():
# Create or get link.
      link, dummy = Link.objects.get_or_create(
        url=form.cleaned_data['url']
      )
      # Create or get bookmark.
      bookmark1, created = bookmark.objects.get_or_create(
        user=request.user,
        link=link
      )
      # Update bookmark title.
      bookmark1.title = form.cleaned_data['title']
      # If the bookmark is being updated, clear old tag list.
      if not created:
        bookmark1.tag_set.clear()
      # Create new tag list.
      tag_names = form.cleaned_data['tags'].split()
      for tag_name in tag_names:
        tag, dummy = Tag.objects.get_or_create(name=tag_name)
        bookmark1.tag_set.add(tag)
      # Save bookmark to database.
      bookmark1.save()
      return HttpResponseRedirect(
        '/user/%s/' % request.user.username
      )
  else:
    form = BookmarkSaveForm()
  variables = RequestContext(request, {
    'form': form
  })
  return render_to_response('bookmark_save.html', variables)

def tag_cloud_page(request):
 	MAX_WEIGHT=5
 	tags=Tag.objects.order_by('name')
 	min_count=max_count=tags[0].bookmarks.count()
 	for tag in tags:
 		tag.count=tag.bookmarks.count()
 		if tag.count<min_count:
 			min_count=tag.count
 		if max_count<tag.count:
 			max_count=tag.count
 	range=float(max_count-min_count)
 	if range==0.0:
 		range=1.0
 	for tag in tags:
 		tag.weight=int(MAX_WEIGHT*(tag.count-min_count)/range)
 	var=RequestContext(request,{
 		'tags':tags
 		})
 	return render_to_response("tag_cloud_page.html",var)
