from django.contrib import admin
from .models import Book, UserBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors', 'publisher', 'published_date', 'categories', 'language', 'isbn_10', 'isbn_13', 'page_count', 'comics_content', 'preview_link', 'info_link', 'thumbnail')
    search_fields = ('title', 'authors', 'isbn_10', 'isbn_13')
    list_filter = ('language', 'comics_content')

@admin.register(UserBook)
class UserBookAdmin(admin.ModelAdmin):
    list_display =("user", "book")
