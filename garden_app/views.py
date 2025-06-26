from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse,reverse_lazy
from .mixins import SuperUserRequiredMixin
from django.shortcuts import render
from django.views.generic import View,CreateView,ListView,UpdateView,DetailView,TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth import update_session_auth_hash
from .forms import SigInForm,Signupform,UserForm,ProfileForm,PlantForm,DiseaseForm,PesticideForm,ProtectionForm,DiaryForm,AboutPageForm,ChangePasswordForm,ForumForm,\
ForumReplyForm,ForumUpdateForm,ForumReplyUpdateForm

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import UserProfile,Plant,Disease,Pesticide,Schedule_Protection,Plant_diary,About_content,ContactMessage,ForumMessage,ForumReplyMessage
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.utils.text import slugify
from datetime import datetime
import re
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required



from django.contrib.auth.views import PasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
#prevent error related force_text not found
from django.utils.encoding import force_str as force_text

from django.core.mail import send_mail


class HomeView(ListView):

    model = Plant
    template_name = 'main/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        random_plant = Plant.objects.all().order_by('?').first()
        try:
            plants = Plant.objects.all().exclude(pk=random_plant.pk).order_by('-name')
        except:
            plants = Plant.objects.all().order_by('-name')

        
        p = Paginator(plants,6)
        page = self.request.GET.get('page')

        try:
            plants = p.page(page)
        except PageNotAnInteger:
            plants = p.page(1)
        except EmptyPage:
            plants = p.page(p.num_pages)

        context['random_plant']  = random_plant
        context['plants'] = plants
        return context
    

class DiseaseView(ListView):

    model = Disease
    template_name = 'main/diseases.html'
    
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        random_disease = Disease.objects.all().order_by('?').first()
        if random_disease:
            pesticides = random_disease.pesticides.all()
            plants = Plant.objects.filter(diseases__in=[random_disease.id])
            diseases = Disease.objects.all().exclude(pk=random_disease.pk).order_by('-name')
        else:
            pesticides = {}
            plants = {}
            diseases = Disease.objects.all().order_by('-name')

                   
        p = Paginator(diseases,6)
        page = self.request.GET.get('page')

        try:
            diseases = p.page(page)
        except PageNotAnInteger:
            diseases = p.page(1)
        except EmptyPage:
            diseases = p.page(p.num_pages)

        context['plants'] = plants
        context['pesticides'] = pesticides
        context['random_disease']  = random_disease
        context['diseases'] = diseases
        return context
    

class PesticideView(ListView):

    model = Pesticide
    template_name = 'main/pesticides.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        random_pesticide = Pesticide.objects.all().order_by('?').first()
        if random_pesticide:
            diseases = Disease.objects.filter(pesticides__in=[random_pesticide.id])
            plants = Plant.objects.filter(diseases__in=diseases)
            pesticides = Pesticide.objects.all().exclude(pk=random_pesticide.pk).order_by('-name')
        else:
            pesticides = Pesticide.objects.all().order_by('-name')
            diseases = {}
            plants = {}
             
        p = Paginator(pesticides,6)
        page = self.request.GET.get('page')

        try:
            pesticides = p.page(page)
        except PageNotAnInteger:
            pesticides = p.page(1)
        except EmptyPage:
            pesticides = p.page(p.num_pages)

        context['plants'] = plants
        context['diseases'] = diseases
        context['random_pesticide']  = random_pesticide
        context['pesticides'] = pesticides
        return context


class SignupView(View):

    def get(self,request):
        form = Signupform()
        context = {'form':form,'header':'Create an account'}
        return render(request,'main/authform.html',context)
    
    def post(self,request):
        form = Signupform(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(self.request)

            subject = 'Activate Your Account'
            message = render_to_string('settings/account_activation_email.html', {
            'user':user,
            'domain':current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),})
           
            try:
                user.email_user(subject=subject, message=message)              
                messages.success(self.request,'To finish registration please check your mailbox including spam folder and follow instructions')
                return redirect('user_signin')
            except:
                messages.error(self.request,'Mail Server Connection problem, please turn to website admin')
        
        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(self.request, "You must pass the reCAPTCHA test")
                    continue
                messages.error(self.request, error)
            
              
        return redirect('user_signup')
    

