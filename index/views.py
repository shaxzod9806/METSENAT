import django_filters.rest_framework
from django.http import HttpResponse
from .models import Student
from .serializers import StudentSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
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

from .pagination import LargeResultsSetPagination
from rest_framework.filters import SearchFilter
from rest_framework import filters
import django_filters.rest_framework
from rest_framework import authentication, permissions
from datetime import datetime, timedelta
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


token = openapi.Parameter(
    'Authorization',
    in_=openapi.IN_HEADER,
    description='enter access token with Bearer word for example: Bearer token',
    type=openapi.TYPE_STRING
)
student_id = openapi.Parameter('student_id', in_=openapi.IN_QUERY, description="student_id",
                               type=openapi.TYPE_INTEGER)


class StudentAPIView(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = BasicPagination
    serializer_class = StudentSerializer
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(manual_parameters=[token])
    def get(self, request):
        students = Student.objects.all()
        page = self.paginate_queryset(students)
        serializer = StudentSerializer(page, many=True, context={"request": request})
        if page is not None:
            serializer = self.get_paginated_response(StudentSerializer(page, many=True).data)
        else:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(manual_parameters=[token], parser_classes=parser_classes,
                         request_body=StudentSerializer)
    def post(self, request):
        request.data._mutable = True
        data = request.data
        request.data._mutable = False
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    @swagger_auto_schema(manual_parameters=[token, student_id], parser_classes=parser_classes,
                         request_body=StudentSerializer)
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


# get one student
class SingleStudentAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = StudentSerializer

    @swagger_auto_schema(manual_parameters=[token, student_id])
    def get(self, request):
        student_id = request.query_params.get('student_id')
        student = Student.objects.get(id=student_id)
        if student is not None:
            serializer = StudentSerializer(student, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
