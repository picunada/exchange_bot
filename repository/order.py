import datetime
from typing import List, Optional
from models import Order
from database import orders
from repository import BaseRepository


class OrdersRepository(BaseRepository):
    async def get_all(self, limit: int = 25, skip: int = 0) -> List[Order]:
        query = orders.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    async def get_by_id(self, id: int) -> Optional[Order]:
        query = orders.select().where(orders.c.id == id)
        order = await self.database.fetch_one(query=query)
        if order is None:
            return None
        return Order.parse_obj(order)

    async def create(self, o: Order) -> Order:
        order = Order(
            amount=o.amount,
            rate=o.rate,
            withdraw_card=o.withdraw_card,
            is_paid=o.is_paid,
            status_id=o.status_id,
            payment_url=o.payment_url,
            created_at=datetime.datetime.utcnow()
        )
        values = {**order.dict()}
        values.pop("id", None)
        print(values)
        query = orders.insert().values(**values)
        print(query)
        order.id = await self.database.execute(query=query)
        return order

    async def update(self, id: int, user_id: int, o: Order, is_in_stock: bool):
        order = Order(
            id=id,
            amount=o.amount,
            rate=o.rate,
            withdraw_card=o.withdraw_card,
            is_paid=o.is_paid,
            status_id=o.status_id,
            payment_url=o.payment_url,
            created_at=datetime.datetime.utcnow()
        )
        values = {**order.dict()}
        values.pop("created_at", None)
        values.pop("id", None)
        query = orders.update().where(orders.c.id == id).values(**values)
        await self.database.execute(query=query)
        return order

    async def delete(self, id: int):
        query = orders.delete().where(orders.c.id == id)
        return await self.database.execute(query=query)
