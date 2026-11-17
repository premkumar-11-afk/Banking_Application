from django.contrib import admin
from .models import Account, Transaction

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("account_number", "user", "balance", "created_at")
    search_fields = ("account_number", "user__username")

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("reference", "from_account", "to_account", "amount", "created_at")
    search_fields = ("reference",)
