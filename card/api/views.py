from card.models import Card, Goods, Orders, Basket
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from .filters import CardFilter
from .serializers import CardDetailSerializer, CardListSerializer, OrdersDetailSerializer, GoodsDetailSerializer, CardDetailNewSerializer, OrderListNewSerializer
from rest_framework.decorators import api_view
from django.forms import model_to_dict
import random


# Cписок карт с полями: серия, номер, дата выпуска, дата окончания активности, статус, фильтрация и поиск по этим же полям
class CardAllStatView(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CardFilter
    search_fields = ['series_card', 'number_card','date_start_card', 'date_end_active_card', 'status_card']


# Aктивация/деактивация карты
class CardActiveView(generics.UpdateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardDetailSerializer


# Просмотр профиля карты с историей покупок по ней
@api_view(['GET'])
def api_orders_detail(request, pk):
    if request.method == 'GET':
        try:
            card = Card.objects.get(pk=pk)
            all_order = card.cards.all()
            serializer = OrdersDetailSerializer(all_order, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            result = 'Card with this number does not exist'
            return Response({'result': result}, status=status.HTTP_404_NOT_FOUND)
    

# Удаление карты (сперва в корзину с возможностью восстановления)
@api_view(['POST'])
def api_delete_card(request, pk):
    if request.method == 'POST':
        try:
            card = Card.objects.get(pk=pk)
            new_basket = Basket.objects.create(
                series_card = card['series_card'],
                number_card = card['number_card'],
                date_start_card = card['date_start_card'],
                date_end_active_card = card['date_end_active_card'],
                date_last_use_card = card['date_last_use_card'],
                sum_purchase = card['sum_purchase'],
                status_card = card['status_card'],
                card_discount = card['card_discount']
            )
            card.delete()
            return Response({'post': model_to_dict(new_basket)})
        except Exception as ex:
            result = 'Card with this number does not exist'
            return Response({'result': result}, status=status.HTTP_404_NOT_FOUND)


# Восстановление карты из корзины
@api_view(['POST'])
def api_repair_card(request, pk):
    if request.method == 'POST':
        try:
            basket = Basket.objects.get(pk=pk)
            new_card = Card.objects.create(
                series_card = basket['series_card'],
                number_card = basket['number_card'],
                date_start_card = basket['date_start_card'],
                date_end_active_card = basket['date_end_active_card'],
                date_last_use_card = basket['date_last_use_card'],
                sum_purchase = basket['sum_purchase'],
                status_card = basket['status_card'],
                card_discount = basket['card_discount']
            )
            basket.delete()
            return Response({'post': model_to_dict(new_card)})
        except Exception as ex:
            result = 'Card with this number does not exist'
            return Response({'result': result}, status=status.HTTP_404_NOT_FOUND)


# Генератор карт, с указанием серии и количества генерируемых карт, а срока активности «с-по»
@api_view(['POST'])
def api_generate_card(request):
    if request.method == 'POST':
        string_for_data = '1234567890'
        list_for_data = list(string_for_data)
        for new_card in range(request.data['count']):
            new_card = Card.objects.create(
                series_card = request.data['series_card'],
                number_card = ''.join([random.choice(list_for_data) for x in range(10)]),
                date_start_card = request.data['date_start_card'],
                date_end_active_card = request.data['date_end_active_card'],
                date_last_use_card = request.data['date_start_card'],
                sum_purchase = 0,
                status_card = 'A',
                card_discount = 0
                )
        result = 'Cards create'
        return Response({'result': result}, status=status.HTTP_201_CREATED)


#Добавление новых товаров
class AddNewGoodsView(generics.ListCreateAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodsDetailSerializer


#Добавление новых дисконтных карт
class AddNewCardsView(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardDetailNewSerializer


#Добавление новых заказов
class AddNewOrdersView(generics.ListCreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderListNewSerializer
