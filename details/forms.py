from django import forms
from .models import ProjectDetail

class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = ProjectDetail
        fields = [
            'title',
            'description',
            'image',
            'content'
        ]