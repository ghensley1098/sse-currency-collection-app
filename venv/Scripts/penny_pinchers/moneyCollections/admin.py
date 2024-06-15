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
    list_display = ['cName','cDate','was_published_recently']
    list_filter = ['cDate']
    search_fields = ['cName']

admin.site.register(mCollection, CollectionAdmin)
