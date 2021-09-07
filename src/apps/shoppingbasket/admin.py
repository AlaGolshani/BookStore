from django.contrib import admin
from .models import *


class OrderInline(admin.TabularInline):
    model = Order
    extra = 0


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


def make_delivered(modeladmin, request, queryset):
    rows_updated = queryset.update(status='D')
    if rows_updated == 1:
        message_bit = 'تحویل داده شد'
    else:
        message_bit = 'تحویل داده شدند'
    modeladmin.message_user(request, f'{rows_updated} سفارش {message_bit}.')


make_delivered.short_description = "تحویل سفارشات انتخاب شده"


@admin.register(ShoppingBasket)
class ShoppingBasketAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_username']
    inlines = [OrderInline]

    def get_username(self, obj):
        try:
            customer = obj.customer.username
        except:
            customer = 'guest'
        return customer

    get_username.admin_order_field = 'customer'  # Allows column order sorting
    get_username.short_description = 'Customer Username'  # Renames column head


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_username', 'status']
    list_display_links = ['id']
    list_editable = ['status']
    list_filter = ['status']
    search_fields = ['status', 'discount_code']
    inlines = [OrderItemInline]
    actions = [make_delivered]
    date_hierarchy = 'ordered'

    def get_username(self, obj):
        try:
            customer = obj.shopping_basket.customer.username
        except:
            customer = 'guest'
        return customer

    get_username.admin_order_field = 'customer'  # Allows column order sorting
    get_username.short_description = 'نام کاربری مشتری'  # Renames column head


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_username', 'book', 'item_count']
    list_editable = ['item_count']
    list_display_links = ['id']

    def get_username(self, obj):
        try:
            customer = obj.order.shopping_basket.customer.username
        except:
            customer = 'guest'
        return customer

    get_username.admin_order_field = 'customer'  # Allows column order sorting
    get_username.short_description = 'Customer Username'  # Renames column head
