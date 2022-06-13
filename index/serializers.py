from rest_framework import serializers
from .models import Student, Sponsor, OTM


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class SponsorSerializer(serializers.ModelSerializer):
    # date = serializers.DateField(format="%Y-%m-%d")

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
                )


class OTMSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTM
        fields = "__all__"
