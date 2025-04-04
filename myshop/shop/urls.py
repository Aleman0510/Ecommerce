from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
     # URLs de autenticación
     path('register/', views.register_view, name='register'),
     path('login/', views.login_view, name='login'),
     path('logout/', views.logout_view, name='logout'),
     path('map/', views.map_view, name='map'),  
     path('', views.product_list, name='product_list'),
     path('<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),
     path('<int:id>/<slug:slug>/', views.product_detail,
         name='product_detail'),
     
]