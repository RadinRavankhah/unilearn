from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # User management
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('user/<str:username>/edit/', views.edit_profile, name='edit_profile'),

    # Subreddits
    path('subreddits/', views.subreddit_list, name='subreddit_list'),
    path('subreddits/new/', views.create_subreddit, name='create_subreddit'),
    path('subreddits/<str:subreddit_name>/', views.subreddit_detail, name='subreddit_detail'),
    path('subreddits/<str:subreddit_name>/edit/', views.edit_subreddit, name='edit_subreddit'),
    path('subreddits/<str:subreddit_name>/follow/', views.follow_subreddit, name='follow_subreddit'),
    path('subreddits/<str:subreddit_name>/unfollow/', views.unfollow_subreddit, name='unfollow_subreddit'),

    # Posts
    path('subreddits/<str:subreddit_name>/posts/new/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('posts/<int:post_id>/upvote/', views.upvote_post, name='upvote_post'),
    path('posts/<int:post_id>/downvote/', views.downvote_post, name='downvote_post'),
    path('posts/<int:post_id>/upvote_from_community/', views.upvote_post_from_community, name='upvote_post_from_community'),
    path('posts/<int:post_id>/downvote_from_community/', views.downvote_post_from_community, name='downvote_post_from_community'),

    # Comments
    path('posts/<int:post_id>/comments/new/', views.add_comment, name='add_comment'),
    path('posts/<int:post_id>/comments/<int:comment_id>/reply/', views.reply_to_comment, name='reply_to_comment'),
    path('posts/<int:post_id>/comments/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('posts/<int:post_id>/comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('posts/<int:post_id>/comments/<int:comment_id>/upvote/', views.upvote_comment, name='upvote_comment'),
    path('posts/<int:post_id>/comments/<int:comment_id>/downvote/', views.downvote_comment, name='downvote_comment'),

    # Search
    path('search/', views.search, name='search'),

    # Settings
    path('settings/', views.settings, name='settings'),
]
