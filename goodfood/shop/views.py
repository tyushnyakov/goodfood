from django.shortcuts import render
from .models import Product
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm


def index(request):
    data = {
        'slider_list': Product.objects.filter(slider=True),
        'chosen_list': Product.objects.filter(chosen=True),
    }
    return render(request, 'index.html', context=data)


def catalog(request, category_id=None):
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    return render(request, 'catalog.html', {"products": products})


def blog(request):
    return render(request, 'blog.html')


def product(request, product_id):
    product = Product.objects.get(id=product_id)
    similar_products = Product.objects.filter(category=product.category)\
        .exclude(id=product_id).order_by('chosen')
    return render(request, 'product.html', {'product': product,
                                            'similar_products': similar_products})


@login_required
def cart(request):
    return render(request, 'cart.html')


def dashboard(request):
    return render(request, 'dashboard.html')


class RegisterFormView(FormView):
    form_class = RegisterForm
    success_url = "/login"
    template_name = "registration.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")
