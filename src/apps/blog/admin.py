from django.contrib import admin

from .forms import PornoStarAdminForm
from .models import PornoStar, Comment, CommentUser


@admin.register(PornoStar)
class PornoStarAdmin(admin.ModelAdmin):
    form = PornoStarAdminForm
    list_display = ('pk', 'name', 'publish', 'author', 'image', 'status')
    list_display_links = ('pk', 'name')
    list_filter = ('created', 'updated', 'publish', 'status')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'content')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'comment_user', 'status')
    list_filter = ('created', 'updated', 'status', 'pornostar__name')
    search_fields = ('name', 'content')


@admin.register(CommentUser)
class CommentUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    list_display_links = ('name',)
    list_filter = ('name', )
    search_fields = ('name',)
