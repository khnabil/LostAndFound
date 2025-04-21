from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_view, name='login'),
    path('home/',views.home_view, name='home'),
    path('create-account/', views.create_account_view, name='create_account'),
]