def account_activation(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)    
    except():
        pass

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Your registration finished now please login')
        return redirect('user_signin')

    else:
        return render(request, 'settings/activation_invalid.html')


class SignInView(SuccessMessageMixin,LoginView):

    template_name = 'main/authform.html'
    form_class = SigInForm

    def get_success_message(self, cleaned_data):
        return(f'Welcome {self.request.user}')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Login'
        return context
    

    def form_invalid(self, form):
        for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(self.request, "You must pass the reCAPTCHA test")
                    continue
                messages.error(self.request, error)
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('home')
    

class SignOutView(View):

    def post(self,request):
        messages.success(request,'Bye ...See you next time')
        logout(request)
        return redirect('home')
    

class UserProfileDetail(LoginRequiredMixin,DetailView):

    template_name="main/profile.html"
    model = UserProfile

    def get_context_data(self,*args, **kwargs):
        context = super(UserProfileDetail,self).get_context_data(*args,**kwargs)
        profile = get_object_or_404(UserProfile,pk=self.kwargs['pk'])
        context['profile'] = profile
        return context





class UpdateUser(LoginRequiredMixin,View):

    def get(self,request):
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)
        context = {'user_form':user_form,'profile_form':profile_form}
        return render(request,'main/update_profile.html',context)

    def post(self,request):

        user_form = UserForm(request.POST,instance=request.user)
        profile_form = ProfileForm(request.POST,request.FILES,instance=request.user.userprofile)

        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile updated')
            return redirect('home')
        else:
            for error in list(user_form.errors.values()):
                messages.error(request,error)
            for error in list(profile_form.errors.values()):
                messages.error(request,error)
            return redirect('user_profile')
        

class PasswordChange(LoginRequiredMixin,View):

    def get(self,request):

        form = ChangePasswordForm(user=request.user)
        context = {'form':form,'header':'Change your password'}
        return render(request,'main/forms.html',context)
    
    def post(self,request):
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,request.user)
            messages.success(request,'Your password has been changed')   
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
            return redirect('password_change')
        return redirect('home')


class CreatePlant(SuperUserRequiredMixin,View):

    def get(self,request):
        form = PlantForm()
        context = {'form':form,'header':'Create Plant'}
        return render(request,'main/forms.html',context)
    
    def post(self,request):
        form = PlantForm(request.POST,request.FILES)
        if form.is_valid():
            plant = form.save(commit=True)
            plant.author = request.user
            plant.save()
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
                return redirect('create_plant')
            
        messages.success(request,f'{plant.name} created')
        return redirect('home')
            

class CreateDisease(SuperUserRequiredMixin,View):

    def get(self,request):
        form = DiseaseForm()
        context = {'form':form,'header':'Create Disease'}
        return render(request,'main/forms.html',context)
    
    def post(self,request):
        form = DiseaseForm(request.POST,request.FILES)
        if form.is_valid():
            disease = form.save(commit=True)
            disease.author = request.user
            disease.save()
            messages.success(request,f'{disease.name} created')
            return redirect('home')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
                return redirect('create_disease')


class CreatePesticide(SuperUserRequiredMixin,View):

    def get(self,request):
        form = PesticideForm()
        context = {'form':form,'header':'Create pesticide'}
        return render(request,'main/forms.html',context)
    
    def post(self,request):
        form = PesticideForm(request.POST,request.FILES)
        if form.is_valid():
            pesticide = form.save(commit=False)
            pesticide.author = request.user
            pesticide.save()
            messages.success(request,f'{pesticide.name} created')
            return redirect('home')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
                return redirect('create_disease')


