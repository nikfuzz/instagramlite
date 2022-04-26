from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('registerUser', views.register_user),
    path('loginUser', views.login_user),
    path('logout', views.logout_user),
    path('createAlbum', views.album_get_create),
    path('getAlbums', views.album_get_create),
    path('addPicture', views.pictures_add)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
