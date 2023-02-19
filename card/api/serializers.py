from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from card.models import Card, Orders, Goods


class CardListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ('id', 'series_card', 'number_card','date_start_card', 'date_end_active_card', 'date_last_use_card','status_card')

    def validate(self, instance, data):
            if data['date_end_active_card'] < data['date_last_use_card']:
                self.update(self, instance, data)
            return data
    
    def update(self, instance, validated_data):
        instance.status_card = 'O'
        instance.save()
        return instance


class CardDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Card
        fields = ('id', 'series_card', 'number_card','date_start_card', 'date_end_active_card', 'status_card')
        extra_kwargs = {
            'status_card': {'write_only': True},
        }
        read_only_fields = ['id', 'series_card', 'number_card','date_start_card', 'date_end_active_card']

        
class OrdersDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields = ('date_time_order', 'sum_order', 'discount_order','final_cost_order')


class GoodsDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = '__all__'


class CardDetailNewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ('series_card', 'number_card','card_discount','status_card', 'sum_purchase')


class OrderListNewSerializer(serializers.ModelSerializer):
    sum_order = serializers.SerializerMethodField()
    discount_order = serializers.SerializerMethodField()
    final_cost_order = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields = ('date_time_order', 'orders', 'name_card', 'sum_order', 'discount_order', 'final_cost_order')

    def get_sum_order(self, instance):
        order = Orders.objects.get(pk=instance.pk)
        all_goods = order.orders.all()
        sum = 0
        for item in all_goods:
            sum += item.discount_cost
        return sum

    def get_discount_order(self, instance):
        order = Orders.objects.get(pk=instance.pk)
        all_goods = order.cards.first()
        return all_goods.card_discount

    def get_final_cost_order(self, instance):
        order = Orders.objects.get(pk=instance.pk)
        all_card_discount = order.cards.first().card_discount
        all_goods = order.orders.all()
        sum = 0
        for item in all_goods:
            sum += item.discount_cost
        return sum * (1 - all_card_discount/100)


    def create(self, validated_data):
        user, created = Orders.objects.get_or_create(**validated_data)
        if not created:
            raise ValidationError()
        return Orders
