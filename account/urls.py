from account.views import create_user, logged_in_user
from django.urls import path, include
from . import views


urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('logged_in_user', views.logged_in_user),
    path('create_user', views.create_user),
    path('get_all_user', views.get_all_user),
    path('delete_user/<id>', views.delete_user),
    path('update_user', views.update_user),
]
