# Uncomment the following imports before adding the Model code

from django.db import models
from datetime import date
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="The name of the car make.")
    description = models.TextField(blank=True, null=True, help_text="A brief description of the car make.")
    country_of_origin = models.CharField(max_length=100, blank=True, null=True, help_text="Country where the car make originates.")
    founded_year = models.PositiveIntegerField(blank=True, null=True, help_text="Year the car make was founded.")
    website = models.URLField(blank=True, null=True, help_text="Official website of the car make.")

    def __str__(self):
        return f"{self.name} ({self.country_of_origin or 'Unknown Origin'})"

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many
# Car Models, using ForeignKey field)
# - Name
# - Type (CharField with a choices argument to provide limited choices
# such as Sedan, SUV, WAGON, etc.)
# - Year (IntegerField) with min value 2015 and max value 2023
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="models")  # Many-to-One relationship
    dealer_id = models.IntegerField(help_text="ID of the dealer in the Cloudant database")
    name = models.CharField(max_length=100, help_text="The name of the car model.")
    
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('COUPE', 'Coupe'),
        ('CONVERTIBLE', 'Convertible'),
        ('HATCHBACK', 'Hatchback'),
        # Add more choices as required
    ]
    type = models.CharField(max_length=12, choices=CAR_TYPES, default='SUV', help_text="Type of the car model")
    
    year = models.IntegerField(
        default=date.today().year,
        validators=[
            MaxValueValidator(date.today().year),
            MinValueValidator(1886)  # The year the first car was invented
        ],
        help_text="Year the car model was manufactured"
    )
    engine_type = models.CharField(max_length=50, blank=True, null=True, help_text="Type of engine, e.g., V6, Electric")
    color = models.CharField(max_length=30, blank=True, null=True, help_text="Color of the car model")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Price of the car model in USD")

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year}) - {self.type}"
