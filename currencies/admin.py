from django.contrib import admin

from currencies.models import Currency, CurrencyPrice


class CurrencyPriceInline(admin.TabularInline):
    model = CurrencyPrice
    extra = 0
    fields = ("date", "price")
    readonly_fields = ("date", "price")
    ordering = ("-date",)
    verbose_name = "Price Record"
    verbose_name_plural = "Price History"


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "symbol", "current_price", "is_active")
    list_filter = ("is_active",)
    search_fields = ("id", "name")
    ordering = ("id",)
    inlines = [CurrencyPriceInline]


@admin.register(CurrencyPrice)
class CurrencyPriceAdmin(admin.ModelAdmin):
    list_display = ("currency", "date", "price")
    list_filter = ("currency",)
    search_fields = ("currency__id", "currency__name")
    date_hierarchy = "date"
    ordering = ("-date",)
