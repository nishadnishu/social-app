from django.urls import re_path
from . import views

app_name = 'api_v1_post'

urlpatterns = [
    re_path(r'^posts/$', views.PostList.as_view()),
    re_path(r'^posts-status-update/(?P<pk>.*)/$', views.change_post_status),
    re_path(r'^similar-posts/(?P<pk>.*)/$', views.SimilarPostList.as_view()),
]