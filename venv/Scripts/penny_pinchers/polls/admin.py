from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Define the fields to be used in displaying the CustomUser model.
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'birth_year')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Add fields to be displayed in the admin list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'birth_year', 'is_staff')

    # Add filters to the admin list view
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    # Add search functionality in the admin list view
    search_fields = ('username', 'first_name', 'last_name', 'email')

    # Define the ordering of the admin list view
    ordering = ('username',)

# Register the custom user model and admin class with the admin site
admin.site.register(CustomUser, CustomUserAdmin)


# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser
# from .models import Choice


# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 3


# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None, {"fields": ["question_text"]}),
#         ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
#     ]
#     inlines = [ChoiceInline]
#     list_display = ["question_text", "pub_date"]
#     list_display = ["question_text", "pub_date", "was_published_recently"]
#     list_filter = ["pub_date"]
#     search_fields = ["question_text"]


# #admin.site.register(Question, QuestionAdmin)
# admin.site.register(CustomUser, UserAdmin)