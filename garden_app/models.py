from django.db import models
from tinymce.models import HTMLField
from PIL import Image
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
from  django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django_resized import ResizedImageField
from django.utils.text import slugify
from django.utils import timezone





class UserProfile(models.Model):

    image = ResizedImageField(size=[800, 600], upload_to='images/diseases',null=True)
    bio = HTMLField(blank=True,max_length=3000)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


@receiver(post_save, sender=User)
def handler_function(sender, instance, created, **kwargs):
    if  created:
        user_profile = UserProfile(user=instance)
        user_profile.save()



class Pesticide(models.Model):

    CATEGORY = (

        ('fungicide','fungicide'),
        ('insecticide','insecticide'),
        ('Other','Other')
      
    )

    name = models.CharField(max_length=250)
    slug = models.SlugField(blank=True,unique=True)
    description = HTMLField(max_length=3000)
    image =  ResizedImageField(size=[800, 600], upload_to='images/pesticides',null=True)
    category = models.CharField(max_length=30,choices=CATEGORY,default='Other')
    link = models.URLField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

@receiver(pre_save, sender=Pesticide)
def pesticide_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


class Disease(models.Model):

    name = models.CharField(max_length=250)
    slug = models.SlugField(blank=True,unique=True)
    description = HTMLField(max_length=3000)
    image = ResizedImageField(size=[800, 600], upload_to='images/diseases',null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    pesticides = models.ManyToManyField(Pesticide)

    def __str__(self):
        return self.name


    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    

@receiver(pre_save, sender=Disease)
def disease_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)




class Plant(models.Model):

    TYPE = (

        ("Vegetables","Vegetables"),
        ("Fruits","Fruits"),
        ("Flowers","Flowers"),
        ("Ornamentals","Ornamentals"),
        ("Other","Other"),

    )


    name = models.CharField(max_length=250)
    slug = models.SlugField(blank=True,unique=True)
    image = ResizedImageField(size=[800, 600], upload_to='images/vegetables',null=True)
    description = HTMLField(max_length=3000)
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    diseases = models.ManyToManyField(Disease)
    category = models.CharField(max_length=15,choices=TYPE,default="Other")
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name


    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
@receiver(pre_save, sender=Plant)
def vegetables_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)



class Schedule_Protection(models.Model):

    date = models.DateField(default=timezone.now)
    expire = models.DateField(default=timezone.now)
    note = HTMLField(blank=True,max_length=1000)
    plants = models.ManyToManyField(Plant)
    pesticide = models.ManyToManyField(Pesticide)
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    

    def __str__(self):
        return str(self.date)


class Plant_diary(models.Model):

    plants = models.ManyToManyField(Plant)
    note =  HTMLField(blank=True,max_length=1000)
    sowing = models.DateField(default=timezone.now)
    harvesting = models.DateField(default=timezone.now, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
   

    def __str__(self):
        return str(self.sowing)
    


class About_content(models.Model):

    title1 = models.CharField(max_length=200)
    subtitle1 = HTMLField(blank=True,max_length=1000)
    title2 = models.CharField(max_length=200)
    subtitle2 =  HTMLField(blank=True,max_length=1000)
    title3 =  models.CharField(max_length=200)
    subtitle3 =  HTMLField(blank=True,max_length=1000)
    image = ResizedImageField(size=[800, 600], upload_to='images/about',null=True)
    icon1 = models.CharField(max_length=50,null=True)
    icon2 = models.CharField(max_length=50,null=True)


    def __str__(self):
        return self.title1
    

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    

class ContactMessage(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    message = models.TextField(max_length=3000)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}-{self.last_name}'
    



class ForumMessage(models.Model):
    
    post = HTMLField(max_length=2000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return str(self.author)


class ForumReplyMessage(models.Model):

    reply = HTMLField(max_length=2000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(ForumMessage,related_name='reply_to', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return str(self.author)



