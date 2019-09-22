from django.db import models

# Create your models here.
class Ingredients(models.Model):
    MEASURE_UNIT_CHOICES = (
        ("grams", "g"),
        ("kilograms", "kg"),
        ("centiliter", "cl"),
        ("liter", "l")
    )

    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2) #7 digits = 1 million
    measureUnit = models.CharField(max_length=10, choices=MEASURE_UNIT_CHOICES)
    ammount = models.IntegerField()
    # crationTime = models.DateTimeField(auto_now_add=True)
    # lastUpdatedTime = models.DateTimeField(default=timezone.now)
    deleted = models.BooleanField(default=False)
