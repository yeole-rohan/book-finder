from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def paginate_results(request, queryset, results_per_page):
    page_number = request.GET.get('page')
    paginator = Paginator(queryset, results_per_page)
    page = paginator.get_page(page_number)
    return page