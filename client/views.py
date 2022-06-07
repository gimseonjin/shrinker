from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

# Create your views here.


def index(request):
    user = User.objects.filter(username = "gimseonjin").first()
    email = user.email if user else "Anoymouse User!"
    if request.user.is_authenticated is False:
        email = "Anonymouse User!"
    return render(request, "base.html", {"welcome_msg" : f'Hello {email}'})


@csrf_exempt
def get_user(request, user_id):
    if request.method == "GET":
        user = User.objects.filter(pk = user_id).first()
        return render(request, "base.html", {"welcome_msg" : f'Hello {user.username}'})
    elif request.method == "POST":
        username = request.GET.get("username")
        if username :
            user = User.objects.filter(pk = user_id).update(username = username)
        return JsonResponse(status = 201, data = {"msg" : "You Change User Name"})