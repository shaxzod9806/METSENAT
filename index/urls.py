from django.urls import path
from .views import StudentAPIView, SponsorAPIView, SponsorRetrieveUpdateDestroyAPIView, OTMAPI, SingleOTMAPI, \
    MyObtainTokenPairView, MembersStatistic, SingleStudentAPIView, SingleSponsorAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('StudentAPI/', StudentAPIView.as_view(), name="student_api"),
    path('SingleStudentAPIView', SingleStudentAPIView.as_view(), name="SingleStudentAPIView"),
    path('SponsorFilter/', SponsorAPIView.as_view(), name="sponsor_api"),
    path('Sponsor/', SponsorRetrieveUpdateDestroyAPIView.as_view()),
    path('SingleSponsorAPIView/', SingleSponsorAPIView.as_view(), name="SingleSponsorAPIView"),
    path('OTMAPI/', OTMAPI.as_view(), name="otm_api"),
    path('SingleOTMAPI/', SingleOTMAPI.as_view(), name="single_otm_api"),
    path('token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('MembersStatistic', MembersStatistic.as_view(), name='members_statistic')

]
