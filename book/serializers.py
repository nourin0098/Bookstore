from rest_framework import serializers
from author.serializers import AuthorSerializer
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    class Meta:
        model = Book
        fields = ['id', 'bookid', 'bookname', 'author', 'created_date']