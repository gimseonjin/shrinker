from django.shortcuts import render, redirect

from django.contrib.auth.models import User

# Create your views here.


def index(request):
    user = User.objects.filter(username = "gimseonjin").first()
    email = user.email if user else "Anoymouse User!"
    if request.user.is_authenticated is False:
        email = "Anonymouse User!"
    return render(request, "base.html", {"welcome_msg" : f'Hello {email}'})

