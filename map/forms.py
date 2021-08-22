from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = []
    
    def addevent(self, request):
        
        if self.is_valid:
            event = self.save(commit=False)
            event.save()
            return True
        else:
            return False
