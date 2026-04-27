from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .models import Tutorial, Question, Choice
from store.models import Order, Product, User, User_Role, Role, Notification

from django.utils import timezone

# Create your views here.

def index(request):
    products_list = Product.objects.order_by()
    orders_list = Order.objects.order_by()
    template = loader.get_template("staff/index.html")
    context = {"products_list":products_list, "orders_list":orders_list}
    return HttpResponse(template.render(context, request))

def tutorial(request, tutorial_id):
    tutorial = Tutorial.objects.get(pk=tutorial_id)
    question_list = Question.objects.filter(tutorial=tutorial.pk)
    choice_list = Choice.objects.filter(question__in=question_list)
    template = loader.get_template("staff/tutorial.html")
    context = {"tutorial":tutorial, "question_list":question_list, "choice_list":choice_list}
    return HttpResponse(template.render(context, request))

def grade(request, tutorial_id):
    tutorial = Tutorial.objects.get(pk=tutorial_id)
    question_list = Question.objects.filter(tutorial=tutorial.pk)
    choice_list = Choice.objects.filter(question__in=question_list)

    correct = 0

    for question in question_list:
        formChoice = request.POST[f"choice{question.pk}"]
        choice = Choice.objects.get(pk=formChoice)
        if choice.is_correct:
            correct += 1

    if correct != question_list.count():
        return render(
            request,
            "staff/tutorial.html",
            {
                "tutorial": tutorial,
                "question_list": question_list,
                "choice_list": choice_list,
                "error_message": "Low test score. Please try again",
            },
        )

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse("staff:index"))

def detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    template = loader.get_template("staff/product.html")
    context = {"product": product}
    return HttpResponse(template.render(context, request))

def update(request, product_id):
    product = Product.objects.get(pk=product_id)
    newStock = request.POST["new_stock"]
    product.stock = newStock
    product.save()
    return HttpResponseRedirect(reverse("staff:index"))

def order(request, order_id):
    order = Order.objects.get(pk=order_id)
    template = loader.get_template("staff/order.html")
    context = {"order": order}
    return HttpResponse(template.render(context, request))

def complete(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.delete()
    return HttpResponseRedirect(reverse("staff:index"))

def roles(request):
    user_roles_list = User_Role.objects.order_by('user')
    template = loader.get_template("staff/roles.html")
    context = {"user_roles_list":user_roles_list}
    return HttpResponse(template.render(context, request))

def changeRole(request, user_id):
    user_roles_list = User_Role.objects.filter(user=user_id)
    template = loader.get_template("staff/changeRole.html")
    context = {"user_roles_list":user_roles_list}
    return HttpResponse(template.render(context, request))

def completeChange(request, user_id):
    user = User.objects.get(pk=user_id)
    user_roles_list = User_Role.objects.filter(user=user_id)

    wasCEO = wasManager = wasClerk = wasTrainer = False

    for entry in user_roles_list:
        if entry.role == Role.objects.get(pk=1):
            wasCEO = True
        elif entry.role == Role.objects.get(pk=2):
            wasManager = True
        elif entry.role == Role.objects.get(pk=3):
            wasClerk = True
        elif entry.role == Role.objects.get(pk=4):
            wasTrainer = True
   
    if wasCEO == False:
        if "ceo" in request.POST:
            ceo = Role.objects.get(title="CEO")
            user_role = User_Role(user=user,role=ceo)
            user_role.save()
            
            ceoTutorial = Tutorial.objects.get(pk=1)
            notification = Notification(userID=user, tutorialID=ceoTutorial, pub_date=timezone.now())
            notification.save()
    else:
        if "ceo" not in request.POST:
            ceo = Role.objects.get(title="CEO")
            user_role = User_Role.objects.get(user=user, role=ceo)
            user_role.delete()

            try:
                ceoTutorial = Tutorial.objects.get(pk=1)
                notification = Notification.objects.get(userID=user, tutorialID=ceoTutorial)
                notification.delete()
            except:
                None
    
    if wasManager == False:
        if "manager" in request.POST:
            manager = Role.objects.get(title="Store Manager")
            user_role = User_Role(user=user,role=manager)
            user_role.save()

            managerTutorial = Tutorial.objects.get(pk=2)
            notification = Notification(userID=user, tutorialID=managerTutorial, pub_date=timezone.now())
            notification.save()
    else:
        if "manager" not in request.POST:
            manager = Role.objects.get(title="Store Manager")
            user_role = User_Role.objects.get(user=user, role=manager)
            user_role.delete()

            try:
                managerTutorial = Tutorial.objects.get(pk=2)
                notification = Notification.objects.get(userID=user, tutorialID=managerTutorial)
                notification.delete()
            except:
                None

    if wasClerk == False:
        if "clerk" in request.POST:
            clerk = Role.objects.get(title="Store Clerk")
            user_role = User_Role(user=user,role=clerk)
            user_role.save()

            clerkTutorial = Tutorial.objects.get(pk=3)
            notification = Notification(userID=user, tutorialID=clerkTutorial, pub_date=timezone.now())
            notification.save()
    else:
        if "clerk" not in request.POST:
            clerk = Role.objects.get(title="Store Clerk")
            user_role = User_Role.objects.get(user=user, role=clerk)
            user_role.delete()

            try:
                clerkTutorial = Tutorial.objects.get(pk=3)
                notification = Notification.objects.get(userID=user, tutorialID=clerkTutorial)
                notification.delete()
            except:
                None

    if wasTrainer == False:
        if "trainer" in request.POST:
            trainer = Role.objects.get(title="Trainer")
            user_role = User_Role(user=user,role=trainer)
            user_role.save()

            trainerTutorial = Tutorial.objects.get(pk=4)
            notification = Notification(userID=user, tutorialID=trainerTutorial, pub_date=timezone.now())
            notification.save()
    else:
        if "trainer" not in request.POST:
            trainer = Role.objects.get(title="Trainer")
            user_role = User_Role.objects.get(user=user, role=trainer)
            user_role.delete()

            try:
                trainerTutorial = Tutorial.objects.get(pk=4)
                notification = Notification.objects.get(userID=user, tutorialID=trainerTutorial)
                notification.delete()
            except:
                None

    user_roles_list = User_Role.objects.filter(user=user_id)
    if user_roles_list.count() == 0:
        user.delete()
    
    return HttpResponseRedirect(reverse("staff:roles"))


    