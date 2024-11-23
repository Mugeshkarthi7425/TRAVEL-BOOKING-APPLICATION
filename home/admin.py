from django.contrib import admin
from home.models import users,S_flight,Flight_schedule,places

#Register your models here.
admin.site.register(users)
admin.site.register(S_flight)
admin.site.register(Flight_schedule)
admin.site.register(places)