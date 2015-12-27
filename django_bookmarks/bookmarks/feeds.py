from django.contrib.syndication.feeds import Feed
from bookmarks.models import Bookmark
class RecentBookmarks(Feed):
  title = 'Django Bookmarks | Recent Bookmarks'
  link = '/feeds/recent/'
  description = 'Recent bookmarks posted to Django Book'
  def items(self):
    return Bookmark.objects.order_by('-id')[:10]