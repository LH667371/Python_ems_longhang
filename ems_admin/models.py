from django.db import models

# Create your models here.
class User(models.Model):
    email = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    sex = models.CharField(max_length=10)
    salt = models.CharField(max_length=255)

    class Meta:
        db_table = 'user_info'