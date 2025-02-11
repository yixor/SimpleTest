import sys
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


def _gen_name(username: str, width: int):
    return f"ФОП {username}".center(width)

def _format_number(value: float) -> str:
    return f"{value:,.2f}".replace(",", " ")

def _gen_product_q_to_p(product : dict, width : int):
    return f"{_format_number(product["quantity"])} x {_format_number(product["price"])}".ljust(width)

def _get_product_name_total(product : dict, width : int):
    name : str = product["name"]
    if len(name) > width:
        map()

                

def generate_reciept(username: str, products : list[dict], width: int, chapter_symbol : str = "=", product_char : str = "-"):
    chapter_separator = chapter_symbol * width
    product_separator = product_char * width
    for i, product in enumerate(products):
        