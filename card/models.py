from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta
from django.utils.functional import cached_property
from datetime import datetime


# Срок действия карты задается на год
def get_end_active():
    today = datetime.now()
    return today + timedelta(days=365)

# Дефолтное значение для карты
def new_time():
    today = datetime.now()
    return today

# Модель описания карты
class Card(models.Model):
    TYPE = (
        ('A', _('Active')),
        ('N', _('Not active')),
        ('O', _('Overdue'))
    )
    series_card = models.CharField(_('Серия карты'), max_length=10)
    number_card = models.IntegerField(_('Номер карты'))
    date_start_card = models.DateTimeField(_('Дата активации карты'), default=new_time)
    date_end_active_card = models.DateTimeField(_('Дата окончания действия карты'), default=get_end_active)
    date_last_use_card = models.DateTimeField(_('Дата последнего использования карты'), default=new_time)
    sum_purchase = models.FloatField(_('Сумма покупок'), default=0)
    status_card = models.CharField(_('Статус карты'), max_length=1, choices=TYPE, default='A')
    card_discount = models.FloatField(_('Текущая скидка'), default=0)


    class Meta:
        verbose_name = _('Дисконтная карта')
        verbose_name_plural = _('Дисконтные карты')
        ordering = ['-date_start_card']

    def __str__(self):
        return f'Card: {self.series_card}{self.number_card}'

# Модель описания заказа
class Orders(models.Model):
    orders = models.ManyToManyField('Goods', verbose_name=_('Товар'), null=True, blank=True, related_name='orders')
    date_time_order = models.DateTimeField(_('Время заказа'), auto_now_add=True)
    sum_order = models.FloatField(_('Сумма заказа'))
    discount_order = models.FloatField(_('Скидка'))
    final_cost_order = models.FloatField(_('Финальная цена'))
    name_card = models.ManyToManyField(Card, null=True, verbose_name=_('Карта скидок'), blank=True, related_name='cards')


    class Meta:
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')
        ordering = ['-date_time_order']

    def __str__(self):
        return f'Order {self.id} : Sum {self.sum_order} : Date {self.date_time_order}'

    @cached_property
    def final_cost(self):
        return self.sum_order * ((100 - self.discount_order)/100)


# Модель описания товара
class Goods(models.Model):
    name_goods = models.CharField(_('Наименование товара'), max_length=100)
    cost_goods = models.FloatField(_('Стоимость товара'))
    discount_cost = models.FloatField(_('Финальная цена с учетом скидки'))


    class Meta:
        verbose_name = _('Товар')
        verbose_name_plural = _('Товары')

    def __str__(self):
        return f'Good: {self.name_goods}{self.cost_goods}'


# Модель описания корзины
class Basket(models.Model):
    series_card = models.CharField(_('Серия карты'), max_length=10)
    number_card = models.IntegerField(_('Номер карты'))
    date_start_card = models.DateTimeField(_('Дата активации карты'))
    date_end_active_card = models.DateTimeField(_('Дата окончания действия карты'))
    date_last_use_card = models.DateTimeField(_('Дата последнего использования карты'))
    sum_purchase = models.FloatField(_('Сумма покупок'))
    status_card = models.CharField(_('Статус карты'), max_length=1)
    card_discount = models.FloatField(_('Текущая скидка'))

    class Meta:
        verbose_name = _('Корзина')
        verbose_name_plural = _('Корзины')

    def __str__(self):
        return f'Card: {self.series_card}{self.number_card}'