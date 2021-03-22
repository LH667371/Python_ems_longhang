from django.db import models


# Create your models here.

class Department(models.Model):
    department = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'depart_info'


class Employee(models.Model):
    name = models.CharField(max_length=255)
    salary = models.FloatField()
    age = models.CharField(max_length=255)
    sex = models.CharField(max_length=1)
    birthday = models.DateField()
    head_pic = models.ImageField(upload_to='pic', null=True)
    depart = models.ForeignKey(to=Department, on_delete=models.CASCADE)

    class Meta:
        db_table = 'employee_info'
