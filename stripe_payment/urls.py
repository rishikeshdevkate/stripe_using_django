from django.urls import path

from . import views

urlpatterns = [
    path('charge/', views.CheckoutAPiView.as_view(), name='charge'),
    path('test', views.WebHookApiView.as_view(), name='test'),
]
