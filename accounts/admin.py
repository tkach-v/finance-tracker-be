from django.contrib import admin

from accounts.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "name",
        "balance",
        "currency",
    )
    list_filter = ("name", "user", "currency")
    search_fields = ("name",)
