from django import forms
from core_app.models import *

class NewBlogForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}), required=True)
    image = forms.FileField(required=True)
    summary = forms.CharField(required=True)
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": 10, "cols": 22}), required=True)
    
    class Meta:
        model = BlogModel
        fields = ('title', 'image', 'summary', 'content', 'isdraft', )
        
    