from rest_framework import serializers
from .models import Student, Sponsor, OTM


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class SponsorSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField('get_students')

    class Meta:
        model = Sponsor
        fields = ('name',
                  'phone_number',
                  'sponsorship_amount',
                  'payment_type',
                  'sponsor_type',
                  'company_name',
                  'sponsor_image',
                  'application_status',
                  'created_at',
                  'updated_at',
                  'students',
                  )

    def get_students(self, obj):
        print(obj)
        students = [{'id': student.id, 'name': student.name} for student in Student.objects.filter(sponsor=obj.id)]
        return students


class OTMSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTM
        fields = "__all__"