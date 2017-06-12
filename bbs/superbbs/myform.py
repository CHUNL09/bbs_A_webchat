from django import forms
from django.forms import ModelForm
from superbbs import models
from ckeditor.widgets import CKEditorWidget

class ArticleForm(ModelForm):
    class Meta:
        model=models.Article
        fields='__all__'
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'brief':forms.TextInput(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control'}),
            'content':forms.CharField(widget=CKEditorWidget()),
            'author':forms.Select(attrs={'class':'form-control'}),
            'pub_date':forms.DateTimeInput(attrs={'class':'form-control'}),  #'%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
            'last_modify_date':forms.DateTimeInput(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            'priority':forms.TextInput(attrs={'class':'form-control'}),

        }