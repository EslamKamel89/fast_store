from sqlmodel import SQLModel


class OrderItem(SQLModel, table=True): ...
