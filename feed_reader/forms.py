from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Feed

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = '<small class="text-muted">Enter a unique username. Letters, digits, and @/./+/-/_ are allowed.</small>'
        self.fields['password1'].help_text = '<small class="text-muted">Your password must be at least 8 characters long and not entirely numeric.</small>'
        self.fields['password2'].help_text = '<small class="text-muted">Re-enter your password for verification.</small>'

class FeedAddForm(forms.ModelForm):
    class Meta:
        model = Feed
        fields = ['url']
