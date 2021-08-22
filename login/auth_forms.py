from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login, get_user_model
from django import forms
from django.contrib.auth.hashers import check_password

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=100)

    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            print(super().errors)
            return valid
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = User.objects.filter(username=username)
        if not user.exists():
            self._errors = "User does not exist"
            return False
        if not user[0].check_password(password):
            self._errors = "Wrong username and password combination"
            return False
        return True
    
    def login_user(self, request):
        if self.is_valid():
            username = self.cleaned_data.get("username")
            password = self.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            return True
        return False

class UserSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password", "email"]
    
    def is_valid(self):
        valid = super().is_valid()
        username = self.cleaned_data.get("username")
        print(username)
        password = self.cleaned_data.get("password")
        address = self.cleaned_data.get("address")
        print(address)

        if not valid:
            print(super().errors)
            return False
        try:
            validate_password(password)
        except Exception as error:
            self.add_error("password", list(error)[0])
            return False
        return True

    def signUpUser(self, request, commit=True):
        if self.is_valid():
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password"])
            if commit:
                user.save()
            login(request, user)
            return True
        print("this is why")
        return False