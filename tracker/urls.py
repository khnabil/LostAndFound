from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('create-account/', views.create_account_view, name='create_account'),
    path('logout/', views.logout_view, name='logout'),
    path('my-profile/', views.my_profile_view, name='my_profile'),
    path('post/', views.post_list_view, name='post_list'),
    path('post/new/', views.create_found_item_view, name='create_found_item'),
]
