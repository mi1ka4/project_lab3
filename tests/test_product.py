import pytest
from src.Product import Product


def test_create_product_valid():
    p = Product("prod_1", "Смартфон", 1000.0, 5)
    assert p.id == "prod_1"
    assert p.name == "Смартфон"
    assert p.price == 1000.0
    assert p.stock == 5


def test_create_product_negative_price():
    with pytest.raises(ValueError):
        Product("prod_1", "Смартфон", -1.0, 5)


def test_create_product_negative_stock():
    with pytest.raises(ValueError):
        Product("prod_1", "Смартфон", 100.0, -1)


def test_repr():
    p = Product("prod_1", "Смартфон", 100.0, 2)
    assert "prod_1" in repr(p)
    assert "Смартфон" in repr(p)


def test_eq():
    p1 = Product("p", "n", 1.0, 1)
    p2 = Product("p", "n", 1.0, 1)
    p3 = Product("p", "n", 1.0, 2)
    assert p1 == p2
    assert p1 != p3


def test_eq_not_product():
    p = Product("p", "n", 1.0, 1)
    assert p.__eq__("not product") is NotImplemented