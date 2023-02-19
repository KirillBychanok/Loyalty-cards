import pytestqq

from .models import Orders, Card, Goods

@pytest.fixture
def create_goods_factory():
    def create_app_goods(
        name_goods: str,
        cost_goods: int,
        discount_cost: int
    ):
        goods = Goods.objects.create(
            name_goods = name_goods,
            cost_goods = cost_goods,
            discount_cost = discount_cost
        )
        return goods

    return create_app_goods


@pytest.fixture
def create_goods1(create_goods_factory):
    return create_goods_factory("Tomato", "20", "17")


@pytest.fixture
def create_goods2(create_goods_factory):
    return create_goods_factory("Potato", "15", "12")


@pytest.fixture
def create_card_factory():
    def create_app_card(
        series_card: str,
        number_card: int,
        status_card: str,
        card_discount: int
    ):
        cards = Card.objects.create(
            series_card = series_card,
            number_card = number_card,
            status_card = status_card,
            card_discount = card_discount
        )
        return cards

    return create_app_card


@pytest.fixture
def create_card1(create_card_factory):
    return create_card_factory("AB", "123456", "N", "5")


@pytest.fixture
def create_card2(create_card_factory):
    return create_card_factory("BC", "123456789", "A", "2")