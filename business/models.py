from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Business(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="business")
    name = models.CharField(max_length=150)
    max_customers = models.IntegerField()
    avg_customers = models.IntegerField()
    employees = models.IntegerField()
    area = models.IntegerField()
    open = models.IntegerField()

    def __str__(self):
        return f"{self.name}"
