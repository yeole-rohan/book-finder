from celery import shared_task
from django.db.models import Q
from .models import Book
import time, requests

# @shared_task
def search_books(keyword, start_index, max_results=10):
    url = f"https://www.googleapis.com/books/v1/volumes?q={keyword}&startIndex={start_index}&maxResults={max_results}&key=AIzaSyCqwC1lzmh9nV1fe3Rv11lAP5OiEyG4hP8"
    response = requests.get(url)
    data = response.json()
    return data

# @shared_task
def save_search_results(search_data, keyword):
    total_items = search_data.get('totalItems', 0)
    error = search_data.get('error', '')
    if total_items > 0 and not error:
        print(f"Total Results: {total_items}")
        total_items = 500 if total_items > 500 else total_items #Limit Max Result Pagination
        for start_index in range(0, total_items, 10):
            search_data = search_books(keyword, start_index, 10)
            for item in search_data.get('items', []):
                
                book = item['volumeInfo']
                industry_identifiers = book.get('industryIdentifiers', [])

                identifier_mapping = {id_type: id_value for id_type, id_value in [(id['type'], id['identifier']) for id in industry_identifiers]}

                isbn_10 = identifier_mapping.get('ISBN_10', '')
                isbn_13 = identifier_mapping.get('ISBN_13', '')
                title=book.get('title', ''),

                if not is_duplicate(isbn_13, isbn_10, title):
                    new_book = Book(
                        title=book.get('title', ''),
                        authors=', '.join(book.get('authors', [])),
                        publisher=book.get('publisher', ''),
                        published_date=book.get('publishedDate', ''),
                        description=book.get('description', ''),
                        categories=', '.join(book.get('categories', [])),
                        language=book.get('language', ''),
                        isbn_10=isbn_10,
                        isbn_13=isbn_13,
                        page_count=book.get('pageCount', 0),
                        comics_content=book.get('comicsContent', False),
                        preview_link=book.get('previewLink', ''),
                        info_link=book.get('infoLink', ''),
                        thumbnail=book['imageLinks']['thumbnail'] if 'imageLinks' in book else ''
                    )
                    new_book.save()
        time.sleep(1) # One Sec Sleep
    else:
        print("No results found for the search.")

# Function to check if a book with given ISBN already exists in the Database file
# @shared_task
def is_duplicate(isbn13, isbn10, title):
    if Book.objects.filter(Q(title__exact=title) | Q(isbn_10__exact=isbn10) | Q(isbn_13__exact=isbn13)).exists():
        return True
    return False