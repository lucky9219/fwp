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


@login_required
def bookmark_save_page(request):
  ajax=request.GET.has_key('ajax')
  if request.method == 'POST':
    form = BookmarkSaveForm(request.POST)
    if form.is_valid():
      bookmark1 = _bookmark_save(form)
      if ajax:
      	variables=RequestContext(request,{'bookmarks':[bookmark1],
      		'show_edit':True,
      		'show_tags':True
      		})
      	return render_to_response('bookmark_list.html',variables)
      else:
      	return HttpResponseRedirect('/user/%s/' % request.user.username)
    else:
    	if ajax:
    		return HttpResponse('failure')
  elif request.GET.has_key('url'):
    url = request.GET['url']
    title = ''
    tags = ''
    try:
      link = Link.objects.get(url=url)
      bookmark1 =bookmark.objects.get(
        link=link,
        user=request.user
      )
      title = bookmark1.title
      tags = ' '.join(
        tag.name for tag in bookmark1.tag_set.all()
      )
    except ObjectDoesNotExist:
      pass
    form = BookmarkSaveForm({
      'url': url,
      'title': title,
      'tags': tags
    })
  else:
    form = BookmarkSaveForm()
  variables = RequestContext(request, {
    'form': form
  })
  if ajax:
  	return render_to_response('bookmark_save_form.html', variables)
  else:
  	return render_to_response('bookmark_save.html',variables)

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
@login_required
def search_page(request):
  form = SearchForm()
  bookmarks = []
  show_results = False
  if request.GET.has_key('query'):
    show_results = True
    query = request.GET['query'].strip()
    if query:
      form = SearchForm({'query' : query}) 
      bookmarks = \
        bookmark.objects.filter (title__icontains=query)[:10]
  variables = RequestContext(request, { 
  	'form': form,
    'bookmarks': bookmarks,
    'show_results': show_results,
    'show_tags': True,
    'show_user': True
  })
  if request.GET.has_key('ajax'):
  	return render_to_response('bookmark_list.html',variables)
  else:
  	return render_to_response('search.html', variables)


@login_required
def _bookmark_save(request,form):
  if request.method == 'POST':
    form = BookmarkSaveForm(request.POST)
    if form.is_valid():
   
      link, dummy = Link.objects.get_or_create(
        url=form.cleaned_data['url']
      )
      
      bookmark1, created = bookmark.objects.get_or_create(
        user=request.user,
        link=link
      )
      
      bookmark1.title = form.cleaned_data['title']
      
      if not created:
        bookmark1.tag_set.clear()

      tag_names = form.cleaned_data['tags'].split()
      for tag_name in tag_names:
        tag, dummy = Tag.objects.get_or_create(name=tag_name)
        bookmark1.tag_set.add(tag)
    
      bookmark1.save()
      return bookmark1;


