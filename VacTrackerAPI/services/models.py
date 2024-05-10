from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    userId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    password = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    userType = models.CharField(max_length=50)
    username = None

    USERNAME_FIELD = 'userId'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.userId:
            initial_user_id = get_next_user_id()
            self.userId = initial_user_id
        super().save(*args, **kwargs)


def get_next_user_id():
    highest_user_id = User.objects.aggregate(models.Max('userId'))['userId__max']
    if highest_user_id is not None:
        return highest_user_id + 1
    else:
        return 1001
