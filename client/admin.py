from django.contrib import admin

from client.models import PayPlan
from client.models import UserDetail

# Register your models here.


admin.site.register(PayPlan)
admin.site.register(UserDetail)