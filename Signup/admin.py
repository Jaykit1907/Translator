from django.contrib import admin

from Signup.models import Signup


class AdminSignup(admin.ModelAdmin):
    display=("first_name","last_name","phone","email","password")
    
admin.site.register(Signup,AdminSignup)





# Register your models here.
