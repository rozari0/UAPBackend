from django.contrib import admin

from .models import AuthToken, Resume, User, UserProfile

# Register your models here.

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Resume)
admin.site.register(AuthToken)
