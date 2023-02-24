from django.urls import path

from .views import *

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("post/<str:pk>/",PostDetailView.as_view(),name="post-detail"),
    path("commentForm/",CommentFormPost.as_view(),name="comment-form"),
    path("post/edit/<str:pk>/",PostEditView.as_view(),name="post-edit"),
    path("CommentDelete/<str:pk>/",CommentDelete,name="comment-delete"),
    path("post_delete/<str:pk>/",post_delete,name="post-delete"),
    path("profile/<str:pk>/",ProfileView.as_view(),name="profile"),
    path("profile-update/<str:pk>/",UpdateProfile.as_view(),name="profile-update"),
    
    path("profile-add-follower/<str:pk>/",AddFollower,name="add-follower"),
    path("profile-remove-follower/<str:pk>/",RemoveFollower,name="remove-follower"),
    
    path("post-add-like/<str:pk>/",add_like,name="add-like"),
    path("post-remove-like/<str:pk>/",remove_like,name="remove-like"),
    
    path("search/",search,name="search"),
    
    path("add_comment_like/<str:pk>/",add_comment_like,name="comment-like"),
    path("remove_comment_like/<str:pk>/",remove_comment_like,name="comment-unlike"),
    path("comment-reply/<str:post_pk>/<str:pk>/",CommentReplyView.as_view(),name="comment-reply"),
    
    path("profile/followers/<str:pk>/",ListFollowers.as_view(),name="followers_list"),
    
    path("notifications/",Notifications.as_view(),name="notifications"),
    path("notifications/<str:pk>/",notification_delete,name="notification-delete"),
    
    path("threads/",ListThreads.as_view(),name="inbox"),
    path("threads/<str:pk>/",ThreadView.as_view(),name="thread"),
    path("threads-create/",CreateThread.as_view(),name="create-thread"),
    path("message-create/<str:pk>/",CreateMessage.as_view(),name="create-message"),
    
    path("post-share/<str:pk>/",SharePostView.as_view(),name="post-share"),
    path("tag/<str:pk>/",get_tag,name="tag")
]
