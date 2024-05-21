from django.contrib import admin

from .models.cities import City 
from .models.departments import Department


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    list_filter = ('department', )


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Register your models here.
admin.site.register(City, CityAdmin)
admin.site.register(Department, DepartmentAdmin) 