from django.urls import path

from . import views

app_name = 'staff'

urlpatterns = [
    path("", views.index, name="index"),
    path("tutorial/<int:tutorial_id>/", views.tutorial, name="tutorial"),
    path("tutorial/<int:tutorial_id>/grade/", views.grade, name="grade"),
    path("<int:product_id>/", views.detail, name="detail"),
    path("<int:product_id>/update/", views.update, name="update"),
    path("order/<int:order_id>/", views.order, name="order"),
    path("order/<int:order_id>/complete/", views.complete, name="complete"),
    path("roles/", views.roles, name="roles"),
    path("roles/<int:user_id>/", views.changeRole, name="changeRole"),
    path("roles/<int:user_id>/completeChange", views.completeChange, name="completeChange"),
]