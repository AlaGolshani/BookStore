from django.contrib import admin
from .models import *


@admin.register(CashDiscount)
class CashDiscountAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'started', 'expired']
    fields = ['amount', ('started', 'expired'), 'creator']
    list_display_links = ['id']
    list_editable = ['amount', 'started', 'expired']
    date_hierarchy = 'expired'
    sortable_by = ['expired', 'started', 'amount']
    readonly_fields = ['creator']


@admin.register(PercentageDiscount)
class PercentageDiscountAdmin(admin.ModelAdmin):
    list_display = ['id', 'percentage', 'max_amount', 'started', 'expired']
    fields = [('percentage', 'max_amount'), ('started', 'expired'), 'creator']
    list_display_links = ['id']
    list_editable = ['percentage', 'max_amount', 'started', 'expired']
    date_hierarchy = 'expired'
    sortable_by = ['expired', 'started', 'percentage']
    readonly_fields = ['creator']



@admin.register(CodeDiscount)
class CodeDiscountAdmin(admin.ModelAdmin):
    list_display = ['code', 'percentage', 'max_amount', 'started', 'expired']
    fields = ['code', ('percentage', 'max_amount'), ('started', 'expired'), 'creator']
    list_display_links = ['code']
    list_editable = ['percentage', 'max_amount', 'started', 'expired']
    date_hierarchy = 'expired'
    sortable_by = ['expired', 'started', 'percentage']
    readonly_fields = ['creator']
