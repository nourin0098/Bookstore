from django.db import models
from author.models import Author
# Create your models here.


class Book(models.Model):
    bookid = models.CharField(max_length=200)
    bookname = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.bookname