class PlantDetail(DetailView):

    model = Plant
    template_name = 'main/plant-detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        plant = get_object_or_404(Plant,slug=self.kwargs['slug'])
        plants = Plant.objects.filter(category__iexact=plant.category).exclude(pk=plant.pk)
        context['plant'] = plant
        context['plants'] = plants
        return context
    

class DiseaseDetail(DetailView):

    model = Disease
    template_name = 'main/disease-detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        disease = get_object_or_404(Disease,slug=self.kwargs['slug'])
        plants = Plant.objects.filter(diseases__in=[disease.id])

        context['disease'] = disease
        context['plants'] = plants
        return context
    

class PesticideDetail(DetailView):

    model = Pesticide
    template_name = 'main/pesticide-detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        pesticide = get_object_or_404(Pesticide,slug=self.kwargs['slug'])
        diseases = Disease.objects.filter(pesticides__in=[pesticide.pk])
        pesticides  = Pesticide.objects.filter(category__iexact=pesticide.category).exclude(pk=pesticide.pk)

              
        context['diseases'] = diseases
        context['pesticide'] = pesticide
        context['pesticides'] = pesticides
        return context


class SearchPlant(View):

    def get(self,request):
        search = request.GET.get('search',"")

        if search :
            plants = Plant.objects.filter(Q(name__icontains=search)|Q(description__icontains=search)).order_by('-date') 
            p = Paginator(plants,6)
            page = self.request.GET.get('page')
            try:
                plants = p.page(page)
            except PageNotAnInteger:
                plants = p.page(1)
            except EmptyPage:
                plants = p.page(p.num_pages)       
        else:
            plants = {}

        
        context = {'plants':plants}
        return render(request,'main/home.html',context)


class SearchDisease(View):

    def get(self,request):
        search = request.GET.get('search',"")

        if search:
            diseases = Disease.objects.filter(Q(name__icontains=search)|Q(description__icontains=search)).order_by('-name') 

            p = Paginator(diseases,6)
            page = self.request.GET.get('page')
            try:
                diseases = p.page(page)
            except PageNotAnInteger:
                diseases = p.page(1)
            except EmptyPage:
                diseases = p.page(p.num_pages)       
        else:
            diseases = {}

        

        context = {'diseases':diseases}
        return render(request,'main/diseases.html',context)
    

class SearchPesticide(View):

    def get(self,request):
        search = request.GET.get('search',"")

        if search:
            pesticides = Pesticide.objects.filter(Q(name__icontains=search)|Q(description__icontains=search)).order_by('-name')    

            p = Paginator(pesticides,6)
            page = self.request.GET.get('page')
            try:
                pesticides = p.page(page)
            except PageNotAnInteger:
                pesticides = p.page(1)
            except EmptyPage:
                pesticides = p.page(p.num_pages)

        else:
            pesticides = {}

        context = {'pesticides':pesticides}
        return render(request,'main/pesticides.html',context)


class UpdatePlant(SuperUserRequiredMixin,View):

    def get(self,request,slug):
        plant = get_object_or_404(Plant,slug=slug)
        form = PlantForm(instance=plant)
        context = {'form':form,'header':'Update Plant'}
        return render(request,'main/forms.html',context)

    def post(self,request,slug):
        plant = get_object_or_404(Plant,slug=slug)
        form = PlantForm(request.POST,request.FILES,instance=plant)
        if form.is_valid():
            plant=form.save(commit=True)
            plant.slug = slugify(plant.name)
            plant.save()
            messages.success(request,f'{plant} updated')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
            return redirect('update_plant',slug)
        return redirect('home')
        


class UpdateDisease(SuperUserRequiredMixin,View):

    def get(self,request,slug):
        disease = get_object_or_404(Disease,slug=slug)
        form = DiseaseForm(instance=disease)
        context = {'form':form,'header':'Update Disease'}
        return render(request,'main/forms.html',context)

    def post(self,request,slug):
        disease = get_object_or_404(Disease,slug=slug)
        form = DiseaseForm(request.POST,request.FILES,instance=disease)
        if form.is_valid():
            disease=form.save(commit=True)
            disease.slug = slugify(disease.name)
            disease.save()
            messages.success(request,f'{disease} updated')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
            return redirect('update_disease',slug)
        return redirect('list_diseases')


