from base.forms import UserCreationForm
from django.contrib import admin
from base.models import User, Post, ReplyPost, BlockUser, FollowUser, FavoritePost, AgreePost, LikeReply
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from base.models.reply_models import ReplyReply
# Register your models here.
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password',)}),
        (None, {'fields': ('is_active', 'is_admin',)}),
    )
 
    list_display = ('username', 'email', 'is_active',)
    list_filter = ()
    ordering = ()
    filter_horizontal = ()
 
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'is_active',)}),
    )
 
    add_form = UserCreationForm
 
 
admin.site.register(BlockUser)
admin.site.register(FollowUser)
admin.site.register(FavoritePost)
admin.site.register(LikeReply)
admin.site.register(AgreePost)
admin.site.register(ReplyReply)
admin.site.register(ReplyPost)
admin.site.register(Post)
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)