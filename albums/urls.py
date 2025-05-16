app_name = 'albums'

from django.urls import path
from .views import AlbumView, AlbumDetailView, AlbumAddImageView, AlbumRemoveImageView

urlpatterns = [
    path('', AlbumView.as_view(), name='album-list-create'),
    path('<int:album_id>/', AlbumDetailView.as_view(), name='album-detail'),
    path('<int:album_id>/add_image/', AlbumAddImageView.as_view(), name='album-add-image'),
    path('<int:album_id>/remove_image/', AlbumRemoveImageView.as_view(), name='album-remove-image'),
]

