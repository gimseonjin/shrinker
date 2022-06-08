from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from client.forms import RegisterForm

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


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        msg = "올바르지 않은 데이터 입니다."
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            msg = "회원가입완료"
        return render(request, "register.html", {"form": form, "msg": msg})
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        msg = "가입되어 있지 않거나 로그인 정보가 잘못 되었습니다."
        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                msg = "로그인 성공"
                login(request, user)
        return render(request, "login.html", {"form": form, "msg": msg})
    else:
        form = AuthenticationForm()
        return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("index")


@login_required
def list_view(request):
    page = int(request.GET.get("p", 1))
    users = User.objects.all().order_by("-id")
    paginator = Paginator(users, 10)
    users = paginator.get_page(page)

    return render(request, "boards.html", {"users": users})