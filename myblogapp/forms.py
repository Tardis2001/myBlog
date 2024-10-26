from django import forms
from .models import Comment
from django_summernote.widgets import SummernoteWidget

class SearchForm(forms.Form):
    query = forms.CharField()

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    # email = forms.EmailField(required=False)
    # to = forms.EmailField(required=False)
    comments = forms.CharField(required=True, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    class Meta:
        model = Comment
        fields = ['name','email','body']
        widgets = {
            'body': SummernoteWidget()
        }