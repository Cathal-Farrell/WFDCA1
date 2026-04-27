from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from django.utils import timezone
import datetime

from .models import Product, Location, User, Order, Notification


def index(request):
    products_list = Product.objects.order_by()
    user = User.objects.get(firstName="user", lastName="1")
    notifications_list = Notification.objects.filter(userID=user)
    template = loader.get_template("store/index.html")
    context = {"products_list": products_list, "notifications_list": notifications_list}
    return HttpResponse(template.render(context, request))

def detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    template = loader.get_template("store/product.html")
    context = {"product": product}
    return HttpResponse(template.render(context, request))

def purchase(request, product_id):
    product = Product.objects.get(pk=product_id)
    locations_list = Location.objects.order_by()
    template = loader.get_template("store/purchase.html")
    context = {"product": product, "locations_list": locations_list}
    return HttpResponse(template.render(context, request))

def sale(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    try:
        username = User.objects.get(firstName=request.POST["fname"], lastName=request.POST["lname"])
        location = Location.objects.get(pk=request.POST["locations"])
    except (KeyError, User.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "store/product.html",
            {
                "product": product,
                "error_message": "An account with that username does not exist.",
            },
        )
    else:
        product.decreaseStock(qty=1)
        product.save()

        order = Order(productID=product, customerID=username, date=timezone.now(), locationID=location)
        order.save()

        notification = Notification(orderID = order, userID=username, pub_date=timezone.now())
        notification.save()

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("store:index"))

def order(request, order_id):
    order = Order.objects.get(pk=order_id)
    template = loader.get_template("store/order.html")
    context = {"order": order}
    return HttpResponse(template.render(context, request))