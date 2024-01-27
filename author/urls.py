from django.urls import path
from . import views

urlpatterns = [
    path('author/', views.author_list, name='author'),
    path('add_author/', views.add_author, name='add_author'),
    path('edit_author/<int:pk>/', views.edit_author, name='edit_author'),
    path('remove_author/<int:pk>/', views.remove_author, name='remove_author'),

    #api
    path('api/authors/', views.AuthorListAPIView.as_view(), name='author-list-api'),
   
]