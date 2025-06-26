
from rest_framework import serializers
from django.http import JsonResponse
from garden_app.models import Plant,Disease,Pesticide,Schedule_Protection,Plant_diary,ForumMessage,ForumReplyMessage


class PlantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plant
        fields = ('id','name','description','category','diseases','image')
        read_only_fields = ('id',)
      
class DiseaseSerialier(serializers.ModelSerializer):

    class Meta:
        model = Disease
        fields = ('id','name','description','pesticides','image')
        read_only_fields = ('id',)


class PesticideSerialier(serializers.ModelSerializer):

     class Meta:
        model = Pesticide
        fields = ('id','name','description','category','link','image')
        read_only_fields = ('id',)

class ProtectionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Schedule_Protection
        fields = ('id','author','date','expire','note','plants','pesticide')
        read_only_fields = ('id','author')


class DiarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Plant_diary
        fields = ('id','author','sowing','harvesting','note','plants')
        read_only_fields = ('id','author')



class ForumMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ForumMessage
        fields = ('id','author','post','date')
        read_only_fields = ('id','author','date')

class ForumReplyMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ForumReplyMessage
        fields = ('id','author','reply','date')
        read_only_fields = ('id','author','date')
