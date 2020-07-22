from django.db import models
from django.contrib.auth.models import User
from business.models import Business

# Create your models here.
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    test_status = models.IntegerField()
    quarantined = models.IntegerField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Visit(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="visits")
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="visits")
    date = models.DateField()

    def __str__(self):
        return f"{self.customer}"
