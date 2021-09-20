from datetime import datetime, date

from django.db import models


# Create your models here.

class UserForm(models.Model):
    first_name = models.CharField(max_length=70)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    nationality = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pin = models.CharField(max_length=50)
    qualification = models.CharField(max_length=50)
    salary = models.CharField(max_length=50)
    pan = models.CharField(max_length=50)
    request_receive_time = models.DateTimeField(default=datetime.now())

    class Meta:
        db_table = "first_django_app_UserForm"


class ResponseInfo(models.Model):
    request_id = models.ForeignKey(UserForm, on_delete=models.CASCADE)
    response = models.CharField(max_length=50)
    reason = models.CharField(max_length=500)

    class Meta:
        db_table = "first_django_app_ResponseInfo"
