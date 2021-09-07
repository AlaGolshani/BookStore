from django.contrib import admin
from .models import *


class BookInline(admin.TabularInline):
    model = Book.categories.through
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'quantity', 'author']
    list_display_links = ['title']
    list_editable = ['author', 'price', 'quantity']
    search_fields = ['title', 'author']
    readonly_fields = ['slug', 'creator']
    fieldsets = (
        ('اطلاعات عمومی', {
            'fields': (('title', 'author'), ('price', 'quantity'), 'categories')
        }),
        ('جزئیات', {
            'classes': ('collapse',),
            'fields': ('image', 'summary', 'cash_discount',
                       'percentage_discount', 'creator')
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_editable = ['name']
    inlines = [BookInline]
    readonly_fields = ['creator']
