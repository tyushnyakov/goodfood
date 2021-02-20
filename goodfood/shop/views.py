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
from django.core.mail import send_mail
from .models import OrderItem, Order
from .forms import OrderCreateForm
from django.contrib.auth.models import User


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


def cart(request, product_id=None):
    form = OrderCreateForm
    if product_id:
        if not 'cart' in request.session:
            request.session['cart'] = {}
        request.session['cart'][str(product_id)] = 1
        request.session.modified = True
        cart_products = Product.objects.filter(pk__in=request.session['cart'])
        cart = request.session['cart']
    else:
        if not 'cart' in request.session:
            cart_products = []
            cart = {}
        else:
            cart_products = Product.objects.filter(pk__in=request.session['cart'])
            cart = request.session['cart']
    return render(request, 'cart.html',
                  {'cart_products': cart_products, 'cart': cart, 'form': form})


def cart_clear(request):
    del request.session['cart']
    request.session.modified = True
    return HttpResponseRedirect("/cart")


def cart_add(request, product_id):
    request.session['cart'][str(product_id)] += 1
    request.session.modified = True
    return HttpResponseRedirect("/cart")


def cart_remove(request, product_id):
    del request.session['cart'][str(product_id)]
    request.session.modified = True
    return HttpResponseRedirect("/cart")


@login_required
def dashboard(request, user_id=None):
    user = User.objects.get(pk=user_id)
    order_list = Order.objects.filter(user=user)
    return render(request, 'dashboard.html', {'user': user,
                                              'order_list': order_list})


class RegisterFormView(FormView):
    form_class = RegisterForm
    success_url = "/login"
    template_name = "registration.html"

    def form_valid(self, form):
        user = form.save()
        send_mail(
            'Подтверждение регистрации',
            'Вы зарегестрированы',
            'ktyushnyakov@gmail.com',
            [user.email],
            fail_silently=False,
        )
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


@login_required
def order(request):
    if request.method == 'POST':
        cart = request.session['cart']
        user = request.user
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            order.user = user
            order.save()
            for key, value in cart.items():
                product = Product.objects.get(pk=int(key))
                OrderItem.objects.create(order=order,
                                         product=product,
                                         price=product.price,
                                         quantity=value)
            del request.session['cart']
            request.session.modified = True
            return render(request, 'order.html', {'order': order})
    else:
        return HttpResponseRedirect("/cart")
