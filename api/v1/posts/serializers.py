from rest_framework import serializers
from post.models import Post, Images, Tag
from django.urls import reverse


class PostSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    post_details = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'pk',
            'tags',
            'images',
            'date_added',
            'description',
            'post_details'
        )
    
    def get_tags(self, instance):
        tags = []
        all_tags = Tag.objects.filter(post=instance)
        for i in tags:
            tags.append(i.tag)
        
        return tags
    
    def get_post_details(self, instance):
        post_details = {
            "total_likes" : Post.objects.filter(id=instance.id, is_liked=True).count(),
            "total_dislikes" : Post.objects.filter(id=instance.id, is_disliked=True).count()
        }
        
        return post_details

    def get_images(self, instance):
        request = self.context.get('request')
        post_images = Images.objects.filter(post=instance)
        return [request.build_absolute_uri(i.post_image.url) for i in post_images]
