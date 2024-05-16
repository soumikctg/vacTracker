from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    userId = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
    phone = models.CharField(max_length=200, unique=True)
    userType = models.CharField(max_length=50)
    nid = models.CharField(max_length=50, unique=True, default='Unknown')
    address = models.CharField(max_length=500, default='Unknown')
    username = None

    USERNAME_FIELD = 'userId'
    REQUIRED_FIELDS = []


class VaccineInfo(models.Model):
    Vaccine_id = models.CharField(primary_key=True, max_length=100)
    Vaccine_name = models.CharField(max_length=100)
    Vaccine_dose = models.IntegerField(default=0)


class UserVaccineDetails(models.Model):
    UserVaccineDetails_id = models.AutoField(primary_key=True)
    User_id = models.ForeignKey(User, on_delete=models.CASCADE)
    Vaccine_id = models.ForeignKey(VaccineInfo, on_delete=models.CASCADE)
    Vaccine_given_date = models.DateField(auto_now_add=True)
    Vaccinator_id = models.CharField(max_length=50)


