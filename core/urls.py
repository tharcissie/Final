from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('view/<int:pk>/', views.article_detail, name='article_detail'),
    path('new/', views.article_create, name='article_new'),
    path('edit/<int:pk>', views.article_update, name='article_edit'),
    path('delete/<int:pk>', views.article_delete, name='article_delete'),
    path('view/<int:pk>/like/', views.ArticleLikeToggle.as_view(), name='like_toggle'), #like path
    path('view/<int:pk>/dislike/', views.ArticleDislikeToggle.as_view(), name='dislike_toggle'),#dislike path
 ]
 
