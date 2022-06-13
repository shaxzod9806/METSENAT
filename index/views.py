import django_filters.rest_framework
from django.http import HttpResponse
from .models import Student, Sponsor, OTM
from .serializers import StudentSerializer, SponsorSerializer, OTMSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser
from utilities.pagination import PaginationHandlerMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token['username'] = user.username
        return token


class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 10
    max_page_size = 100


# Create your views here.

class StudentAPIView(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = BasicPagination
    serializer_class = StudentSerializer
    parser_classes = (MultiPartParser, FormParser)
    token = openapi.Parameter(
        'Authorization',
        in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING
    )
    student_id = openapi.Parameter('student_id', in_=openapi.IN_FORM, description="student_id",
                                   type=openapi.TYPE_STRING)

    type_id = openapi.Parameter('type_student', in_=openapi.IN_QUERY, description="type_student",
                                type=openapi.TYPE_STRING)
    otm_id = openapi.Parameter('otm_id', in_=openapi.IN_QUERY, description="otm_id",
                               type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token, type_id, otm_id])
    def get(self, request):
        type_student = request.query_params.get('type_student')
        otm_id = request.query_params.get('otm_id')
        print("type_student: ", type_student)
        student = Student.objects.all()
        if type_student and otm_id is not None:
            student = Student.objects.filter(type_student=type_student, OTM=otm_id)
        elif type_student is not None:
            student = Student.objects.filter(type_student=type_student)
        elif otm_id is not None:
            student = Student.objects.filter(OTM=otm_id)
        page = self.paginate_queryset(student)
        serializer = StudentSerializer(page, many=True, context={"request": request})
        if page is not None:
            serializer = self.get_paginated_response(StudentSerializer(page, many=True).data)
        else:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(manual_parameters=[token], parser_classes=parser_classes,
                         request_body=StudentSerializer)
    def post(self, request):
        data = request.data

        sponsor = Sponsor.objects.get(id=data['sponsor'])
        sponsor_b = sponsor.current_balance
        student_b = data['current_balance']
        contract_b = data['contract_balance']

        # if sponsor has money and student has not enough money
        if sponsor_b > 0 and student_b < contract_b:

            # if sponsor has not enough money to pay student
            if sponsor_b >= contract_b - student_b:
                sponsor.current_balance = sponsor_b - (contract_b - student_b)
                sponsor.save()
                data['current_balance'] = student_b + sponsor_b
            else:
                sponsor.current_balance = 0
                data['current_balance'] = student_b + sponsor_b
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    @swagger_auto_schema(manual_parameters=[token, student_id], parser_classes=parser_classes,
                         serializer_class=serializer_class)
    def put(self, request):
        student_id = request.data["student_id"]
        student = Student.objects.get(id=student_id)
        serializer = StudentSerializer(student, data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[token, student_id])
    def delete(self, request):
        student_id = request.data["student_id"]
        student = Student.objects.get(id=student_id)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from .pagination import LargeResultsSetPagination
from rest_framework.filters import SearchFilter
from rest_framework import filters
import django_filters.rest_framework
from rest_framework import authentication, permissions


class SponsorAPIView(generics.ListCreateAPIView):
    start_t = openapi.Parameter('start_t', in_=openapi.IN_QUERY, description='start time',
                                type=openapi.TYPE_STRING)
    end_t = openapi.Parameter('end_t', in_=openapi.IN_QUERY, description='end time',
                              type=openapi.TYPE_STRING)
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = SponsorSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)
    pagination_class = LargeResultsSetPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter]
    filter_fields = ['sponsorship_amount', 'application_status']
    queryset = Sponsor.objects.all()


class SponsorRetrieveUpdateDestroyAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = SponsorSerializer
    queryset = Sponsor.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)


class OTM_API(APIView, PaginationHandlerMixin):
    serializer_class = OTMSerializer
    pagination_class = BasicPagination
    parser_classes = (MultiPartParser, FormParser)
    token = openapi.Parameter(
        'Authorization',
        in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING
    )
    otm_id = openapi.Parameter('otm_id', in_=openapi.IN_QUERY, description="otm_id", type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token], )
    def get(self, request):
        otm = OTM.objects.all()
        page = self.paginate_queryset(otm)
        serializer = OTMSerializer(page, many=True, context={"request": request})
        if page is not None:
            serializer = self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(manual_parameters=[token], parser_classes=parser_classes, request_body=OTMSerializer)
    def post(self, request):
        serializer = OTMSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    @swagger_auto_schema(manual_parameters=[token, otm_id], parser_classes=parser_classes, request_body=OTMSerializer)
    def put(self, request):
        otm_id = request.data["otm_id"]
        otm = OTM.objects.get(id=otm_id)
        serializer = OTMSerializer(otm, data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[token, otm_id])
    def delete(self, request):
        otm_id = request.data["otm_id"]
        otm = OTM.objects.get(id=otm_id)
        if otm:
            otm.delete()
            return Response({"detail": f"{otm_id} is deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": f"{otm_id} is not found"}, status=status.HTTP_404_NOT_FOUND)


class SingleOTM_API(APIView):
    serializer_class = OTMSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)
    token = openapi.Parameter(
        'Authorization',
        in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING
    )
    otm_id = openapi.Parameter('otm_id', in_=openapi.IN_QUERY, description="otm_id", type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token, otm_id])
    def get(self, request):
        otm_id = request.query_params.get('otm_id')
        otm = OTM.objects.get(id=otm_id)
        serializer = OTMSerializer(otm, many=False, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class Members_Statistic(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)
    token = openapi.Parameter(
        'Authorization',
        in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[token])
    def get(self, request):
        students = Student.objects.all()
        sponsors = Sponsor.objects.all()
        student_count = students.count()
        sponsor_count = sponsors.count()
        return Response({"students": student_count, "sponsors": sponsor_count}, status=status.HTTP_200_OK)


