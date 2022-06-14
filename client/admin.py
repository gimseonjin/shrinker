from django.contrib import admin

from client.models import PayPlan, Staticstic, Users

# Register your models here.

admin.site.register(PayPlan)
admin.site.register(Users)
admin.site.register(Staticstic)