from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('api/clientes/', views.api_clientes, name='api_clientes'),
    path('api/fornecedores/', views.api_fornecedores, name='api_fornecedores'),
    path('api/produtos/', views.api_produtos, name='api_produtos'),
    path('api/vendas/', views.api_vendas, name='api_vendas'),
    path('api/dashboard/', views.api_dashboard, name='api_dashboard'),
]