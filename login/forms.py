from django import forms
from django.contrib.auth import get_user_model
from .models import Beaver

class BeaverForm(forms.ModelForm):
    class Meta:
        model = Beaver
        exclude = ["user"]

    def checkProfile(self, request):
        print(request.user)
        if self.is_valid():
            beaver = self.save(commit=False)
            beaver.user = request.user
            beaver.save()
            return True
        print(self.errors)
        print("exact reason")
        return False