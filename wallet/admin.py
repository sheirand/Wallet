from django.contrib import admin
from wallet.models import Organization, Transaction


class CustomTransactionAdmin(admin.ModelAdmin):

    list_display = ("id", "user", "time", "amount", "income")
    ordering = ("id", "time", "amount")
    list_filter = ("time", "category", "income")
    search_fields = ("id", "user", "time", "category")
    filter_horizontal = ()


admin.site.register(Organization)
admin.site.register(Transaction, CustomTransactionAdmin)
