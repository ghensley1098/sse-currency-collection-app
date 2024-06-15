from django.contrib import admin

from .models import mCollection, mEntry

class ChoiceInLine(admin.StackedInline):
    model = mEntry
    extra = 1

class CollectionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ['cName']}),
        ('Date Information', {'fields': ['cDate'], "classes": ['collapse']})
    ]
    inlines = [ChoiceInLine]

admin.site.register(mCollection, CollectionAdmin)
