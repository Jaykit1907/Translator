from django.db import models

# Create your models here.
class Signup(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    phone=models.CharField(max_length=20)
    email=models.EmailField(max_length=80)
    password=models.CharField(max_length=100)
    
    
    
    def __str__(self):
     return self.first_name




