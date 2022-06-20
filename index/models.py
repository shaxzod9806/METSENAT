from django.db import models
from django.contrib.auth.models import User

upload_student = "profile/student_image/"


# create Student model with AbstractUser
class Student(User):
    profession = models.CharField(max_length=100, null=True, blank=True)
    student_image = models.ImageField(upload_to=upload_student, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
