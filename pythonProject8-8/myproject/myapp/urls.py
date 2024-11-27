from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('login/recommendation/', views.recommendation_view, name='recommendation'),
    path('profile/', views.profile_view, name='profile'),
    path('edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/search/', views.product_search, name='product_search'),
    path('products/suggestions/', views.product_suggestion, name='product_suggestion'),
    path('about/', views.about, name='about'),
]
