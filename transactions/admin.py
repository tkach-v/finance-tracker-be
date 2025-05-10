from django.contrib import admin

from transactions.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "amount",
        "description",
        "created_at",
    )
    list_filter = ("user",)
    search_fields = ("description",)
