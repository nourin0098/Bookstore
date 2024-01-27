from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='books'),
    path('add_book/', views.add_book, name='add_book'),
    path('book_edit/<int:pk>/', views.book_edit, name='book_edit'),
    path('remove_book/<int:pk>/', views.remove_book, name='remove_book'),

    #api for listing books
    path('api/books/', views.BookListAPIView.as_view(), name='book-list-api'),
]
