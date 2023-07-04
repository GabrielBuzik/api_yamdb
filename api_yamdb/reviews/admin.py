from django.contrib import admin

from .models import Comment, Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'text',
        'author',
        'score',
        'pub_date'
    )
    list_editable = ('text',)
    search_fields = ('title', 'text',)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'review',
        'text',
        'author',
        'pub_date'
    )
    list_editable = ('text',)
    search_fields = ('review', 'text',)


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
