from django.urls import path
from .import views
from .views import SearchResult


urlpatterns = [
    path('', views.home, name='home'),          ### path to home view (home page)
    path('search_result/', SearchResult.as_view(), name='search_result'),   ## path to search results view
    path('<int:pk>/details/', views.article_details, name='article_details'),    ### viewing the details of article at the home page
    path('tag/<slug>/',views.TagListView.as_view(), name='tagged'),
    path('details/<int:pk>/like/', (views.ArticleLikeToggle.as_view()), name='like_toggle'), #like path
    path('details/<int:pk>/dislike/', views.ArticleDislikeToggle.as_view(), name='dislike_toggle'),#dislike path
    path('articles/cst', views.cst, name='cst'),          ## viewing all articles from cst
    path('articles/cbe', views.cbe, name='cbe'),          ## viewing all articles from cbe
    path('articles/cmhs', views.cmhs, name='cmhs'),       ## viewing all articles from cmhs
    path('articles/ce', views.ce, name='ce'),             ## viewing all articles from ce
    path('articles/cass', views.cass, name='cass'),       ## viewing all articles from cass
    path('articles/cavm', views.cavm, name='cavm'),       ## viewing all articles from cavm
]