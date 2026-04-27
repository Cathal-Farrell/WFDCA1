from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class Location(models.Model):
    phoneNumber = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    province = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    postalCode = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.province}, {self.country}"

class Role(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class User(models.Model):
    lastName = models.CharField(max_length=200)
    firstName = models.CharField(max_length=200)
    phoneNumber = models.CharField(max_length=200)
    emailAddress = models.CharField(max_length=200)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return f"{self.firstName} {self.lastName}"
    
class User_Role(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    salary = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.role}"

class Product(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=2000)
    price = models.IntegerField()
    stock = models.IntegerField()

    def increaseStock(self, qty):
        self.stock += qty
    
    def decreaseStock(self, qty):
        self.stock -= qty

    def __str__(self):
        return self.name

class Order(models.Model):
    date = models.DateTimeField("date sold")
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    customerID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_set")
    locationID = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null = True, default=None)

    def __str__(self):
        return f"{self.pk} - {self.date}" 
    
class Notification(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    orderID = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null = True)
    tutorialID = models.ForeignKey('staff.Tutorial', on_delete=models.CASCADE, blank=True, null = True)
    pub_date = models.DateTimeField("date published")

    def was_published_recently(self):
        now = timezone.now()
        return now >= self.pub_date >= now - datetime.timedelta(days=30)
    
    def has_arrived(self):
        now = timezone.now()
        return now >= self.pub_date >= now - datetime.timedelta(days=3)