from django.db import models
from django.utils import timezone



# Create your models here.

class Country(models.Model):
    name=models.CharField(max_length=300)
    flag = models.ImageField(upload_to='plants/images/')


    def __str__(self):
        return self.name


class Plant(models.Model):

    class CategoryChoices (models.TextChoices):
        MEDICINAL = "MED", "Medicinal"
        ORNAMENTAL = "ORN", "Ornamental"
        AROMATIC = "ARO", "Aromatic"
        FRUIT = "FRT", "Fruit Plants"
        TOXIC = "TOX", "Toxic Plants"
        INDOOR = "IN", "Indoor Plants"
        OUTDOOR = "OUT", "Outdoor Plants"


    name=models.CharField(max_length=300)
    about=models.TextField()
    used_for=models.TextField()
    image = models.ImageField(upload_to='plants/images/')
    category=models.CharField(max_length=150, choices=CategoryChoices.choices)
    is_edible=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    countries =models.ManyToManyField(Country)

    def __str__(self):
        return self.name

class Review(models.Model):
    plant = models.ForeignKey(Plant,on_delete=models.CASCADE)
    name=models.CharField(max_length=300)
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"review name {self.name} for {self.plant.name}"
    




    