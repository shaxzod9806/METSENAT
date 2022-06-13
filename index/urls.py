from django.urls import path
from .views import StudentAPIView, SponsorAPIView, SponsorRetrieveUpdateDestroyAPIView, OTMAPI, SingleOTMAPI, \
    MyObtainTokenPairView, MembersStatistic
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('StudentAPI/', StudentAPIView.as_view(), name="student_api"),
    # path('StudentAPI/<int:pk>',StudentAPIView.as_view()),
    path('SponsorFilter/', SponsorAPIView.as_view(), name="sponsor_api"),
    path('Sponsor/', SponsorRetrieveUpdateDestroyAPIView.as_view(),
         name="Sponsor_RetrieveUpdateDestroy_api"),
    path('OTMAPI/', OTMAPI.as_view(), name="otm_api"),
    path('SingleOTMAPI/', SingleOTMAPI.as_view(), name="single_otm_api"),
    path('token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('MembersStatistic', MembersStatistic.as_view(), name='members_statistic')

]
