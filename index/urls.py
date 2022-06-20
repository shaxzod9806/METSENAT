from django.urls import path
from .views import MyObtainTokenPairView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import StudentAPIView, SingleStudentAPIView

urlpatterns = [
    path('Students/', StudentAPIView.as_view(), name='Students'),
    path('SingleStudentAPIView/', SingleStudentAPIView.as_view(), name='SingleStudentAPIView'),
    path('token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
