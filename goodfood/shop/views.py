from django.shortcuts import render
from django.http import HttpResponse
from .models import Product


def index(request):
    data = {
        'slider_list': Product.objects.filter(slider=True),
        'chosen_list': Product.objects.filter(chosen=True),
    }
    return render(request, 'index.html', context=data)


def catalog(request):
    return render(request, 'catalog.html')


def blog(request):
    return render(request, 'blog.html')


def product(request, product_id):
    product = Product.objects.get(id=product_id)
    similar_products = Product.objects.filter(category=product.category)
    return render(request, 'product.html', {'product': product,
                                            'similar_products': similar_products})


def cart(request):
    return render(request, 'cart.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def login(request):
    return render(request, 'login.html')
