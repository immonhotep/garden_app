from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.contrib.auth.models import User
from .models import UserProfile,Plant,Pesticide,Disease,Schedule_Protection,Plant_diary,About_content,ForumMessage,ForumReplyMessage

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout,HTML
from crispy_forms.bootstrap import InlineCheckboxes

from bootstrap_datepicker_plus.widgets import DatePickerInput
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class SigInForm(AuthenticationForm):

    username = forms.CharField(max_length=250)
    password = forms.PasswordInput()
    captcha = ReCaptchaField(label="",widget=ReCaptchaV2Checkbox())

    
class Signupform(UserCreationForm):

    username = forms.CharField(max_length=250)
    email = forms.EmailField(max_length=100)
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    captcha = ReCaptchaField(label="",widget=ReCaptchaV2Checkbox())

    class Meta:
        model = User 
        fields = ('username','email','password1','password2')


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username','email','first_name','last_name')


class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('bio','image')



class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ('name','description','category','image','diseases')


    diseases = forms.ModelMultipleChoiceField(required=False,
        queryset=Disease.objects.all(),
        widget=forms.CheckboxSelectMultiple())

    def __init__(self, *args, **kwargs):
        super(PlantForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST' 
        self.helper.layout = Layout( 
            'name',
            'description',
            'category', 
            'image',       
            InlineCheckboxes('diseases',css_class='items-checkboxes mb-1'),
            Submit('submit', u'Submit', css_class='button-nice'),
            HTML('<a id="user-link" class="button-nice" href="javascript:history.back()">back</a>'),
            
    )
        

class DiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = ('name','description','pesticides','image')

    pesticides = forms.ModelMultipleChoiceField(required=False,
        queryset=Pesticide.objects.all(),
        widget=forms.CheckboxSelectMultiple())

    def __init__(self, *args, **kwargs):
        super(DiseaseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST' 
        self.helper.layout = Layout( 
            'name',
            'description', 
            'image',
            InlineCheckboxes('pesticides',css_class='items-checkboxes mb-1'),
            Submit('submit', u'Submit', css_class='button-nice'),
            HTML('<a class="button-nice" href="javascript:history.back()">back</a>'),
            
    )
        

class PesticideForm(forms.ModelForm):

    class Meta:
        model = Pesticide
        fields = ('name','description','category','link','image')


    def __init__(self, *args, **kwargs):
        super(PesticideForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST' 
        self.helper.layout = Layout( 
            'name',
            'description', 
            'category',
            'link',
            'image',
            Submit('submit', u'Submit', css_class='button-nice'),
            HTML('<a id="user-link" class="button-nice" href="javascript:history.back()">back</a>'),
            
    )



class ProtectionForm(forms.ModelForm):
    class Meta:
        model = Schedule_Protection
        fields = ('date','expire','note','plants','pesticide')


    date = forms.DateField(required=True,widget=DatePickerInput())
    expire = forms.DateField(required=True,widget=DatePickerInput())

    
    plants = forms.ModelMultipleChoiceField(required=True,
        queryset=Plant.objects.all(),
        widget=forms.CheckboxSelectMultiple())

    pesticide = forms.ModelMultipleChoiceField(required=True,
        queryset=Pesticide.objects.all(),
        widget=forms.CheckboxSelectMultiple())
    

    def __init__(self, *args, **kwargs):
        super(ProtectionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST' 
        self.helper.layout = Layout( 
            'date',
            'expire', 
            'note',
            InlineCheckboxes('plants',css_class='items-checkboxes mb-1'),
            InlineCheckboxes('pesticide',css_class='items-checkboxes mb-1'),
            Submit('submit', u'Submit', css_class='button-nice'),
            HTML('<a class="button-nice" href="javascript:history.back()">back</a>'),
            
    )
        


class DiaryForm(forms.ModelForm):
    class Meta:
        model = Plant_diary
        fields = ('sowing','harvesting','note','plants')


    sowing = forms.DateField(required=True,widget=DatePickerInput())
    harvesting = forms.DateField(required=False,widget=DatePickerInput())
  
    plants = forms.ModelMultipleChoiceField(required=True,
        queryset=Plant.objects.all(),
        widget=forms.CheckboxSelectMultiple())
    
    def __init__(self, *args, **kwargs):
        super(DiaryForm, self).__init__(*args, **kwargs)      
        self.helper = FormHelper()
        self.helper.form_method = 'POST' 
        self.helper.layout = Layout( 
            'sowing',
            'harvesting', 
            'note',
            InlineCheckboxes('plants',css_class='items-checkboxes mb-1'),
            Submit('submit', u'Submit', css_class='button-nice'),
            HTML('<a class="button-nice" href="javascript:history.back()">back</a>'),
            
    )
        

class AboutPageForm(forms.ModelForm):
    class Meta:
        model = About_content
        fields = ('title1','subtitle1','title2','subtitle2','title3','subtitle3','icon1','icon2','image')

    icon1 = forms.CharField(help_text="Example fontawesome formats: <b>(fa-solid fa-house) or (fa-regular fa-circle-user)</b>")
    icon2 = forms.CharField(help_text="Example fontawesome formats: <b>(fa-solid fa-house) or (fa-regular fa-circle-user)</b>")


    def __init__(self, *args, **kwargs):
        super(AboutPageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST' 
        self.helper.layout = Layout( 
            'title1',
            'subtitle1',
            'title2', 
            'subtitle2', 
            'title3',
            'subtitle3',
            'icon1',
            'icon2',
            'image',    
            Submit('submit', u'Submit', css_class='button-nice'),
            HTML('<a id="user-link" class="button-nice" href="javascript:history.back()">back</a>'),
            
    )
        


class ChangePasswordForm(PasswordChangeForm):

    def __init__(self, user, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(user,*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST' 
        self.helper.layout = Layout( 
            'old_password',
            'new_password1',
            'new_password2',    
            Submit('submit', u'Submit', css_class='button-nice'),
            HTML('<a id="user-link" class="button-nice" href="javascript:history.back()">back</a>'),
            
    )
        

class ForumForm(forms.ModelForm):

    class Meta:
        model = ForumMessage
        fields = ('post',)


class ForumReplyForm(forms.ModelForm):

    class Meta:
        model = ForumReplyMessage
        fields = ('reply',)


class ForumUpdateForm(forms.ModelForm):

    class Meta:
        model = ForumMessage
        fields = ('post',)

    def __init__(self, *args, **kwargs):
        super(ForumUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST' 
        self.helper.layout = Layout( 
            'post',
            Submit('submit', u'Submit', css_class='button-nice'),
            HTML('<a id="user-link" class="button-nice" href="javascript:history.back()">back</a>'),
            
    )
        

class ForumReplyUpdateForm(forms.ModelForm):

    class Meta:
        model = ForumReplyMessage
        fields = ('reply',)

    def __init__(self, *args, **kwargs):
        super(ForumReplyUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST' 
        self.helper.layout = Layout( 
            'reply',
            Submit('submit', u'Submit', css_class='button-nice'),
            HTML('<a id="user-link" class="button-nice" href="javascript:history.back()">back</a>'),
            
    )


