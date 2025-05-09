from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('create-account/', views.create_account_view, name='create_account'),
    path('logout/', views.logout_view, name='logout'),
    path('my-profile/', views.my_profile_view, name='my_profile'),
    path('post/', views.post_list_view, name='post_list'),
    path('post/new/', views.create_item_view, name='create_found_item'),
    path('post-comment/', views.post_comment_ajax, name='post_comment_ajax'),
    path('send-claim/', views.send_claim_request, name='send_claim_request'),
    path('claim-item/<int:item_id>/', views.claim_item_view, name='claim_item'),
    path('delete-claimed-item/<int:item_id>/', views.delete_claimed_item, name='delete_claimed_item'),

]
