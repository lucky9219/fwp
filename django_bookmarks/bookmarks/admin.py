from django.contrib import admin
from .models import *


class BookmarkAdmin(admin.ModelAdmin):
	list_display = ['title', 'link','user']
	search_fields=['title']
	list_filter = ('user', )
  	#ordering = ('title', )

class LinkAdmin(admin.ModelAdmin):
	list_display=['url']
	search_fields=['url']

class SharedBookmarkAdmin(admin.ModelAdmin):
	list_display=['bookmark']
	search_fields=['bookmark']

class TagAdmin(admin.ModelAdmin):
	list_display=['name']
	search_fields=['name']
class FriendshipAdmin(admin.ModelAdmin):
	list_display=['from_friend','to_friend']
	search_fields=['from_friend']
class InvitationAdmin(admin.ModelAdmin):
	list_display=['name']
	search_fields=['name']


admin.site.register(Invitation,InvitationAdmin)
admin.site.register(Friendship,FriendshipAdmin)
admin.site.register(Link,LinkAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(bookmark,BookmarkAdmin)
admin.site.register(SharedBookmark,SharedBookmarkAdmin)

