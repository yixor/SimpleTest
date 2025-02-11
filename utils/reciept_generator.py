from typing import List, Literal
from fastapi import HTTPException, status

from models.reciept import Reciept
from models.users import User

Directions = Literal["left", "right", "both", "center"]


class RecieptGenerator:

    @staticmethod
    def _use_alignment(direction: Directions, content: List[str]):
        return "".join(
            []
        )

    @staticmethod
    def _proccess_line(
        line_width: int,
        content: str,
    ):
        if len(content) > line_width:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid line width, content is sticking out:\n{content}",
            )

    @staticmethod
    async def generate_reciept(user: User, reciept: Reciept, line_width: int):

        user.name
