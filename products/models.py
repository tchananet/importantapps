from django.db import models
from uuid import uuid4

# Create your models here.

class Category(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    description = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    
    def __str__(self):
        return self.designation
    

class Product(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    description = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    categorie = models.ForeignKey('Category', on_delete=models.CASCADE)    
    images = models.CharField(max_length=500)

    def __str__(self):
        return self.designation 