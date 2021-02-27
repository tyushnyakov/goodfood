from django.shortcuts import render
from .models import Product, OrderItem, Order, Blog
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.core.mail import send_mail, mail_admins
from .forms import OrderCreateForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator


def index(request):
    data = get_cart(request)
    data['slider_list'] = Product.objects.filter(slider=True)
    data['chosen_list'] = Product.objects.filter(chosen=True)

    return render(request, 'index.html', context=data)


def catalog(request):
    data = get_cart(request)
    if not request.GET.get('order'):
        sort_order = 'category'
    else:
        sort_order = request.GET.get('order')
    products = Product.objects.all().order_by(sort_order)

    paginator = Paginator(products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data['page_obj'] = page_obj

    return render(request, 'catalog.html', context=data)


def category_catalog(request, category_id=None):
    data = get_cart(request)
    if not request.GET.get('order'):
        sort_order = '?'
    else:
        sort_order = request.GET.get('order')

    products = Product.objects.filter(category_id=category_id).order_by(sort_order)

    paginator = Paginator(products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data['page_obj'] = page_obj

    return render(request, 'catalog.html', context=data)


def blog(request):
    data = get_cart(request)
    data['blogs'] = Blog.objects.all()

    return render(request, 'blog.html', context=data)


def product(request, product_id):
    data = get_cart(request)
    product = Product.objects.get(id=product_id)
    data['product'] = product
    data['similar_products'] = Product.objects.filter(category=product.category)\
        .exclude(id=product_id).order_by('chosen')

    return render(request, 'product.html', context=data)


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
    data = get_cart(request)
    user = User.objects.get(pk=user_id)
    data['user'] = user
    data['order_list'] = Order.objects.filter(user=user)
    return render(request, 'dashboard.html', context=data)


class RegisterFormView(FormView):
    form_class = RegisterForm
    success_url = "/login"
    template_name = "registration.html"

    def get(self, request):
        context = self.get_context_data()
        data = get_cart(request)
        context['cart'] = data['cart']
        context['cart_products'] = data['cart_products']
        return render(self.request, self.template_name, context)

    def form_valid(self, form):
        user = form.save()
        send_mail(
            'Подтверждение регистрации',
            'Вы зарегестрированы',
            'admin@localhost',
            [user.email],
            fail_silently=False,
        )
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/"

    def get(self, request):
        context = self.get_context_data()
        data = get_cart(request)
        context['cart'] = data['cart']
        context['cart_products'] = data['cart_products']
        return render(self.request, self.template_name, context)

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
            mail_admins('Новый заказ', 'Оформлен новый заказ № {}'.format(order.id))
            del request.session['cart']
            request.session.modified = True
            return render(request, 'order.html', {'order': order})
    else:
        return HttpResponseRedirect("/cart")


def get_cart(request):
    if not 'cart' in request.session:
        cart_products = []
        cart = {}
    else:
        cart_products = Product.objects.filter(pk__in=request.session['cart'])
        cart = request.session['cart']
    return {'cart': cart, 'cart_products': cart_products}
