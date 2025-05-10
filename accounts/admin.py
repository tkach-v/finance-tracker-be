from django.contrib import admin

from accounts.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "name",
    )
    list_filter = ("name",)
    search_fields = ("name",)