class UpdatePesticide(SuperUserRequiredMixin,View):

    def get(self,request,slug):
        pesticide = get_object_or_404(Pesticide,slug=slug)
        form = PesticideForm(instance=pesticide)
        context = {'form':form,'header':'Update Pesticide'}
        return render(request,'main/forms.html',context)

    def post(self,request,slug):
        pesticide = get_object_or_404(Pesticide,slug=slug)
        form = PesticideForm(request.POST,request.FILES,instance=pesticide)
        if form.is_valid():
            pesticide=form.save(commit=True)
            pesticide.slug = slugify(pesticide.name)
            pesticide.save()
            messages.success(request,f'{pesticide} updated')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
            return redirect('update_pesticide',slug)
        return redirect('list_pesticides')
    

class DeletePlant(SuperUserRequiredMixin,View):

    def post(self,request,slug):

        plant = get_object_or_404(Plant,slug=slug)       
        plant.delete()
        messages.success(request,f'{plant} deleted')
        return redirect('home')
    
class DeleteDisease(SuperUserRequiredMixin,View):

    def post(self,request,slug):

        disease = get_object_or_404(Disease,slug=slug)
        disease.delete()
        messages.success(request,f'{disease} deleted')
        return redirect('list_diseases')
    
class DeletePesticide(SuperUserRequiredMixin,View):

    def post(self,request,slug):

        pesticide = get_object_or_404(Pesticide,slug=slug)
        pesticide.delete()
        messages.success(request,f'{pesticide} deleted')
        return redirect('list_pesticides')
    

class DeleteScheduleProtection(LoginRequiredMixin,View):

    def post(self,request,pk):

        schedule = get_object_or_404(Schedule_Protection,pk=pk)
        if schedule.author != request.user:
            return redirect('403_page')
        
        schedule.delete()
        messages.success(request,f'{schedule} deleted')
        return redirect('list_protection_schedules')
    

class DeleteDiary(LoginRequiredMixin,View):

    def post(self,request,pk):

        diary = get_object_or_404(Plant_diary,pk=pk)
        if diary.author != request.user:
            return redirect('403_page')
        
        diary.delete()
        messages.success(request,f'{diary} deleted')
        return redirect('list_diaries')

    

class PlantCategoryView(View):

    def get(self,request,category):

        random_plant = Plant.objects.filter(category__iexact=category).order_by('?').first()
        try:
            plants = Plant.objects.filter(category__iexact=category).exclude(pk=random_plant.pk).order_by('name')
        except:
            plants = Plant.objects.filter(category__iexact=category).order_by('name')


        p = Paginator(plants,2)
        page = self.request.GET.get('page')

        try:
            plants = p.page(page)
        except PageNotAnInteger:
            plants = p.page(1)
        except EmptyPage:
            plants = p.page(p.num_pages)
        context = {'plants':plants,'random_plant':random_plant}
        return render(request,'main/home.html',context)
    

class ScheduleProtection(LoginRequiredMixin,View):

    def get(self,request):

        form = ProtectionForm()
        context = {'form':form,'header':'Schedule protection'}
        return render(request,'main/forms.html',context)

    def post(self,request):

        form = ProtectionForm(request.POST)
        if form.is_valid():

            date = form.cleaned_data['date']
            expire = form.cleaned_data['expire']

            if expire:
                if date >= expire:
                    messages.error(request,'Expire date must before the protection date')
                    return redirect('schedule_protection')

            #Must be commit=True due unknow crispy form error, witch prevent inlinecheckboxes to save when settings is False)
            protection = form.save(commit=True)
            protection.author = request.user
            protection.save()
            messages.success(request,f'protection date: {protection.date} saved' )
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
                return redirect('schedule_protection')
            
        return redirect('home')
   

