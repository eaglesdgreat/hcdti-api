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
    path('update_user_admin/<id>', views.update_user_admin),
    path('reset_password_otp', views.reset_password_otp),
    path('reset_password_confirm', views.reset_password_confirm),
    path('get_single_user/<id>', views.get_single_user),
]
