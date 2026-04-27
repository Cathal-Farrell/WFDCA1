from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:product_id>/", views.detail, name="detail"),
    path("<int:product_id>/purchase/", views.purchase, name="purchase"),
    path("<int:product_id>/sale/", views.sale, name="sale"),
    path("order/<int:order_id>/", views.order, name="order"),
]