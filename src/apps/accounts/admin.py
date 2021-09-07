from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .forms import AddressCreationForm, AddressChangeForm
from ..discount.models import (CashDiscount,
                               PercentageDiscount,
                               CodeDiscount)
from .models import Customer, Staff, Admin, Address
from ..product.models import Book, Category
from ..shoppingbasket.models import ShoppingBasket


class BasketInline(admin.TabularInline):
    model = ShoppingBasket
    extra = 0


class AddressInline(admin.StackedInline):
    model = Address
    extra = 0


@admin.register(Customer)
class CustomerProxyAdmin(admin.ModelAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ['id', 'username', 'email', 'phone_number', 'device']
    list_display_links = ['id']
    list_editable = ['phone_number', 'email']
    search_fields = ['username', 'email']
    readonly_fields = ['device']
    inlines = [BasketInline, AddressInline]

    def get_queryset(self, request):
        return Customer.objects.filter(is_staff=False)


class CashDiscountInline(admin.TabularInline):
    model = CashDiscount
    extra = 0


class PercentageDiscountInline(admin.TabularInline):
    model = PercentageDiscount
    extra = 0


class CodeDiscountInline(admin.StackedInline):
    model = CodeDiscount
    extra = 0


class BookInline(admin.StackedInline):
    model = Book
    extra = 0


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0


@admin.register(Staff)
class StaffProxyAdmin(admin.ModelAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ['id', 'username', 'email', 'phone_number']
    list_display_links = ['username']
    list_editable = ['phone_number', 'email']
    search_fields = ['username', 'email']
    inlines = [CashDiscountInline, PercentageDiscountInline,
               CodeDiscountInline, BookInline, CategoryInline]

    def get_queryset(self, request):
        return Staff.objects.filter(is_staff=True, is_superuser=False)


@admin.register(Admin)
class AdminProxyAdmin(admin.ModelAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ['id', 'username', 'email', 'phone_number']
    list_display_links = ['username']
    list_editable = ['phone_number', 'email']
    search_fields = ['username', 'email']
    inlines = [CashDiscountInline, PercentageDiscountInline,
               CodeDiscountInline, BookInline, CategoryInline]

    def get_queryset(self, request):
        return Admin.objects.filter(is_superuser=True)


class AddressAdmin(admin.ModelAdmin):
    add_form = AddressCreationForm
    form = AddressChangeForm
    list_display = ['id', 'city', 'zip_code']
    list_editable = ['zip_code']
    list_filter = ['state']
    search_fields = ['country', 'state', 'city']
