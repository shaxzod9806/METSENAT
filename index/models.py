from django.db import models

upload_sponsor = "profile/sponsor_image/"
upload_student = "profile/student_image/"


# Create your models here.
class Sponsor(models.Model):
    TYPE_PAYMENT = (
        (1, 'bank'),
        (2, 'click'),
        (3, 'payme'),
        (4, 'cash'),
        (5, 'other'),
    )
    TYPE_SPONSOR = (
        (1, 'legal_entity'),
        (2, 'individual'),
    )
    TYPE_APPLICATION_STATUS = (
        ('yangi', 'yangi'),
        ('tasdiqlangan', 'tasdiqlangan'),
        ('moderatsiyada', 'moderatsiyada'),
        ('bekor_qilingan', 'bekor_qilingan'),
    )
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)
    sponsorship_amount = models.FloatField(null=True, blank=True)
    current_balance = models.FloatField(null=True, blank=True,default=sponsorship_amount)
    payment_type = models.PositiveSmallIntegerField(choices=TYPE_PAYMENT, default=4)
    sponsor_type = models.PositiveSmallIntegerField(choices=TYPE_SPONSOR, default=2)
    company_name = models.CharField(max_length=100, default="not_legal_entity")  # it is same with extend
    sponsor_image = models.ImageField(upload_to=upload_sponsor, null=True, blank=True)
    application_status = models.CharField(choices=TYPE_APPLICATION_STATUS, max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class OTM(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    TYPE_STUDENT = (
        ('bachelor', 'bachelor'),
        ('magister', 'magister'),
    )
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)
    contract_amount = models.FloatField()
    current_balance = models.FloatField(default=0)
    type_student = models.CharField(choices=TYPE_STUDENT, default='bachelor', max_length=20)
    OTM = models.ForeignKey(OTM, on_delete=models.CASCADE)
    sponsor = models.ManyToManyField(Sponsor, null=True, blank=True)
    image = models.ImageField(upload_to=upload_sponsor, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
