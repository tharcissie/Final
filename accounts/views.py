from .forms import *
from core.models import Article
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator






#####################     function for rendering signup form on page    ######################

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

#####################     function for rendering the dashboard page   ######################

@login_required
def dashboard(request):
    article = Article.objects.filter(author=request.user)
    paginator = Paginator(article, 6) # < 3 is the number of items on each page
    page = request.GET.get('page') # < Get the page number
    article = paginator.get_page(page) # < New in 2.0!
    data = {}
    data['object_list'] = article
    return render(request, 'accounts/dashboard.html',data)

#####################     function for updating user profile inforamtion and profile picture     ######################

@login_required
def update_profile(request):

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid():
            u_form.save()
            p_form.save()
      
            return redirect('update_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'accounts/update_profile.html',{'u_form':u_form, 'p_form':p_form})

