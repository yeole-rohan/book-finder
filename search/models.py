from django.db import models
from user.models import User

class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    published_date = models.CharField(max_length=20)
    description = models.TextField()
    categories = models.CharField(max_length=255)
    language = models.CharField(max_length=20)
    isbn_10 = models.CharField(max_length=20)
    isbn_13 = models.CharField(max_length=20)
    page_count = models.PositiveIntegerField()
    comics_content = models.BooleanField()
    preview_link = models.URLField()
    info_link = models.URLField()
    thumbnail = models.URLField()

    def __str__(self):
        return self.title

class UserBook(models.Model):
    book = models.ForeignKey("Book", verbose_name="Book", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Shop User", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "User Book"
        verbose_name_plural = "User Books"

    def __str__(self):
        return str(self.user.username)