from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.shortcuts import redirect

class SuperUserRequiredMixin(LoginRequiredMixin,UserPassesTestMixin):
  
    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):

        return redirect('home')