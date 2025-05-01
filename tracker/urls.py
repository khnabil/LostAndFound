from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('create-account/', views.create_account_view, name='create_account'),
    path('logout/', views.logout_view, name='logout'),
    path('my-profile/', views.my_profile_view, name='my_profile'),
    path('comment/<int:item_id>/', views.post_comment, name='post_comment'),
    path('upvote/<int:item_id>/', views.upvote_post, name='upvote_post'),
]
