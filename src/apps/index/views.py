from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from apps.product.models import Category, Book
from django.views import View


class HomePageView(View):
    def get(self, request):
        if 'term' in request.GET:
            qs = Book.objects.filter(Q(title__icontains=request.GET.get('term')) |
                                     Q(author__icontains=request.GET.get('term')))
            titles = [book.title for book in qs]
            return JsonResponse(titles, safe=False)

        queryset = {
            'books': Book.objects.all(),
        }
        return render(request, 'index/home.html', queryset)

    def post(self, request):
        title = request.POST['search']
        queryset = {
            'books': Book.objects.filter(Q(title__icontains=title) |
                                         Q(author__icontains=title)),
        }
        return render(request, 'index/home.html', queryset)


class CategoryBooksView(View):
    def get(self, request, slug):
        if 'term' in request.GET:
            qs = Book.objects.filter(Q(title__icontains=request.GET.get('term')) |
                                     Q(author__icontains=request.GET.get('term')))
            titles = [book.title for book in qs]
            return JsonResponse(titles, safe=False)

        category = Category.objects.get(slug=slug)
        queryset = {
            'books': Book.objects.filter(categories__in=[category]),
        }
        return render(request, 'index/home.html', queryset)
