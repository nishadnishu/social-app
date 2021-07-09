from django.contrib import admin
from post.models import Images, Tag, Post


class ImagesInlineAdmin(admin.TabularInline):
    list_display = ('id', 'post',)
    model = Images


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', )
    search_fields = ('id', 'tag', )

admin.site.register(Tag, TagAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'date_added', 'likes')
    search_fields = ('id', 'description', )

    inlines = [
        ImagesInlineAdmin
    ]

    def likes(self, obj):
        count = Post.objects.filter(id=obj.id, is_liked=True).count()
        return count

admin.site.register(Post, PostAdmin)