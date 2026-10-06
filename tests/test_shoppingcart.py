import pytest
from src.Product import Product
from src.ShoppingCart import (
    ShoppingCart,
    ProductNotFoundError,
    InvalidQuantityError,
    InsufficientStockError,
    InvalidPromoCodeError
)


@pytest.fixture
def catalog():
    return {
        "prod_1": Product("prod_1", "Смартфон", 1000.0, 5),
        "prod_2": Product("prod_2", "Наушники", 500.0, 10),
    }


@pytest.fixture
def cart(catalog):
    return ShoppingCart(catalog)



def test_add_new_product(cart):
    cart.add_product("prod_1", 2)
    assert cart.items == {"prod_1": 2}


def test_add_existing_product(cart):
    cart.add_product("prod_1", 2)
    cart.add_product("prod_1", 1)
    assert cart.items == {"prod_1": 3}


def test_add_zero_quantity(cart):
    with pytest.raises(InvalidQuantityError):
        cart.add_product("prod_1", 0)


def test_add_negative_quantity(cart):
    with pytest.raises(InvalidQuantityError):
        cart.add_product("prod_1", -1)


def test_add_unknown_product(cart):
    with pytest.raises(ProductNotFoundError):
        cart.add_product("unknown", 1)


def test_add_more_than_stock(cart):
    with pytest.raises(InsufficientStockError):
        cart.add_product("prod_1", 6)


def test_add_exceeding_stock_with_existing(cart):
    cart.add_product("prod_1", 3)
    with pytest.raises(InsufficientStockError):
        cart.add_product("prod_1", 3)



def test_remove_full(cart):
    cart.add_product("prod_1", 3)
    cart.remove_product("prod_1")
    assert cart.items == {}


def test_remove_partial(cart):
    cart.add_product("prod_1", 3)
    cart.remove_product("prod_1", 1)
    assert cart.items == {"prod_1": 2}


def test_remove_more_than_in_cart_removes_all(cart):
    cart.add_product("prod_1", 2)
    cart.remove_product("prod_1", 5)
    assert cart.items == {}


def test_remove_exact_amount(cart):
    cart.add_product("prod_1", 2)
    cart.remove_product("prod_1", 2)
    assert cart.items == {}


def test_remove_unknown_product(cart):
    with pytest.raises(ProductNotFoundError):
        cart.remove_product("prod_1")


def test_remove_zero(cart):
    cart.add_product("prod_1", 1)
    with pytest.raises(InvalidQuantityError):
        cart.remove_product("prod_1", 0)


def test_remove_negative(cart):
    cart.add_product("prod_1", 1)
    with pytest.raises(InvalidQuantityError):
        cart.remove_product("prod_1", -1)



def test_total_price_empty(cart):
    assert cart.total_price() == 0.0


def test_total_price_one_product(cart):
    cart.add_product("prod_1", 2)
    assert cart.total_price() == 2000.0


def test_total_price_multiple(cart):
    cart.add_product("prod_1", 1)
    cart.add_product("prod_2", 3)
    assert cart.total_price() == 1000.0 + 1500.0


def test_total_price_one_product_promocode(cart):
    cart.add_product("prod_1", 2)
    cart.apply_promo("SALE10")
    assert cart.total_price() == 1800.0
    cart.apply_promo("SALE20")
    assert cart.total_price() == 1600.0


def test_total_price_multiple_promocode(cart):
    cart.add_product("prod_1", 1)
    cart.add_product("prod_2", 3)
    cart.apply_promo("SALE10")
    assert cart.total_price() == round((1000.0 + 1500.0)*(1-10/100),2)
    cart.apply_promo("SALE20")
    assert cart.total_price() == round((1000.0 + 1500.0)*(1-20/100),2)

def test_promocode_apply_error(cart):
    with pytest.raises(InvalidPromoCodeError):
        cart.apply_promo("SALE100")


def test_items_returns_copy(cart):
    cart.add_product("prod_1", 1)
    snapshot = cart.items
    snapshot["prod_1"] = 999
    assert cart.items["prod_1"] == 1