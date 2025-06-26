from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('signup/',SignupView.as_view(),name='user_signup'),
    path('signin/',SignInView.as_view(),name='user_signin'),
    path('signout/',SignOutView.as_view(),name='user_signout'),
    path('profile/<int:pk>/',UserProfileDetail.as_view(),name='profile'),
    path('update-profile/',UpdateUser.as_view(),name='user_profile'),
    path('password-change/',PasswordChange.as_view(),name='password_change'),
    path('create-plant/',CreatePlant.as_view(),name='create_plant'),
    path('plant-detail/<slug:slug>/',PlantDetail.as_view(),name='plant_detail'),
    path('update-plant/<slug:slug>/',UpdatePlant.as_view(),name='update_plant'),
    path('delete-plant/<slug:slug>/',DeletePlant.as_view(),name='delete_plant'),
    path('list-diseases/',DiseaseView.as_view(),name='list_diseases'),
    path('create-disease/',CreateDisease.as_view(),name='create_disease'),
    path('disease-detail/<slug:slug>/',DiseaseDetail.as_view(),name='disease_detail'),
    path('update-disease/<slug:slug>/',UpdateDisease.as_view(),name='update_disease'),
    path('delete-disease/<slug:slug>/',DeleteDisease.as_view(),name='delete_disease'),
    
    path('list-pesticides/',PesticideView.as_view(),name='list_pesticides'),
    path('create_pesticide/',CreatePesticide.as_view(),name='create_pesticide'),
    path('pesticide-detail/<slug:slug>/',PesticideDetail.as_view(),name='pesticide_detail'),
    path('update-pesticide/<slug:slug>/',UpdatePesticide.as_view(),name='update_pesticide'),
    path('delete-pesticide/<slug:slug>/',DeletePesticide.as_view(),name='delete_pesticide'),

    path('search-plant/',SearchPlant.as_view(),name='search_plant'),
    path('search-diseases/',SearchDisease.as_view(),name='search_diseases'),
    path('Search-pesticide/',SearchPesticide.as_view(),name='search_pesticides'),

    path('plant-category/<str:category>/',PlantCategoryView.as_view(),name='plant_category'),

    path('schedule-protection/',ScheduleProtection.as_view(),name='schedule_protection'),
    path('list-protection-schedules',ProtectionScheduleList.as_view(),name='list_protection_schedules'),
    path('update-protection/<int:pk>/',UpdateProtectionScedule.as_view(),name='update_protection'),
    path('delete-protection/<int:pk>/',DeleteScheduleProtection.as_view(),name='delete_protection'),
    path('create-diary/',CreateDiary.as_view(),name='create_diary'),
    path('list-diaries/',DiaryList.as_view(),name='list_diaries'),
    path('update-diary/<int:pk>/',UpdateDiary.as_view(),name='update_diary'),
    path('delete-diary/<int:pk>/',DeleteDiary.as_view(),name='delete_diary'),

    path('account_activation/<uidb64>/<token>', views.account_activation, name='account_activation'),

    path('forum/',Forum.as_view(),name='forum'),
    path('reply/<int:pk>/',Reply.as_view(),name='reply'),
    path('delete-post/<int:pk>/',DeleteForumPost.as_view(),name='delete_post'),
    path('update-post/<int:pk>/',UpdateForumPost.as_view(),name='update_post'),
    path('delete-reply/<int:pk>/',DeleteForumReplyPost.as_view(),name='delete_reply'),
    path('update-reply/<int:pk>/',UpdateForumReply.as_view(),name='update_reply'),
    path('comment-status/<int:pk>/',CommentStatus.as_view(),name='comment_status'),
    path('reply-status/<int:pk>/',ReplyStatus.as_view(),name='reply_status'),

    path('update-about/',UpdateAboutPage.as_view(),name='update_about'),
    path('about/',AboutPage.as_view(),name='about'),
    path('create-contact-message',SendContactMessage.as_view(),name='contact_message'),
    path('list-contact-messages/',ListContactMessages.as_view(),name='list_contact_messages'),

    path('users/',ListUsers.as_view(),name='users'),
    path('user-status/<int:pk>/',UserStatus.as_view(),name='user_status'),
    path('403/',Forbidden.as_view(),name='403_page')
  
]