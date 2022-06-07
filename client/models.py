from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class PayPlan(models.Model):
    '''
    유저의 계약 정보를 담는 모델입니다.
    '''
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class UserDetail(models.Model):
    '''
    유저와 계약 정보를 1 대 1 매핑하는 관계 테이블 모델입니다.
    관계 테이블로 만든 이유는 가능한 사이드 이펙트를 만들고 싶지 않아
    django 기본 테이블을 변형시키고 싶지 않습니다.
    '''
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    pay_plan = models.ForeignKey(PayPlan, on_delete= models.DO_NOTHING)

