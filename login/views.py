from django.shortcuts import render, reverse
from django.views import View
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Beaver
from .forms import BeaverForm
from .auth_forms import UserLoginForm, UserSignupForm

# Create your views here.

User = get_user_model()

def index(request):
    return render(request, 'login/index.html')

class LoginView(View):
    template_name = "login/login.html"
    form_class = UserLoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("map:home"))
        return render(request, self.template_name)
    
    def post(self, request):
        userLoginForm = self.form_class(request.POST)
        if userLoginForm.login_user(request):
            return HttpResponseRedirect(reverse("map:home"))
        else:
            kwargs = {"form" : userLoginForm}
            return render(request, self.template_name, kwargs)

class RegisterView(View):
    template_name = "login/register.html"
    form_class = UserSignupForm
    form_class2 = BeaverForm

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("map:home"))
        return render(request, self.template_name)
    
    def post(self, request):
        userSignUpForm = self.form_class(request.POST)
        if(userSignUpForm.signUpUser(request)):
            print("works fine till here")
            userSignUpForm2 = self.form_class2(request.POST, request.FILES)
            if(userSignUpForm2.checkProfile(request)):
                return HttpResponseRedirect(reverse("map:home"))
            else:
                print("problem is here")
                kwargs = {"form" : userSignUpForm2}
                return render(request, self.template_name, kwargs)
        else:
            print("why doesn't this work")
            kwargs = {"form" : userSignUpForm}
            return render(request, self.template_name, kwargs)

class LogoutView(RedirectView):
    permanent = False
    pattern_name = "login:index"

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        message = ""
        messages.success(request, message, fail_silently=True)
        return super().dispatch(request, *args, **kwargs)
