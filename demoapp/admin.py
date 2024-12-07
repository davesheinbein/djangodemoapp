# Register your models here to make them available in the Django admin interface
# This file is used to register models with the Django admin site.
# By registering models, they become manageable through the admin interface.

from django.contrib import admin
from .models import HomePage, AboutPage, ContactPage, Visitor, Profile, Category, Tag, Article, Author, Book

class HomePageAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')  # Display these fields in the list view
    search_fields = ('title', 'content')  # Enable search on these fields
    list_filter = ('title',)  # Add filter options for the title field
    ordering = ('title',)  # Order by title
    list_per_page = 20  # Paginate the list view

class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')
    search_fields = ('title', 'content')
    list_filter = ('title',)
    ordering = ('title',)
    list_per_page = 20

class ContactPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')
    search_fields = ('title', 'content')
    list_filter = ('title',)
    ordering = ('title',)
    list_per_page = 20

class VisitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'favorite_thing_to_cook')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('favorite_thing_to_cook',)
    ordering = ('name',)  # Order by name
    list_per_page = 20
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'phone')
        }),
        ('Additional Information', {
            'fields': ('favorite_thing_to_cook', 'additional_comments')
        }),
    )
    readonly_fields = ('email',)  # Make email field read-only

admin.site.register(HomePage, HomePageAdmin)
admin.site.register(AboutPage, AboutPageAdmin)
admin.site.register(ContactPage, ContactPageAdmin)
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(Author)
admin.site.register(Book)