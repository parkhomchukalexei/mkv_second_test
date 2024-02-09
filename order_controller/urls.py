from django.urls import path
from . import views


urlpatterns = [
    path('order/', views.OrderAPI.as_view(), name='order'),
    path('create_order', views.OrderFormView.as_view(), name='create_order'),
    path('order/<slug:slug>/ ', views.OrderFormView.order_detail_view, name='order_detail_view'),

]