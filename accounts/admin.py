from django.contrib import admin
from .models import Profile


#####################     registering profile model in admin dashboard      ######################

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image',)
admin.site.register(Profile, ProfileAdmin)
