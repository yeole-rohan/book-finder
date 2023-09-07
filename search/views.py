from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.db.models import Q,  CharField, TextField
from django.contrib import messages
from .models import Book, UserBook
from . import tasks


def shopbooks(request):
    shopbooks = UserBook.objects.filter(user=request.user).select_related("book")
    print(shopbooks)
    return render(request, "shopbooks.html", {'shopbooks' :shopbooks})

def selectbooks(request):
    if request.user.isVerified:
        keyword, search_results = '', ''
        if request.method == "POST" and "search-btn" in request.POST:
            keyword = request.POST.get("search-input")
            q_objects = create_query(keyword)
            userHasBooks = list(UserBook.objects.filter(user=request.user).values_list("book", flat=True))
            try:
                search_results = Book.objects.filter(q_objects).exclude(id__in=userHasBooks)[:10]
            except:
                search_results = Book.objects.filter(q_objects).exclude(id__in=userHasBooks)
    else:
        messages.warning(request, "Wait till we verify your account")
        return redirect("search:selectbooks")
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


def booktoshop(request):
    if request.method== "POST":
        bookId = request.POST.get("bookId")
        checkStatus = request.POST.get("checkStatus")
        print("checkStatus", checkStatus)
        try:
            isBook = Book.objects.get(id=bookId)
        except:
            return JsonResponse({"status" : False, "message" : "book doesnot exists."})
        if checkStatus == "true":
            book, created = UserBook.objects.get_or_create(user=request.user, book=isBook)
            if created:
                return JsonResponse({"status" : True, "message" : "book added to your shop."})
            else:
                return JsonResponse({"status" : False, "message" : "book already added to shop."})
        elif checkStatus == "false":
            UserBook.objects.filter(user=request.user, book=isBook).delete()
            return JsonResponse({"status" : True, "message" : "book removed from your shop."})
    return JsonResponse({"status" : False, "message" : "request error."})