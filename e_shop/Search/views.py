from django.shortcuts import render
from django.http import HttpResponse
from e_app.models import Product
from django.db.models import Q


# Create your views here.


def searchDetails(request):
    if 'q' in request.GET:
        query = request.GET.get('q')
        products = Product.objects.all().filter(Q(name__contains=query) | Q(desc__contains=query))
    return render(request, 'search.html', {'products': products, 'query': query})
