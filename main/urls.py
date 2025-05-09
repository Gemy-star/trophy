from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomePageView.as_view(),name='home'),
    path('policy', views.PolicyPageView.as_view(), name='policy'),
    path('refund', views.RefundPageView.as_view(), name='refund'),
    path('categories', views.CategoriesListView.as_view(), name='categories'),
    path('auth', views.AuthView.as_view(), name='auth_view'),
    path('vendor/create', views.vendor_register, name='register_vendor'),
    path('contact', views.contact_view, name='contact'),
    path('about', views.AboutPageView.as_view(), name='about'),

]