class CreateDiary(LoginRequiredMixin,View):

    def get(self,request):

        form = DiaryForm()
        context = {'form':form,'header':'Create Diary'}
        return render(request,'main/forms.html',context)

    def post(self,request):

        form = DiaryForm(request.POST)
        if form.is_valid():
            
            sowing = form.cleaned_data['sowing'] 
            harvesting = form.cleaned_data['harvesting']

            if harvesting:
                if sowing >= harvesting:
                    messages.error(request,'Sowing date must before the harvesting date')
                    return redirect('create_diary')
            
            diary = form.save(commit=True)
            diary.author = request.user
            diary.save()
            messages.success(request,f'protection date: {diary.sowing} saved' )
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
                return redirect('create_diary')
            
        return redirect('home')

    

class UpdateProtectionScedule(LoginRequiredMixin,View):

    def get(self,request,pk):

        schedule = get_object_or_404(Schedule_Protection,pk=pk)

        if schedule.author != request.user:
            return redirect('403_page')

        form = ProtectionForm(instance=schedule)
        context = {'form':form,'header':'Update protection'}
        return render(request,'main/forms.html',context)
    
    def post(self,request,pk):

        schedule = get_object_or_404(Schedule_Protection,pk=pk)

        if schedule.author != request.user:
            return redirect('403_page')
        
        form = ProtectionForm(request.POST,instance=schedule)
        if form.is_valid():

            date = form.cleaned_data['date']
            expire = form.cleaned_data['expire']
        
            if expire:
                if date >= expire:
                    messages.error(request,'Protection date must before the protection expiration date')
                    return redirect('update_protection',pk)

            schedule = form.save(commit=True)
            messages.success(request,f'{schedule.date} updated')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
                return redirect('update_protection',pk)
        return redirect('list_protection_schedules')
    

class UpdateDiary(LoginRequiredMixin,View):

    def get(self,request,pk):

        diary = get_object_or_404(Plant_diary,pk=pk)

        if diary.author != request.user:
            return redirect('403_page')

        form = DiaryForm(instance=diary)
        context = {'form':form,'header':'Update diary'}
        return render(request,'main/forms.html',context)
    
    def post(self,request,pk):

        diary = get_object_or_404(Plant_diary,pk=pk)

        if diary.author != request.user:
            return redirect('403_page')
        
        form = DiaryForm(request.POST,instance=diary)
        if form.is_valid():
            
            sowing = form.cleaned_data['sowing'] 
            harvesting = form.cleaned_data['harvesting']

            if harvesting:
                if sowing >= harvesting:
                    messages.error(request,'Sowing date must before the harvesting date')
                    return redirect('update_diary',pk)

            diary = form.save(commit=True)
            messages.success(request,f'{diary.sowing} updated')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
                return redirect('update_diary',pk)
        return redirect('list_diaries')


class ProtectionScheduleList(LoginRequiredMixin,View):

    def get(self,request):

        cur_year = datetime.now().year     
        year = request.GET.get('select',cur_year)
       
        all_schedules = Schedule_Protection.objects.filter(author=self.request.user)
        schedules = all_schedules.filter(date__year=year).order_by('-date')
        years = set(all_schedules.values_list("date__year", flat=True))
        
        p = Paginator(schedules,8)
        page = self.request.GET.get('page')

        try:
            schedules = p.page(page)
        except PageNotAnInteger:
            schedules = p.page(1)
        except EmptyPage:
            schedules = p.page(p.num_pages)

        context = {'schedules':schedules,'years':years,'year':year}
        return render(request,'main/protection_schedules.html',context)
    

