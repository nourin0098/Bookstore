from django.db import models

# Create your models here.
class Author(models.Model):
    authorname = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.authorname