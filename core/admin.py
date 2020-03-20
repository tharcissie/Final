from django.contrib import admin
from .models import Article, College,  Comment, Subscriber



#####################     registering college model on admin dashboard    ######################


class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name','description',)
    search_fields = ('name','description',)

admin.site.register(College, CollegeAdmin)

#####################     registering comment model on admin dashboard    ######################

class CommentAdmin(admin.ModelAdmin):
    list_display = ('article','user','reply','content','timestamp',)

admin.site.register(Comment, CommentAdmin)

#####################     registering college model on admin dashboard    ######################

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('subject','message','created_at','updated_at','author','college', 'tag_list')
    

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
    
admin.site.register(Article, ArticleAdmin)





#####################     registering subscriber model on admin dashboard    ######################

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email','subscription_date')

admin.site.register(Subscriber, SubscriberAdmin)