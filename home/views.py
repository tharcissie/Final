from core.forms import *
from django.db.models import Q
from django.forms import ModelForm
from django.urls import reverse_lazy
from core.models import Article, Comment, College, Subscriber
from core.forms import SubscriberForm
from django.views.generic import ListView, DetailView, RedirectView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from taggit.models import Tag
from django.core.paginator import Paginator
from django.core.mail import send_mail
from rootFolder.settings import EMAIL_HOST_USER





class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tags']=Tag.objects.all()
        return context
    
 
class TagListView(TagMixin,ListView):
    model = Article
    template_name = "home/tag.html"
    def get_queryset(self):
        return Article.objects.filter(tags__slug=self.kwargs.get('slug'))

    


class ArticleView(DetailView):
    model = Article

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['subject', 'message']

#################     function of rendering the homepage     ###################

def home(request):
    article = Article.objects.all().order_by('-id')
    paginator = Paginator(article, 6) # < 3 is the number of items on each page
    page = request.GET.get('page') # < Get the page number
    article = paginator.get_page(page) # < New in 2.0!

  
    subscriber_form = SubscriberForm(request.POST or None)
    if subscriber_form.is_valid():
        subscriber_form.save()
        
        subject = "Hello New Subscriber"
        message = 'Thank you for subscribing to our UR Blog !!!'
        send_mail(subject, message, EMAIL_HOST_USER,['byives21@gmail.com']
        
        )
    else:
        subscriber_form = SubscriberForm()
    return render(request, 'home/home.html',{'article':article,'form':subscriber_form})


#################     function of article details and comment stuff     ###################

def article_details(request, pk, template_name='home/article_details.html'):
    article = get_object_or_404(Article, pk=pk)
    # article = Article.objects.get(pk=pk)
    comments = Comment.objects.filter(article=article , reply=None).order_by('id')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
             content = request.POST.get('content')
             reply_id = request.POST.get('comment_id')
             comment_qs = None
             if reply_id:
                 comment_qs = Comment.objects.get(id=reply_id)
             comment = Comment.objects.create(article=article, user=request.user, content=content, reply=comment_qs)
             comment.save() 
             return redirect('home')
    comment_form = CommentForm()
    context = { 'object':article, 'comments':comments, 'comment_form':comment_form }  
    return render(request, template_name, context)

#####################     dealing with search features       ######################

class SearchResult(ListView):
    model = Article
    template_name = 'home/search.html'

    def get_queryset(self):
        search = self.request.GET.get('query')
       
        object_list = Article.objects.filter(

            Q(subject__icontains=search) | Q(message__icontains=search)
        )
        return object_list

class ArticleLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        print(pk)
        obj = get_object_or_404(Article, pk=pk)
        url_= obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_



class ArticleDislikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        print(pk)
        ob = get_object_or_404(Article, pk=pk)
        urll_= ob.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in ob.dislikes.all():
                ob.dislikes.remove(user)
            else:
                ob.dislikes.add(user)
        return urll_


def cst(request):
    articles_cst = Article.objects.filter(college__name='CST').order_by('-id')
    return render(request,'home/cst.html',{'articles_cst':articles_cst})

def cbe(request):
    articles_cbe = Article.objects.filter(college__name='CBE').order_by('-id')
    return render(request,'home/cbe.html',{'articles_cbe':articles_cbe})

def cmhs(request):
    articles_cmhs = Article.objects.filter(college__name='CMHS').order_by('-id')
    return render(request,'home/cmhs.html',{'articles_cmhs':articles_cmhs})

def ce(request):
    articles_ce = Article.objects.filter(college__name='CE').order_by('-id')
    return render(request,'home/ce.html',{'articles_ce':articles_ce})

def cass(request):
    articles_cass = Article.objects.filter(college__name='CASS').order_by('-id')
    return render(request,'home/cass.html',{'articles_cass':articles_cass})

def cavm(request):
    articles_cavm = Article.objects.filter(college__name='CAVM').order_by('-id')
    return render(request,'home/cavm.html',{'articles_cavm':articles_cavm})





    