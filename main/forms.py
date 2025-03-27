from django import forms
from .models import Users,Story

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['full_name', 'gender', 'mobile']


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'content']
