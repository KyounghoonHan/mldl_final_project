from django.contrib import admin
from .models import Apartment, Dong, Apt

# Register your models here.

admin.site.register(Apartment)
admin.site.register(Dong)
admin.site.register(Apt)