class DiaryList(LoginRequiredMixin,View):

    def get(self,request):

        cur_year = datetime.now().year     
        year = request.GET.get('select',cur_year)
       
        all_diaries = Plant_diary.objects.filter(author=self.request.user)
        diaries = all_diaries.filter(sowing__year=year).order_by('-sowing')
        years = set(all_diaries.values_list("sowing__year", flat=True))
      
        
        p = Paginator(diaries,8)
        page = self.request.GET.get('page')

        try:
            diaries = p.page(page)
        except PageNotAnInteger:
            diaries = p.page(1)
        except EmptyPage:
            diaries = p.page(p.num_pages)

        context = {'diaries':diaries,'years':years,'year':year}
        return render(request,'main/diaries.html',context)
    

class UpdateAboutPage(SuperUserRequiredMixin,View):

    def get(self,request):

        about_content = About_content.objects.all().first()
        form = AboutPageForm(instance=about_content)

        context = {'form':form,'header':'Update about page'}
        return render(request,'main/forms.html',context)
    
    def post(self,request):

        about_content = About_content.objects.all().first()
        form = AboutPageForm(request.POST,request.FILES,instance=about_content)
        if form.is_valid():

            icon1 = form.cleaned_data['icon1']
            icon2 = form.cleaned_data['icon2']

            x = re.search("^(fa-regular|fa-solid)+\s(fa)[-]+[a-z-]{0,100}$",icon1)
            y = re.search("^(fa-regular|fa-solid)+\s(fa)[-]+[a-z-]{0,100}$",icon2)

            if not x:
                messages.error(request,'Invalid format of icon1')
                return redirect('update_about')
            if not y:
                messages.error(request,'Invalid format of icon2')
                return redirect('update_about')
            
            form.save()
            messages.success(request,'About page updated')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
                return redirect('update_about')

        return redirect('about')



class AboutPage(View):

    def get(self,request):
        about_content = About_content.objects.all().first()
        context = {'about_content':about_content}
        return render(request,'main/about.html',context)
    

class SendContactMessage(View):

    def post(self,request):

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        valid_email = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
        valid_phone = re.match(r'^[\W0-9-]+$',phone)
        err=False

        if not valid_phone:
            messages.error(request,'not valid phone number')
            err = True

        if not valid_email:
            messages.error(request,'not valid email address')
            err = True

        if len(first_name) > 100:
            messages.error(request,'first name must be maximum 100 character long')
            err = True

        if len(last_name) > 100:
            messages.error(request,'last name must be maximum 100 character long')
            err = True

        if len(phone) > 20:
            messages.error(request,'last name must be maximum 20 character long')
            err = True
        
        if len(message) > 3000:
            messages.error(request,'your message must be max 3000 character long')
            err = True

        if err == True:
            return redirect('about')

        ContactMessage.objects.create(first_name=first_name,last_name=last_name,email=email,phone=phone,message=message)
        messages.success(request,'Your message sent to the staff, we will send answer soon')
        return redirect('about')

class Forbidden(TemplateView):
    template_name = 'main/403.html'



class Forum(View):

    def get(self,request):
        comments = ForumMessage.objects.all().order_by('-date')
        p = Paginator(comments,2)
        page = self.request.GET.get('page')

        try:
            comments = p.page(page)
        except PageNotAnInteger:
            comments = p.page(1)
        except EmptyPage:
            comments = p.page(p.num_pages)

        form = ForumForm()
        reply_form = ForumReplyForm()
        context = {'comments':comments,'form':form,'reply_form':reply_form}
        return render(request,'main/forum.html',context)
    
    @method_decorator(login_required)
    def post(self,request):

        form = ForumForm(data=request.POST)
        if form.is_valid():
            comments = form.save(commit=False)
            comments.author = request.user
            comments.save()
            messages.success(request,'Your post saved')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)            
        return redirect('forum')
       

class Reply(LoginRequiredMixin,View):

    def post(self,request,pk):

        message = get_object_or_404(ForumMessage,pk=pk)

        reply_form = ForumReplyForm(request.POST)
        if reply_form.is_valid():
            reply_comment = reply_form.save(commit=False)
            reply_comment.author = request.user
            reply_comment.message = message
            reply_comment.save()
            messages.success(request,'reply saved')
        else:
            for error in list(reply_form.errors.values()):
                messages.error(request,error)
        return redirect('forum')

        
