from django.contrib import admin

from categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "name",
        "type",
        "budget_limit",
    )
    list_filter = ("type",)
    search_fields = ("name",)
