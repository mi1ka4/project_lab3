class Product:

    def __init__(self, product_id: str, name: str, price: float, stock: int):
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        if stock < 0:
            raise ValueError("Количество на складе не может быть отрицательным")

        self.id: str = product_id
        self.name: str = name
        self.price: float = price
        self.stock: int = stock

    def __repr__(self) -> str:
        return f"Product(id={self.id!r}, name={self.name!r}, price={self.price}, stock={self.stock})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        return (
            self.id == other.id
            and self.name == other.name
            and self.price == other.price
            and self.stock == other.stock
        )