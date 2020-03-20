from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django_userforeignkey.models.fields import UserForeignKey
from django.utils.html import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager


#####################  creating college model   ######################

class College(models.Model):
    name        = models.CharField(max_length=6, unique=True)
    description = models.CharField(max_length=800, unique=True)

    def __str__(self):
        return self.name

#####################  creating article model   ######################

class Article( models.Model):
    subject    = models.CharField(max_length=30, unique=True)
    message    = RichTextUploadingField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField( auto_now=True, null=True)
    author     = UserForeignKey(auto_user_add=True, on_delete=models.CASCADE)
    college    = models.ForeignKey(College, on_delete=models.CASCADE)
    picture    = models.ImageField(upload_to='article_images',null=True, default="")
    likes      = models.ManyToManyField(User, related_name='article_likes', blank=True)
    dislikes      = models.ManyToManyField(User, related_name='article_dislikes', blank=True)# likes field
    tags       = TaggableManager()


    def snippet(self):
        return self.message[:30]+ '........'
    
    def __str__(self):
        return self.subject

#   def highrated(request):
   
    def get_absolute_url(self):
        return reverse('article_details', kwargs={'pk': self.pk})
    
    
    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))

    
    def get_like_url(self):
        return reverse('like_toggle', kwargs={'pk': self.pk})

    def get_dislike_url(self):
        return reverse('dislike_toggle', kwargs={'pk': self.pk})

#####################  creating comment model   ######################


class Comment(models.Model):
    article     = models.ForeignKey(Article, on_delete=models.CASCADE)
    user        = UserForeignKey(auto_user_add=True, on_delete=models.CASCADE)
    reply       = models.ForeignKey('Comment', null=True, related_name='replies', on_delete=models.CASCADE)
    content     = models.TextField(max_length = 160, default="")
    timestamp   = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return '{}-{}'.format(self.article.subject, str(self.user.username))


  

class Subscriber(models.Model):
    email               = models.EmailField(blank=False, null=False)
    article_category    = models.ForeignKey(College, on_delete = models.CASCADE)
    subscription_date   = models.DateTimeField(auto_now_add = True)


    def __str__(self):
        return self.email
    
    