from django.urls import path
from .views import StudentAPIView, SponsorAPIView, SponsorRetrieveUpdateDestroyAPIView, OTM_API, SingleOTM_API, \
    MyObtainTokenPairView,Members_Statistic
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('StudentAPI/', StudentAPIView.as_view(), name="student_api"),
    # path('StudentAPI/<int:pk>',StudentAPIView.as_view()),
    path('Sponsor_F/', SponsorAPIView.as_view(), name="sponsor_api"),
    path('Sponsor/', SponsorRetrieveUpdateDestroyAPIView.as_view(),
         name="Sponsor_RetrieveUpdateDestroy_api"),
    path('OTM_API/', OTM_API.as_view(), name="otm_api"),
    path('Single_OTM_API/', SingleOTM_API.as_view(), name="single_otm_api"),
    path('token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('Members_Statistic',Members_Statistic.as_view(),name='members_statistic')

]