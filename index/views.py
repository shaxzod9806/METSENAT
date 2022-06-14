import django_filters.rest_framework
from django.http import HttpResponse
from .models import Student, Sponsor, OTM
from .serializers import StudentSerializer, SponsorSerializer, OTMSerializer
from rest_framework.response import Response
from rest_framework import status, generics
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

otm_id = openapi.Parameter('otm_id', in_=openapi.IN_QUERY, description="otm_id",
                           type=openapi.TYPE_STRING)

student_id = openapi.Parameter('student_id', in_=openapi.IN_QUERY, description="student_id",
                               type=openapi.TYPE_INTEGER)
sponsor_id = openapi.Parameter('sponsor_id', in_=openapi.IN_QUERY, description="sponsor_id",
                               type=openapi.TYPE_INTEGER)


class StudentAPIView(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = BasicPagination
    serializer_class = StudentSerializer
    parser_classes = (MultiPartParser, FormParser)
    type_id = openapi.Parameter('type_student', in_=openapi.IN_QUERY, description="type_student",
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
        request.data._mutable = True
        data = request.data
        sponsor = Sponsor.objects.get(id=data['sponsor'])
        sponsor_b = sponsor.current_balance
        student_b = float(data['current_balance'])
        contract_b = float(data['contract_amount'])

        # if sponsor has money and student has not enough money
        if sponsor_b > 0 and student_b < contract_b:

            # if sponsor has not enough money to pay student
            if sponsor_b >= contract_b - student_b:
                sponsor.current_balance = sponsor_b - (contract_b - student_b)
                sponsor.save()
                print(student_b + sponsor_b)
                data['current_balance'] = student_b + sponsor_b
            elif sponsor_b == 0:
                return Response({"message": "Sponsor has no enough money"}, status=status.HTTP_400_BAD_REQUEST)
            elif contract_b <= data['current_balance']:
                return Response({"message": "Student has enough money"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                sponsor.current_balance = 0
                data['current_balance'] = student_b + sponsor_b
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


# class SponsorAPIView(generics.ListCreateAPIView, MultipleFieldLookupMixin, ):
#     start_t = openapi.Parameter('start_t', in_=openapi.IN_QUERY, description='start time',
#                                 type=openapi.TYPE_STRING)
#     end_t = openapi.Parameter('end_t', in_=openapi.IN_QUERY, description='end time',
#                               type=openapi.TYPE_STRING)
#     authentication_classes = [authentication.TokenAuthentication]
#     serializer_class = SponsorSerializer
#     permission_classes = [permissions.IsAdminUser]
#     parser_classes = (MultiPartParser, FormParser)
#     pagination_class = LargeResultsSetPagination
#     filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter]
#     filter_fields = ['sponsorship_amount', 'application_status']
#     queryset = Sponsor.objects.all()


class SponsorAPIView(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = BasicPagination
    serializer_class = SponsorSerializer
    parser_classes = (MultiPartParser, FormParser)

    start_t = openapi.Parameter('start_t', in_=openapi.IN_QUERY, description='start time',
                                type=openapi.TYPE_STRING)
    end_t = openapi.Parameter('end_t', in_=openapi.IN_QUERY, description='end time',
                              type=openapi.TYPE_STRING)
    application_status = openapi.Parameter('application_status', in_=openapi.IN_QUERY, description='application_status',
                                           type=openapi.TYPE_STRING)
    sponsorship_amount = openapi.Parameter('sponsorship_amount', in_=openapi.IN_QUERY, description='sponsorship_amount',
                                           type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token, start_t, end_t, application_status, sponsorship_amount])
    def get(self, request):
        start = request.query_params.get('start_t')
        end = request.query_params.get('end_t')
        start_t = datetime.strptime(start, "%m/%d/%Y")  # 10/12/2013 type: datetime
        end_t = datetime.strptime(end, "%m/%d/%Y")
        print("start: ", start_t)
        print("start: ===============", start)
        application_status = request.query_params.get('application_status')
        sponsorship_amount = request.query_params.get('sponsorship_amount')
        # print("start_t: ", start_t)
        # print("end_t: ", end_t)
        # print("application_status: ", application_status)
        # print("sponsorship_amount: ", sponsorship_amount)
        sponsors = Sponsor.objects.filter(application_status=application_status, sponsorship_amount=sponsorship_amount,
                                          created_at__range=(start_t, end_t)  # worked
                                          # created_at__gte=start_t, created_at__lte=end_t #worked
                                          )

        serializer = SponsorSerializer(sponsors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(manual_parameters=[token], parser_classes=parser_classes, request_body=SponsorSerializer)
    def post(self, request):
        data = request.data
        serializer = SponsorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class SingleSponsorAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(manual_parameters=[token, sponsor_id])
    def get(self, request):
        sponsor_id = request.query_params.get('sponsor_id')
        sponsor = Sponsor.objects.get(id=sponsor_id)
        if sponsor is not None:
            serializer = SponsorSerializer(sponsor, many=False, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Sponsor not found"}, status=status.HTTP_404_NOT_FOUND)


class SponsorRetrieveUpdateDestroyAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = SponsorSerializer
    queryset = Sponsor.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)


class OTMAPI(APIView, PaginationHandlerMixin):
    serializer_class = OTMSerializer
    pagination_class = BasicPagination
    parser_classes = (MultiPartParser, FormParser)

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


class SingleOTMAPI(APIView):
    serializer_class = OTMSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(manual_parameters=[token, otm_id])
    def get(self, request):
        otm_id = request.query_params.get('otm_id')
        otm = OTM.objects.get(id=otm_id)
        serializer = OTMSerializer(otm, many=False, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class MembersStatistic(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(manual_parameters=[token])
    def get(self, request):
        students = Student.objects.all()
        sponsors = Sponsor.objects.all()
        student_count = students.count()
        sponsor_count = sponsors.count()
        return Response({"students": student_count, "sponsors": sponsor_count}, status=status.HTTP_200_OK)
