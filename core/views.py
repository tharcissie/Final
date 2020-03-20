from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, RedirectView
from django.utils.decorators import method_decorator
from .models import Article, Comment, College
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.forms import ModelForm
from django.utils import timezone
from .forms import *
from django.core.paginator import Paginator
from django.core.mail import send_mail
from rootFolder.settings import EMAIL_HOST_USER
   

class ArticleView(DetailView):
    model = Article

class ArticleCreate(CreateView):
    model = Article
    fields = ['subject', 'message', 'picture' , 'tags']
    success_url = reverse_lazy('article_list')



class ArticleDelete(DeleteView):
    model = Article
    success_url = reverse_lazy('article_list')


def article_list(request, template_name='core/article_list.html'):
    article = Article.objects.all()
    paginator = Paginator(article, 6) # < 3 is the number of items on each page
    page = request.GET.get('page') # < Get the page number
    article = paginator.get_page(page) # < New in 2.0!
    data = {}
    data['object_list'] = article
    return render(request, template_name, data)




def article_detail(request, pk, template_name='core/article_detail.html'):
    article = get_object_or_404(Article, pk=pk)
    # article = Article.objects.get(pk=pk)
    comments = Comment.objects.filter(article=article , reply=None).order_by('-id')

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
             return redirect('article_list')
    comment_form = CommentForm()
    context = { 'object':article, 'comments':comments, 'comment_form':comment_form}  
    return render(request, template_name, context)

################################## section of like view  ##################################
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
        return  url_


##############################################  section of dislike view  ###############################
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


def subscriber():
    subscribers_list = []

    subscribers = Subscriber.objects.all()

    for subscriber in subscribers:
        subscribers_list.append(subscriber.email)

    return subscribers_list


@login_required
def article_create(request, template_name='core/article_form.html'):
    form = ArticleForm(request.POST or None ,files=request.FILES)
    if form.is_valid():
        form.save()

        subject = "Hello Subscriber"
        message = 'A new article from your choice has been created, be the first to read it and share your feedback'
        send_mail(subject, message, EMAIL_HOST_USER,subscriber())

        return redirect('article_list')
    return render(request, template_name, {'form':form})

@login_required
def article_update(request, pk, template_name='core/article_form.html'):
    # article= get_object_or_404(Article, pk=pk)
    article1 = Article.objects.get(pk=pk)
    form1 = ArticleForm(request.POST or None, instance=article1)
    if form1.is_valid():
        form1.save()
        return redirect('article_list')
    return render(request, template_name, {'form':form1})

@login_required
def article_delete(request, pk, template_name='core/article_confirm_delete.html'):
    article= get_object_or_404(Article, pk=pk)    
    if request.method=='POST':
        article.delete()
        return redirect('article_list')
    return render(request, template_name, {'object':article})
