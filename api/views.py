from rest_framework.response import Response
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from .serializers import *
from django.http import Http404
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist



class ApiSummary(generics.GenericAPIView):

    permission_classes = (AllowAny,)

    def get(self,request):
        api_urls = {
            'API summary' :'api/',      
            'Session login' : 'api/api-auth/login/',
            'Session logout' : 'api/api-auth/logout/',
            'Obtain JWT auth token' : 'api/token/',
            'Refresh JWT auth token' : 'api/token/refresh/',
            'Plant List' : 'api/plants/',
            'Disease List' : 'api/diseases/',
            'Pesticide List' : 'api/pesticides',
            'Create Plant' : 'api/plant/create/',
            'Create Disease' :'api/disease/create/',
            'Create Pesticide ' : 'api/pesticide/create/',
            'Update Delete Plant' : 'api/plant/<int:pk>/',
            'Update Delete Disease' : 'api/disease/<int:pk>/',
            'Update Delete Pestcide' : 'api/pesticide/<int:pk>/',
            'Protection scheduler'  : 'api/protections/',
            'Update Delete protection' : 'api/protection/<int:pk>/',
            'Diary scheduler' : 'api/diaries/',
            'Update delete diary' : 'api/diary/<int:pk>/',
            'Create forum Message' : 'api/post/create/',
            'List all forum message' : 'api/posts/all/',
            'Forum message detail' : 'api/post/<int:pk>/',
            'Create reply under post ' : 'api/post/<int:pk>/reply/',
            'List replies in post ' : 'api/post/<int:pk>/replies/',
            'Reply detail'  : 'reply/<int:pk>/',
                        
            }
        
        return Response(api_urls)
    

class PlantListApiView(generics.ListAPIView):

    permission_classes = (AllowAny,)
    serializer_class = PlantSerializer
    queryset = Plant.objects.all()

class DiseaseListApiView(generics.ListAPIView):

    permission_classes = (AllowAny,)
    serializer_class = DiseaseSerialier
    queryset = Disease.objects.all()

class PesticideListApiView(generics.ListAPIView):

    permission_classes = (AllowAny,)
    serializer_class = PesticideSerialier
    queryset = Pesticide.objects.all()


class PlantCreateApiView(generics.CreateAPIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = PlantSerializer
    queryset = Plant.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class DiseaseCreateApiView(generics.CreateAPIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = DiseaseSerialier
    queryset = Disease.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PesticideCreateApiView(generics.CreateAPIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = PesticideSerialier
    queryset = Pesticide.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PlantUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = PlantSerializer
    queryset = Plant.objects.all()


    def perform_update(self, serializer):
        name = serializer.validated_data.get('name')
        slug = slugify(name)
        serializer.save(slug=slug)


class DiseaseUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = DiseaseSerialier
    queryset = Disease.objects.all()


    def perform_update(self, serializer):
        name = serializer.validated_data.get('name')
        slug = slugify(name)
        serializer.save(slug=slug)

class PesticideUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = PesticideSerialier
    queryset = Pesticide.objects.all()


    def perform_update(self, serializer):
        name = serializer.validated_data.get('name')
        slug = slugify(name)
        serializer.save(slug=slug)



class ScheduleProtectionApiView(generics.ListCreateAPIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProtectionSerializer
    queryset = Schedule_Protection.objects.all()

    def get_queryset(self):
        qs = super().get_queryset() 
        return qs.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        date = request.data['date']
        expire = request.data['expire']
        if expire <= date:
            return Response({'error': 'expiration date must before protection date'}, status=400)
        return super().create(request, *args, **kwargs)



class ProtectionUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProtectionSerializer
    queryset = Schedule_Protection.objects.all()
    
    def get_queryset(self):
        qs = super().get_queryset() 
        return qs.filter(author=self.request.user)
    
    def update(self, request, *args, **kwargs):
        date = request.data['date']
        expire = request.data['expire']
        if expire <= date:
            return Response({'error': 'expiration date must before protection date'}, status=400)
        return super().update(request, *args, **kwargs)

     

class CreateDiaryApiView(generics.ListCreateAPIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DiarySerializer
    queryset = Plant_diary.objects.all()


    def get_queryset(self):
        qs = super().get_queryset() 
        return qs.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        sowing = request.data['sowing']
        harvesting = request.data['harvesting']
        if harvesting:
            if harvesting <= sowing:
                return Response({'error': 'sowing date must before harwesting date'}, status=400)
        return super().create(request, *args, **kwargs)



class DiaryUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DiarySerializer
    queryset = Plant_diary.objects.all()
    
    def get_queryset(self):
        qs = super().get_queryset() 
        return qs.filter(author=self.request.user)
    
    def update(self, request, *args, **kwargs):
        sowing = request.data['sowing']
        harvesting = request.data['harvesting']
        if harvesting:
            if harvesting <= sowing:
                return Response({'error': 'harvesting date must before sowing date'}, status=400)
        return super().update(request, *args, **kwargs)



class ForumMessageListApiView(generics.ListAPIView):

    permission_classes = (AllowAny,)
    serializer_class = ForumMessageSerializer
    queryset = ForumMessage.objects.filter(enabled=True)


class ForumMessageListCreateApiView(generics.ListCreateAPIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ForumMessageSerializer
    queryset = ForumMessage.objects.all()

    def get_queryset(self):
        qs = super().get_queryset() 
        return qs.filter(author=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return super().perform_create(serializer)
    

class ForumMessageDeleteUpdateApiView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ForumMessageSerializer
    queryset = ForumMessage.objects.all()

    def get_queryset(self):
        qs = super().get_queryset() 
        return qs.filter(author=self.request.user)
    


class ForumMessageReplyCreateApiView(generics.ListCreateAPIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ForumReplyMessageSerializer
    queryset = ForumReplyMessage.objects.all()

    def get_message(self):
        pk = self.request.parser_context['kwargs']['pk']
        try:
            message = ForumMessage.objects.get(pk=pk)
        except: 
            message = {}
        return message
    

    def get_queryset(self):
        qs = super().get_queryset()
        message = self.get_message()
        if not message:
            raise Http404
        return qs.filter(author=self.request.user,message=message)


    def perform_create(self, serializer):
        message = self.get_message()
        if not message:
            raise Http404     
        serializer.save(author=self.request.user,message=message)
        return super().perform_create(serializer)
    


class ForumReplyListApiView(generics.ListAPIView):

    permission_classes = (AllowAny,)
    serializer_class = ForumReplyMessageSerializer
    queryset = ForumReplyMessage.objects.filter(enabled=True)

    def get_message(self):
        pk = self.request.parser_context['kwargs']['pk']
        try:
            message = ForumMessage.objects.get(pk=pk)
        except: 
            message = {}
        return message

    def get_queryset(self):
        qs = super().get_queryset()
        message = self.get_message()
        if not message:
            raise Http404
        return qs.filter(message=message)


class ReplyUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ForumReplyMessageSerializer
    queryset = ForumReplyMessage.objects.all()

    def get_queryset(self):
        qs = super().get_queryset() 
        return qs.filter(author=self.request.user)






    

