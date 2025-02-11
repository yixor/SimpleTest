from datetime import datetime
from typing import Any, Dict

from fastapi import HTTPException

# from schemas.reciepts import Product


def format_number(value: float) -> str:
    return f"{value:,.2f}".replace(",", " ")


username = "user"
receipt_data = {
    "products": [
        {"name": "Mavic 3T", "price": 298870.00, "quantity": 3.00, "total": 896610.00},
        {
            "name": "Дрон FPV з акумулятором\n6S чорний",
            "price": 31000.00,
            "quantity": 20.00,
            "total": 620000.00,
        },
    ],
    "total": 1516610.00,
    "rest": 0.00,
    "payment": {"type": "cash", "amount": 1516610.00},
}


def gen_separator(char: str, width: int):
    return char * width


def get_header(prefix: str, data: str, sufix: str, width: int):
    if len(prefix) + len(data) + len(sufix) > width:
        return HTTPException()
    return f"{prefix}{data}{sufix}".center(width)


def gen_products(data: list[dict[str, Any]], width: int):
    # if len(data) > 0 and isinstance(data[0], dict):
    #     data = list(map(lambda product: Product(**product), data))
    for product in data:
        {format_number(product.quantity)}


def generate(width: int):
    separator = gen_separator("=", width)


def generate_receipt(
    username: str = username, data: Dict[str, Any] = receipt_data, width: int = 31
) -> str:
    # Header and line separators
    header = f"ФОП {username}".center(width)
    separator = "=" * width
    product_separator = "-" * width
    products_list = []
    # Odd check
    if width % 2 != 0:
        left_aligment = width // 2
        right_aligment = left_aligment + 1
    else:
        right_aligment = left_aligment = width // 2

    # Payment type
    payment_type = "Готівка" if data["payment"]["type"] == "cash" else "Картка"

    # Products
    products_last_index = len(data["products"]) - 1 if len(data["products"]) != 0 else 0
    for i, product in enumerate(data["products"]):
        quantity = (
            f"{format_number(product['quantity'])} x {format_number(product['price'])}"
        )
        total_price = f"{format_number(product['quantity'])}".rjust(right_aligment)
        products_list.append(quantity + " " + total_price)
        products_list.append(product["name"].ljust(left_aligment))
        if i != products_last_index:
            products_list.append(product_separator)
    products = "\n".join(products_list)
    for product in products_list:
        print(len(product))
    total = "СУМА".ljust(left_aligment) + f"{format_number(data['total'])}".rjust(
        right_aligment
    )
    payment = f"{payment_type}".ljust(
        left_aligment
    ) + f"{format_number(data['payment']['amount'])}".rjust(right_aligment)
    change = "Решта".ljust(left_aligment) + f"{format_number(data['rest'])}".rjust(
        right_aligment
    )

    footer = f"{datetime.now().strftime('%d.%m.%Y %H:%M')}".center(width)
    footer_end = "Дякуємо за покупку!".center(width)

    return "\n".join(
        [
            header,
            separator,
            products,
            separator,
            total,
            payment,
            change,
            separator,
            footer,
            footer_end,
        ]
    )


print(generate_receipt())
# RESULT = timeit(generate_receipt)
# print(RESULT)
