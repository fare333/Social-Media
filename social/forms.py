from django import forms

from .models import *

class PostForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Say Something...'
            }))
    
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'multiple': True
            })
    )
    
    class Meta:
        model = Post
        fields = ("body",)
    
class ShareForm(forms.Form):
    body = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '1',
            'placeholder': 'Say Something...',
            }))
    
class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Say Something...'
            }))
    class Meta:
        model = Comment
        fields = ("comment",)
        
class ThreadForm(forms.Form):
    username = forms.CharField(label='',max_length=1000)
    
class MessageForm(forms.ModelForm):
    body = forms.CharField(label='', max_length=1000)
    image = forms.ImageField(required=False)
    class Meta:
        model = MessageModel
        fields = ['body', 'image']