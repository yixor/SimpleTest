from fastapi import HTTPException, status

from schemas.reciepts import RecieptGet, Product, PaymentType


class TextReciept:
    def __init__(
        self,
        reciept_width: int,
        reciept: RecieptGet,
        chapter_char: str = "=",
        product_char: str = "-",
    ) -> None:
        self.reciept_width = reciept_width
        self.reciept = reciept
        self.chapter_char = chapter_char
        self.product_char = product_char

    def _gen_name(self, username: str):
        return f"ФОП {username}".center(self.reciept_width)

    def _format_number(self, value: float | None) -> str:
        return f"{value:,.2f}".replace(",", " ")

    def _gen_product_quantity_and_price(self, product: Product):
        return (
            f"{self._format_number(product.quantity)}"
            + " x "
            + f"{self._format_number(product.price)}"
        ).ljust(self.reciept_width)

    def _gen_product_name_and_total(self, product: Product):
        name: str = product.name
        total: str = self._format_number(product.total)
        if len(name) < self.reciept_width // 2:
            return (
                f"{name}"
                + f"{' ' * (self.reciept_width - len(name) - len(total))}"
                + f"{total}"
            )
        max_name_length = self.reciept_width - len(total)
        name_words = name.split(" ")
        words_length = len(name_words)
        max_index = words_length - 1
        index = 0
        words_list = []
        while True:
            if index < max_index:
                if (
                    len(name_words[index]) + len(name_words[index + 1])
                ) < max_name_length:
                    words_list.append(f"{name_words[index]} {name_words[index + 1]}")
                    index += 2
                else:
                    words_list.append(name_words[index])
                    index += 1
            if index == max_index:
                last_name_part = words_list[:-1]
                if len(last_name_part) + len(total) <= self.reciept_width:
                    words_list[:-1] = (
                        f"{last_name_part}"
                        + f"{' ' * (self.reciept_width - len(last_name_part) - len(total))}"
                        + f"{total}"
                    )
                    break
                else:
                    raise HTTPException(
                        status_code=status.HTTP_411_LENGTH_REQUIRED,
                        detail="Cannot generate reciept with given line width",
                    )
        return "\n".join(words_list)

    def _generate_summary(self):
        summary = []
        total = self._format_number(self.reciept.total)

        summary.append(
            "СУМА" + f"{' ' * (self.reciept_width - len('СУМА') - len(total))}" + total
        )
        payment_type_str = (
            "Картка" if self.reciept.payment.type == PaymentType.CASHLESS else "Готівка"
        )
        payment_amount = self._format_number(self.reciept.total - self.reciept.rest)
        summary.append(
            payment_type_str
            + f"{' ' * (self.reciept_width - len(payment_type_str) - len(total))}"
            + payment_amount
        )
        rest = self._format_number(self.reciept.rest)
        summary.append(
            "Решта" + f"{' ' * (self.reciept_width - len('Решта') - len(rest))}" + rest
        )
        return "\n".join(summary)

    def generate_reciept(self, user_name: str):
        reciept_lines = []

        chapter_separator = self.chapter_char * self.reciept_width
        product_separator = self.product_char * self.reciept_width

        reciept_lines.append(self._gen_name(user_name))
        reciept_lines.append(chapter_separator)

        products_count = len(self.reciept.products)
        if products_count == 1:
            reciept_lines.append(
                self._gen_product_quantity_and_price(self.reciept.products[0])
            )
            reciept_lines.append(
                self._gen_product_name_and_total(self.reciept.products[0])
            )
            reciept_lines.append(chapter_separator)
        else:
            for i, product in enumerate(self.reciept.products):
                reciept_lines.append(self._gen_product_quantity_and_price(product))
                reciept_lines.append(self._gen_product_name_and_total(product))
                if i < products_count:
                    reciept_lines.append(product_separator)
                else:
                    reciept_lines.append(chapter_separator)

        reciept_lines.append(self._generate_summary())
        reciept_lines.append(chapter_separator)
        reciept_lines.append(
            self.reciept.created.strftime("%H:%M:%S %d.%m.%Y").center(
                self.reciept_width
            )
        )
        reciept_lines.append("Дякуємо за покупку!".center(self.reciept_width))
        return "\n".join(reciept_lines)
