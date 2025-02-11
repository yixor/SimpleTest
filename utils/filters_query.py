import enum
from typing import Any, List, Optional

from schemas.reciepts import PaymentType, QueryPair, RecieptsFilter


class Filter:
    @staticmethod
    def _format_value(value: Any) -> str:
        if isinstance(value, str):
            return f"'{value}'"
        return str(value)

    @staticmethod
    def _querypair_to_sql(field_name: str, query: Optional["QueryPair"]) -> str:
        conditions = []
        if query:
            if query.gt is not None:
                conditions.append(f"{field_name} >= {Filter._format_value(query.gt)}")
            if query.ls is not None:
                conditions.append(f"{field_name} <= {Filter._format_value(query.gt)}")
            if query.eq is not None:
                conditions.append(f"{field_name} = {Filter._format_value(query.eq)}")
        return " AND ".join(conditions) if len(conditions) != 0 else ""

    @staticmethod
    def _enum_to_sql(field_name: str, value: Optional[enum.Enum]) -> str:
        if not value:
            return ""
        return f"{field_name} IN ({value.value})"

    @staticmethod
    def _add_limit_to_sql(limit: int):
        return f"LIMIT {limit}"

    @staticmethod
    def _add_offset_to_sql(offset: int):
        return f"OFFSET {offset}"

    @staticmethod
    def make_query(rf: RecieptsFilter):
        sql_conditions = []
        query_parts = []

        for field, field_info in rf.model_fields.items():
            value = getattr(rf, field)

            if isinstance(value, QueryPair):
                condition = Filter._querypair_to_sql(field, value)
                if condition:
                    sql_conditions.append(condition)
            elif isinstance(value, list) and field_info.annotation == List[PaymentType]:
                condition = Filter._enum_to_sql(field, value)
                if condition:
                    sql_conditions.append(condition)
            elif field == "limit":
                query_parts.append(Filter._add_limit_to_sql(value))
            elif field == "offset":
                query_parts.append(Filter._add_offset_to_sql(value))

        where_clause = " AND ".join(sql_conditions) if sql_conditions else ""
        limit_offset_clause = " ".join(query_parts)

        return where_clause + (" " + limit_offset_clause if limit_offset_clause else "")
