from django.urls import path
from . import views
from .views import CategoryDetailView, PostDetailView, PostUpdateView, PostDeleteView, SearchResultsView

from django.conf.urls import url

urlpatterns = [
    path('', views.feed, name='socialcoder-feed'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='socialcoder-post-delete'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='socialcoder-post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='socialcoder-post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='socialcoder-post-delete'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='socialcoder-category-detail'),
    path('leaderboard/', views.leaderboard, name='socialcoder-leaderboard'),
    path('upvote/<int:id>', views.upvote, name='socialcoder-upvote'),
    path('post/<int:pk>/accept/<int:id>', views.acceptResponse, name='acceptResponse'),
    path('post/<int:pk>/upvote/<int:id>', views.upvote, name='socialcoder-post-upvote'),
    path('post/<int:pk>/downvote/<int:id>', views.downvote, name='socialcoder-post-downvote'),
    path('downvote/<int:id>', views.downvote, name='socialcoder-downvote'),
    path('post/<int:pk>/post/<int:id>/upvote/response/<int:rid>', views.upvote_response, name='upvote-response'),
    path('post/<int:pk>/post/<int:id>/downvote/response/<int:rid>', views.downvote_response, name='downvote-response'),
    path('post/<int:pk>/addcomment/', views.add_comment, name='socialcoder-add-comment'),
    path('add/post/', views.add_post, name='socialcoder-post-create'),
    path('usernames', views.all_usernames, name='socialcoder-all-usernames'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('add/category/', views.add_category, name='socialcoder-category-create'),
    path('category/<int:pk>/followCategory/<int:id>', views.followCategory, name='followCategory'),
]
