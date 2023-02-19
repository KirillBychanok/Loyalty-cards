from django.urls import path
from card.api.views import CardAllStatView, CardActiveView, api_orders_detail, api_delete_card, api_repair_card, AddNewCardsView, AddNewGoodsView, AddNewOrdersView


urlpatterns = [
    path('card_list/', CardAllStatView.as_view({'get': 'list'}), name='all_card'),
    path('card_detail/<int:pk>/', CardActiveView.as_view(), name='detail_card'), 
    path('card_history/<int:pk>/', api_orders_detail, name='history_card'),
    path('card_delete/<int:pk>/', api_delete_card, name='delete_card'), 
    path('card_repair/<int:pk>/', api_repair_card, name='repair_card'),
    path('add_new_card/', AddNewCardsView.as_view(), name='add_card'),
    path('add_new_goods/', AddNewGoodsView.as_view(), name='add_goods'),
    path('add_new_orders/', AddNewOrdersView.as_view(), name='add_orders'), 
]