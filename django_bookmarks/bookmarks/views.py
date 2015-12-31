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
from datetime import datetime,timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def main_page(request):
  shared_bookmarks = SharedBookmark.objects.order_by(
    '-date'
  )[:10]
  variables = RequestContext(request, {
    'shared_bookmarks': shared_bookmarks
  }) 
  return render_to_response('main_page.html', variables)

def user_page(request,username):
  user=get_object_or_404(User,username=username)
  query_set=bookmark.objects.order_by('-id')
  pag=Paginator(query_set,3)
  page = request.GET.get('page')
  is_friend=Friendship.objects.filter(
    from_friend=request.user,
    to_friend=user)
  try:
    bookmarks = pag.page(page)
  except PageNotAnInteger:
    bookmarks = pag.page(1)
  except EmptyPage:
    bookmarks = pag.page(pag.num_pages)
  var=RequestContext(request,{
		'username':username,
		'bookmarks':bookmarks,
		'show_tags':True,
		'show_edit':username==request.user.username,
    'show_paginator':pag.num_pages>1,
    'count':pag.num_pages,
    'is_friend':is_friend
    })
  return render_to_response('user_page.html',var)

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')

def tag_page(request,tag_name):
	tag=get_object_or_404(Tag,name=tag_nfame)
	bookmarks=tag.bookmarks.order_by('-id')
	var=RequestContext(request,{

		'tag_name':tag_name,
		'bookmarks':bookmarks,
		'show_tags':True,
		'show_user':True
		})
	return render_to_response('tag_page.html',var)

[ 203 ]
def register_page(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      user = User.objects.create_user(
        username=form.cleaned_data['username'],
        password=form.cleaned_data['password1'],
        email=form.cleaned_data['email']
      )
      if 'invitation' in request.session:
        # Retrieve the invitation object.
        invitation = \
          Invitation.objects.get(id=request.session['invitation'])
        # Create friendship from user to sender.
        friendship = Friendship(
          from_friend=user,
          to_friend=invitation.sender
        )
        friendship.save()
        # Create friendship from sender to user.
        friendship = Friendship (
          from_friend=invitation.sender,
          to_friend=user
        )
        friendship.save()
        # Delete the invitation from the database and session.
        invitation.delete()
        del request.session['invitation']
      return HttpResponseRedirect('/register/success/')
  else:
    form = RegistrationForm()
  variables = RequestContext(request, {
    'form': form
  })
  return render_to_response('registration/register.html', variables)

@login_required 
def bookmark_save_page(request):
  if request.method == 'POST':
    form = BookmarkSaveForm(request.POST)
    if form.is_valid():
      bookmark1 = _bookmark_save(request, form)
      return HttpResponseRedirect(
        '/user/%s/' % request.user.username
      )
  elif request.GET.has_key('url'):
    url = request.GET['url']
    title = ''
    tags = ''
    try:
      link = Link.objects.get(url=url)
      bookmark1 = bookmark.objects.get(
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
  return render_to_response('bookmark_save.html', variables)

def tag_cloud_page(request):
 	MAX_WEIGHT=6
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
    variables = RequestContext(request, { 'form': form,
      'bookmarks': bookmarks,
      'show_results': show_results,
      'show_tags': True,
      'show_user': True
    })
    if request.GET.has_key('ajax'):
      return render_to_response('bookmark_list.html',variables)
    else:
      return render_to_response('search.html', variables)



def _bookmark_save(request, form):
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
  # Share on the main page if requested.
  if form.cleaned_data['share']:
    shared_bookmark, created = SharedBookmark.objects.get_or_create(
      bookmark=bookmark1
    )
    if created:
      shared_bookmark.users_voted.add(request.user)
      shared_bookmark.save()
  # Save bookmark to database and return it.
  bookmark1.save()
  return bookmark1

@login_required
def bookmark_vote_page(request):
  if request.GET.has_key('id'):
    try:
      id=request.GET['id']
      shared_bookmark=SharedBookmark.objects.get(id=id)
      users_voted=shared_bookmark.users_voted.filter(username=request.user.username)
      if not users_voted:
        shared_bookmark.votes+=1
        shared_bookmark.users_voted.add(request.user)
        shared_bookmark.save()
    except ObjectDoesNotExist:
      raise Http404('Bookmark not found.')
  if request.META.has_key('HTTP_REFERER'):
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
  return HttpResponseRedirect('/')
 
def popular_page(request):
  today = datetime.today()
  yesterday = today - timedelta(1)
  shared_bookmarks = SharedBookmark.objects.filter(
    date__gt=yesterday
  )
  shared_bookmarks = shared_bookmarks.order_by(
    '-votes'
  )[:10]
  variables = RequestContext(request, {
    'shared_bookmarks': shared_bookmarks
  }) 
  return render_to_response('popular_page.html', variables)

def friends_page(request,username):
  user=get_object_or_404(User,username=username)
  friends= \
  [friendship.to_friend for friendship in user.friend_set.all()]
  friend_bookmarks = \
    bookmark.objects.filter(user__in=friends).order_by('-id')
  variables=RequestContext(request, {
    'username':username,
    'friends':friends,
    'bookmarks':friend_bookmarks,
    'show_tags':True,
    'show_user':True
    })
  return render_to_response('friends_page.html',variables)
@login_required
def friend_add(request):
  if request.GET.has_key('username'):
    friend=get_object_or_404(User,username=request.GET['username'])
    friendship=Friendship(from_friend=request.user,
      to_friend=friend)
    friendship.save()
    return HttpResponseRedirect('/friends/%s'% request.user.username)
  else:
    pass  
@login_required
def friend_invite(request):
  if request.method == 'POST':
    form = FriendInviteForm(request.POST)
    if form.is_valid():
      invitation = Invitation(
        name = form.cleaned_data['name'],
        email = form.cleaned_data['email'],
        code = User.objects.make_random_password(20),
        sender = request.user
      )
      invitation.save()
      invitation.send()
      return HttpResponseRedirect('/friend/invite/')
  else:
    form = FriendInviteForm()
  variables = RequestContext(request, {
    'form': form
  })
  return render_to_response('friend_invite.html', variables)

def friend_accept(request,code):
  invitation=get_object_or_404(Invitation,code=code)
  request.session['invitation']=invitation.id
  return HttpResponseRedirect('/register/')