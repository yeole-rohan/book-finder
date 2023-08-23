from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    shopName = models.CharField(_("Shop Name"), max_length=100, default="")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    mobileNumber = models.CharField(max_length=12, default="")
    shopAddress = models.TextField("Shop Address", default="")
    email = models.EmailField(_("Email"),unique=True, max_length=254, default="")
    gstn = models.CharField(_("GSTN Number"), unique=True, max_length=16, default="")
    isVerified = models.BooleanField(_("Is Verified"), default=False)
    created = models.DateTimeField(_("Created At"),auto_now_add=True)
    lastUpdated = models.DateTimeField(_("Last Updated At"),auto_now=True)

    def __str__(self):
        return str(self.shopName)