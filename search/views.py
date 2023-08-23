from django.shortcuts import render, redirect
from django.db.models import Q,  CharField, TextField
from .models import Book, UserBook
from . import tasks


def shopbooks(request):
    shopbooks = UserBook.objects.filter(user=request.user).select_related("book")
    return render(request, "shopbooks.html", {'books' :shopbooks})

def selectbooks(request):
    # if request.user.isVerified:
    keyword, search_results = '', ''
    if request.method == "POST" and "search-btn" in request.POST:
        keyword = request.POST.get("search-input")
        q_objects = create_query(keyword)
        try:
            search_results = Book.objects.filter(q_objects)[:10]
        except:
            search_results = Book.objects.filter(q_objects)
    # else:
    #     return redirect()
    return render(request, "selectbook.html", {'search_results' : search_results, 'keyword' : keyword})

def adminsearch(request):
    keyword = ''
    if request.method == "POST" and "search-btn" in request.POST:
        keyword = request.POST.get("search-input")
        search_data = tasks.search_books(keyword, 0, 10)
        tasks.save_search_results(search_data, keyword)
        
    return render(request, "adminsearch.html", {'keyword' : keyword})

def search(request):
    keyword, search_results, users_with_these_books = '', '', ''
    if request.method == "POST" and "search-btn" in request.POST:
        keyword = request.POST.get("search-input")
        q_objects = create_query(keyword)
        
        # Perform the search using the Q object
        try:
            search_results = Book.objects.filter(q_objects)[:10]
        except:
            search_results = Book.objects.filter(q_objects)
        users_with_these_books = UserBook.objects.filter(book__in=search_results.values_list("id", flat=True)).select_related("user")
        print(users_with_these_books, "Billesur", search_results)
    return render(request, "search.html", {'search_results' : search_results, 'keyword' : keyword, 'users_with_these_books' : users_with_these_books})

def create_query(keyword):
    q_objects = Q()
    for field in Book._meta.fields:
        if isinstance(field, (CharField, TextField)):
            q_objects |= Q(**{f'{field.name}__icontains': keyword})
    return q_objects

