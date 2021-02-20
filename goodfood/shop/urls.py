from django.urls import path
from . import views

app_name = "shop"
urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/<int:category_id>', views.catalog, name='catalog'),
    path('catalog', views.catalog, name='catalog'),
    path('blog', views.blog, name='blog'),
    path('product/<int:product_id>/', views.product, name='product'),
    path('cart/clear/', views.cart_clear, name='cart_clear'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/<int:product_id>/', views.cart, name='cart'),
    path('cart', views.cart, name='cart'),
    path('order', views.order, name='order'),
    path('dashboard/<int:user_id>/', views.dashboard, name='dashboard'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('registration', views.RegisterFormView.as_view(), name='registration'),
    path('login', views.LoginFormView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    ]
