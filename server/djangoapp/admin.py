from django.contrib import admin
from .models import CarMake, CarModel

@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'country_of_origin', 'founded_year')
    search_fields = ('name', 'country_of_origin')
    list_filter = ('country_of_origin', 'founded_year')

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'type', 'year', 'dealer_id')
    search_fields = ('name', 'car_make__name')
    list_filter = ('type', 'year', 'car_make')


# Register your models here.

# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
