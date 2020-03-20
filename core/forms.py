from django import forms
from .models import Comment, Article, Subscriber
from django.contrib.auth.models import User


#####################  form for creating article   ######################

class ArticleForm(forms.ModelForm):
    class Meta:
        model   = Article
        fields  = ['subject', 'message','college', 'picture', 'tags']

#####################  form for creating comment   ######################

class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Comments goes here','rows':'5', 'cols':'250'}))
    class Meta:
        model   = Comment
        fields  = ('content',)


class SubscriberForm(forms.ModelForm):
    class Meta:
        model   = Subscriber
        fields  = ('email','article_category',)