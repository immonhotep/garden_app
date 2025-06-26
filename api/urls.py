from django.urls import path,include
from . import views
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


urlpatterns = [

    path('',ApiSummary.as_view(), name="api-summary"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('plants/',PlantListApiView.as_view(),name='api_list_plants'),
    path('diseases/',DiseaseListApiView.as_view(),name='api_list_diseases'),
    path('pesticides/',PesticideListApiView.as_view(),name='api_list_pesticides'),
    path('plant/create/',PlantCreateApiView.as_view(),name='api_create_plants'),
    path('disease/create/',DiseaseCreateApiView.as_view(),name='api_create_disease'),
    path('pesticide/create/',PesticideCreateApiView.as_view(),name='api_create_pesticide'),
    path('plant/<int:pk>/',PlantUpdateDeleteApiView.as_view(),name='api_plant_detail'),
    path('disease/<int:pk>/',DiseaseUpdateDeleteApiView.as_view(),name='api_disease_detail'),
    path('pesticide/<int:pk>/',PesticideUpdateDeleteApiView.as_view(),name='api_pesticide_detail'),
    path('protections/',ScheduleProtectionApiView.as_view(),name='api_list_create_protections'),
    path('protection/<int:pk>/',ProtectionUpdateDeleteApiView.as_view(),name='api_protection_detail'),
    path('diaries/',CreateDiaryApiView.as_view(),name='api_list_create_diary'),
    path('diary/<int:pk>/',DiaryUpdateDeleteApiView.as_view(),name='api_diary_detail'),
    path('post/create/',ForumMessageListCreateApiView.as_view(),name='api_post_create'),
    path('posts/all/',ForumMessageListApiView.as_view(),name='api_all_posts'),
    path('post/<int:pk>/',ForumMessageDeleteUpdateApiView.as_view(),name='api_post_detail'),
    path('post/<int:pk>/reply/',ForumMessageReplyCreateApiView.as_view(),name='api_create_reply'),
    path('post/<int:pk>/replies/',ForumReplyListApiView.as_view(),name='api_list_reply'),
    path('reply/<int:pk>/',ReplyUpdateDeleteApiView.as_view(),name='reply_detail'),

]