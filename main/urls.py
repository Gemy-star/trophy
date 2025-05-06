from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomePageView.as_view(),name='home'),
    path('policy', views.PolicyPageView.as_view(), name='policy'),
    path('refund', views.RefundPageView.as_view(), name='refund'),

]
