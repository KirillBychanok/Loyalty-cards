from django.contrib import admin
from .models import Card, Orders, Goods

@admin.register(Card)
class AdminCard(admin.ModelAdmin):
    list_display = ('series_card', 'number_card', 'date_end_active_card', 'sum_purchase', 'status_card', 'card_discount')
    list_display_links = ('status_card', )


@admin.register(Orders)
class AdminOrders(admin.ModelAdmin):
    list_display = ('id', 'date_time_order', 'final_cost_order')


@admin.register(Goods)
class AdminGoods(admin.ModelAdmin):
    list_display = ('name_goods', 'cost_goods', 'discount_cost')
    list_display_links = ('name_goods',)

