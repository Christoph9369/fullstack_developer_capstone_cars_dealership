# from django.contrib import admin
from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.


# CarModelInline class
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1  # Number of extra forms displayed


# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "year", "car_make"]
    list_filter = ["type", "year"]
    search_fields = ["name", "car_make__name"]


# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    inlines = [CarModelInline]


# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
