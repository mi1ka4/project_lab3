from typing import Dict
from src.Product import Product

class ShoppingCartError(Exception):
    pass


class ProductNotFoundError(ShoppingCartError):
    pass


class InvalidQuantityError(ShoppingCartError):
    pass


class InsufficientStockError(ShoppingCartError):
    pass


class ShoppingCart:

    def __init__(self, catalog: Dict[str, Product]):
        self._catalog: Dict[str, Product] = catalog
        self._items: Dict[str, int] = {}


    def _get_product(self, product_id: str) -> Product:
        product = self._catalog.get(product_id)
        if product is None: raise ProductNotFoundError(f"Товар с id={product_id!r} не найден")
        return product

    @property
    def items(self) -> Dict[str, int]:
        return dict(self._items)

    def add_product(self, product_id: str, quantity: int) -> None:
        
        if quantity <= 0:
            raise InvalidQuantityError("Количество должно быть положительным")

        product = self._get_product(product_id)
        current = self._items.get(product_id, 0)
        new_quantity = current + quantity

        if new_quantity > product.stock:
            raise InsufficientStockError(
                f"На складе только {product.stock} шт., "
                f"запрошено {new_quantity} шт."
            )

        self._items[product_id] = new_quantity


    def remove_product(self, product_id: str, quantity: int | None = None) -> None:
        
        if product_id not in self._items:
            raise ProductNotFoundError(f"Товара с id={product_id!r} нет в корзине")

        
        if quantity <= 0: raise InvalidQuantityError("Количество должно быть положительным")
        
        if quantity is None:
            del self._items[product_id]
            return

        

        current = self._items[product_id]
        if quantity >= current:
            del self._items[product_id]
        else:
            self._items[product_id] = current - quantity


    def total_price(self) -> float:
        total = 0.0
        for product_id, qty in self._items.items():
            product = self._catalog.get(product_id)
            if product is not None: total += product.price * qty
        return total