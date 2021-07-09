
from django.http import Http404
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from post.models import Post, Images, Tag
from .serializers import PostSerializer


class PostList(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):

        posts = Post.objects.all()
        
        page = int(request.GET.get('page', 1))

        paginator = Paginator(posts, 21)
        
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        serialized = PostSerializer(posts, many=True, context={"request": request})
        
        response_data = {
            "StatusCode": 6000,
            "data":  {
                "data": serialized.data,
                "pagination": {
                    "has_next": posts.has_next(),
                    "next_page_number": posts.next_page_number() if page < paginator.num_pages else paginator.num_pages,
                }
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)


class SimilarPostList(APIView):
    permission_classes = [AllowAny]

    def get(self, request,pk, format=None):
        post = Post.objects.get(pk=pk)

        if request.user.is_authenticated:
            tags_pks = Post.objects.all().values_list('tags__pk', flat=True).distinct()
            tags = Tag.objects.filter(pk__in=tags_pks)
            post_pks = Post.objects.filter(tags__in=tags).values_list('post_id', flat=True)
            similar_posts = Post.objects.filter(pk__in=post_pks).exclude(pk=pk).annotate(matched_count=Count('postimage__tags')).order_by('-matched_count')
        else:
            similar_posts = Post.objects.none()

        # pagination
        page = int(request.GET.get('page', 1))

        paginator = Paginator(similar_posts, 21)
        try:
            similar_posts = paginator.page(page)
        except PageNotAnInteger:
            similar_posts = paginator.page(1)
        except EmptyPage:
            similar_posts = paginator.page(paginator.num_pages)

        similar_post_serialized = PostSerializer(similar_posts, many=True, context={"request": request})
        serialized  = PostSerializer(post,  context={"request": request})
        
        response_data = {
            "StatusCode": 6000,
            "data":  {
                "data": serialized.data,
                "similar_products" : similar_post_serialized.data,
                "pagination": {
                    "has_next": similar_posts.has_next(),
                    "next_page_number": similar_posts.next_page_number() if page < paginator.num_pages else paginator.num_pages,
                }
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def change_post_status(request, pk):
    if Post.objects.filter(pk=pk).exists():
        post = Post.objects.get(pk=pk)
        
        status = request.data['status']

        if status == "2":        
            post.is_liked = True
        elif status == "4":
            post.is_disliked = True
            
        response_data = {
            "StatusCode": 6000,
            "data":  {
                "message": "Successfully changed",
            }
        }
    else:
        response_data = {
            "StatusCode": 6000,
            "data":  {
                "message": "Post Not Found",
            }
        }
        
    return Response(response_data, status=status.HTTP_200_OK)