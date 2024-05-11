from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    userId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    password = models.CharField(max_length=200)
    phone = models.CharField(max_length=200, unique=True)
    userType = models.CharField(max_length=50)
    username = None

    USERNAME_FIELD = 'userId'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.userId:
            initial_user_id = get_next_user_id()
            self.userId = initial_user_id
        super().save(*args, **kwargs)


class VaccineInfo(models.Model):
    Vaccine_id = models.CharField(primary_key=True, max_length=100)
    Vaccine_name = models.CharField(max_length=100)
    Vaccine_dose = models.IntegerField(default=0)


class UserVaccineDetails(models.Model):
    UserVaccineDetails_id = models.AutoField(primary_key=True)
    User_id = models.ForeignKey(User, on_delete=models.CASCADE)
    Vaccine_id = models.ForeignKey(VaccineInfo, on_delete=models.CASCADE)
    Vaccine_given_date = models.DateField(auto_now_add=True)
    Vaccinator_id = models.IntegerField()


def get_next_user_id():
    highest_user_id = User.objects.aggregate(models.Max('userId'))['userId__max']
    if highest_user_id is not None:
        return highest_user_id + 1
    else:
        return 1001
