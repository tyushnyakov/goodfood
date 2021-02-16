from django.urls import path
from . import views

app_name = "shop"
urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/<int:category_id>', views.catalog, name='catalog'),
    path('catalog', views.catalog, name='catalog'),
    path('blog', views.blog, name='blog'),
    path('product/<int:product_id>/', views.product, name='product'),
    path('cart', views.cart, name='cart'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('login', views.login, name='login'),
    ]
