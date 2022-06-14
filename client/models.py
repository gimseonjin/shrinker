"""
Describe models in client
"""
import string
import random

from django.db import models
from django.contrib.auth.models import User as U
from django.contrib.gis.geoip2 import GeoIP2

# Create your models here.


class TimeStampedModel(models.Model):
    """
    This is Time Stame Model!

    abstracted the generation and modification times of other models.
    """
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class PayPlan(TimeStampedModel):
    '''
    This is Users Pay Plan Model

    name : string
    price : intiger
    '''
    name = models.CharField(max_length=20)
    price = models.IntegerField()

class Organization(TimeStampedModel):
    '''
    This is relationship table User and PayPaln

    name : string
    / should insert user before

    industry : string
    / this is enum(persional, retail, manufacturing, it, others)

    pay_playn : Object(PayPlan)
    '''
    class Industries(models.TextChoices):
        '''
        This is enum class of Organization

        - persional, retail, manufacturing, it, others
        '''
        PERSONAL = "personal"
        RETAIL = "retail"
        MANUFACTURING = "manufacturing"
        IT = "it"
        OTHERS = "others"
    name = models.CharField(max_length=20)
    industry = models.CharField(max_length=15,
                                choices=Industries.choices,
                                default=Industries.OTHERS)
    pay_plan = models.ForeignKey(PayPlan, on_delete=models.DO_NOTHING, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Users(models.Model):
    '''
    This is Users table extends admin user in django

    full_name : string, null true
    url_count : integer, default 0
    organization : Object(organization), null true
    '''
    user = models.OneToOneField(U, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True)
    url_count = models.IntegerField(default=0)
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, null=True)


class EmailVerification(TimeStampedModel):
    """
    This is Email Verification Model!

    user : Object(User)
    key : string / null true
    verified : boolean / default False
    """
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, null=True)
    verified = models.BooleanField(default=False)


class Categories(TimeStampedModel):
    """
    This is Categories Model!

    This is Using for Pro level

    name : string / different from users name
    organization : Object(Organization)
    creator : Object(Users)
    """
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, null=True)
    creator = models.ForeignKey(Users, on_delete=models.CASCADE)


class ShortenedUrls(TimeStampedModel):
    """
    This is Shortened Url models

    Make shortened urls and save

    nick_name : string
    category : Object(Categories)
    prefix : string
    creator : Object(Users)
    target_url : string
    shortened_url : string
    create_via : string
    / this is enum(Web, telegram)
    expired_at : datetime
    """
    class UrlCreatedVia(models.TextChoices):
        """
        This is enum class of ShortenedUrls

        - web, telegram
        """
        WEBSITE = "web"
        TELEGRAM = "telegram"

    def rand_string():
        """
        This is Static method for creating short url!!!

        parameter not required!

        return 6 length string!
        """
        str_pool = string.digits + string.ascii_letters
        return ("".join([random.choice(str_pool) for _ in range(6)])).lower()
    
    def rand_letter():
        """
        This is Static method for creating prefix!!!

        parameter not required!

        return random string!
        """
        str_pool = string.ascii_letters
        return random.choice(str_pool).lower()

    def clicked(self):
        """
        It is update Click number!!

        It is Just update rows! So when you get db locks?

        Fix this logic!!
        """
        self.click += 1
        self.save()

    nick_name = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, on_delete=models.DO_NOTHING, null=True)
    prefix = models.CharField(max_length=50, default=rand_letter)
    creator = models.ForeignKey(Users, on_delete=models.CASCADE)
    target_url = models.CharField(max_length=2000)
    shortened_url = models.CharField(max_length=6, default=rand_string)
    create_via = models.CharField(max_length=8,
                                choices=UrlCreatedVia.choices,
                                default=UrlCreatedVia.WEBSITE)
    expired_at = models.DateTimeField(null=True)
    click = models.BigIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "prefix",
                    "shortened_url"
                ]
            )
        ]


class Staticstic(TimeStampedModel):
    class ApproachDevice(models.TextChoices):
        PC = "pc"
        MOBILE = "mobile"
        TABLET = "tablet"
    
    shortened_url = models.ForeignKey(ShortenedUrls, on_delete=models.CASCADE)
    ip = models.CharField(max_length=15)
    web_browser = models.CharField(max_length=50)
    device = models.CharField(max_length=6, choices=ApproachDevice.choices)
    device_os = models.CharField(max_length=30)
    country_code = models.CharField(max_length=2, default="XX")
    country_name = models.CharField(max_length=100, default="UNKNOWN")

    def record(self, request, url: ShortenedUrls):
        self.shortened_url = url
        self.ip = request.META["REMOTE_ADDR"]
        self.web_browser = request.user_agent.browser.family
        self.device = self.ApproachDevice.MOBILE \
            if request.user_agent.is_mobile else self.ApproachDevice.TABLET \
            if request.user_agent.is_tablet  else self.ApproachDevice.PC 
        self.device_os = request.user_agent.os.family
        try: 
            country = GeoIP2().country(self.ip)
            self.country_code = country.get("country_code", "XX")
            self.country_name = country.get("country_name", "UNKNOWN")
        except:
            pass
        url.clicked()
        self.save()