class DeleteForumPost(LoginRequiredMixin,View):

    def post(self,request,pk):
        post = get_object_or_404(ForumMessage,pk=pk)
        if post.author != request.user:
            return redirect('forum')       
        else:
            post.delete()
            messages.success(request,'Your post deleted')
            return redirect('forum')



class UpdateForumPost(LoginRequiredMixin,View):

    def get(self,request,pk):
        post = get_object_or_404(ForumMessage,pk=pk)
        if post.author != request.user:
            return redirect('forum')
        else:
            form = ForumUpdateForm(instance=post)
            context = {'form':form,'header':'Update Post'}
            return render(request,'main/forms.html',context)
        
    def post(self,request,pk):
        post = get_object_or_404(ForumMessage,pk=pk)
        if post.author != request.user:
            return redirect('forum')
        else:
            form = ForumUpdateForm(request.POST,instance=post)
            if form.is_valid():
                form.save()
                messages.success(request,'Post updated')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
            return redirect('forum')



class DeleteForumReplyPost(LoginRequiredMixin,View):

    def post(self,request,pk):
        reply = get_object_or_404(ForumReplyMessage,pk=pk)
        if reply.author != request.user:
            return redirect('forum')       
        else:
            reply.delete()
            messages.success(request,'Your reply deleted')
            return redirect('forum')


class UpdateForumReply(LoginRequiredMixin,View):

    def get(self,request,pk):
        reply = get_object_or_404(ForumReplyMessage,pk=pk)
        if reply.author != request.user:
            return redirect('forum')
        else:
            form = ForumReplyUpdateForm(instance=reply)
            context = {'form':form,'header':'Update Reply'}
            return render(request,'main/forms.html',context)
        
    def post(self,request,pk):
        reply = get_object_or_404(ForumReplyMessage,pk=pk)
        if reply.author != request.user:
            return redirect('forum')
        else:
            form =ForumReplyUpdateForm(request.POST,instance=reply)
            if form.is_valid():
                form.save()
                messages.success(request,'Reply updated')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
            return redirect('forum')
        


class ListContactMessages(SuperUserRequiredMixin,ListView):

    model = ContactMessage
    template_name = 'main/contact_messages.html'
    context_object_name = 'contact_messages'
    ordering=['-date']
    paginate_by = 3




class ListUsers(SuperUserRequiredMixin,ListView):

    model = User
    template_name = 'main/users.html'
    context_object_name = "users"
    ordering=['-username']
    paginate_by = 8



class UserStatus(SuperUserRequiredMixin,View):

    def post(self,request,pk):
        user = get_object_or_404(User,pk=pk)
        if user.is_superuser:
           messages.error(request,'Admin user status unable to modify here')
           return redirect('users')
        
        if user.is_active:
            user.is_active = False
            messages.error(request,f'{user.username} disabled')
        else:
            user.is_active = True
            messages.success(request,f'{user.username} enabled')
        user.save()
        return redirect('users')
    

class CommentStatus(SuperUserRequiredMixin,View):

    def post(self,request,pk):
        comment = get_object_or_404(ForumMessage,pk=pk)

        if comment.enabled:
            comment.enabled = False
            messages.error(request,f'{comment} disabled')
        else:
            comment.enabled = True
            messages.success(request,f'{comment} enabled')
        comment.save()
        return redirect('forum')


class ReplyStatus(SuperUserRequiredMixin,View):

    def post(self,request,pk):
        reply = get_object_or_404(ForumReplyMessage,pk=pk)

        if reply.enabled:
            reply.enabled = False
            messages.error(request,f'{reply} disabled')
        else:
            reply.enabled = True
            messages.success(request,f'{reply} enabled')
        reply.save()
        return redirect('forum')