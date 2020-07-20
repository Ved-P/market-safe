from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    test_status = models.IntegerField()
    quarantined = models.IntegerField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
