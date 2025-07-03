import psycopg
from dataclasses import dataclass

connection_payload = {
    "dbname": "hillel",
    "user": "hillel_homework_user",
    "password": "qwerty",
    "host": "localhost",
    "port": 5432,
}

class DatabaseConnection:
    def __enter__(self):
        self.conn = psycopg.connect(**connection_payload)
        self.cur = self.conn.cursor()

        return self

    def __exit__(self, exc_type, *_):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()

        self.cur.close()
        self.conn.close()

    def query(self, sql: str, params: tuple | None = None):
        self.cur.execute(sql, params or ())
        return self.cur.fetchall()


@dataclass
class User:
    name: str
    id: int | None = None

    @classmethod
    def all(cls) -> list["User"]:

        with DatabaseConnection() as db:
            rows = db.query("SELECT name, id FROM users")
            return [cls(*row) for row in rows]

    @classmethod
    def filter(cls, **filters) -> list["User"]:

        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())

        with DatabaseConnection() as db:
            rows = db.query(
                f"SELECT name, id FROM users WHERE {conditions}",
                values,
            )
            return [cls(*row) for row in rows]

    @classmethod
    def get(cls, **filters) -> "User":

        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())

        with DatabaseConnection() as db:
            rows = db.query(
                f"SELECT name, id FROM users WHERE {conditions}",
                values,
            )
            name,id_ = rows[0]

            return cls(id=id_, name=name)

    def create(self) -> "User":
        with DatabaseConnection() as db:
            db.cur.execute(
                "INSERT INTO users (name) VALUES (%s) RETURNING id",
                (self.name,)
            )

            self.id = db.cur.fetchone()[0]

            return self

    def update(self, **payload) -> "User | None":
        fields = ", ".join([f"{key} = %s" for key in payload])
        values = tuple(payload.values())

        if self.id is None:
            raise ValueError("Can not update user without ID")

        with DatabaseConnection() as db:
            db.cur.execute(
                f"UPDATE users SET {fields} WHERE id = %s RETURNING id, name",
                (*values, self.id),
            )

            row = db.cur.fetchone()

        if not row:
            return None
        else:
            name = row
            self.name = name
            return self

    @classmethod
    def delete(cls, id_: int) -> bool:
        with DatabaseConnection() as db:
            db.cur.execute("DELETE FROM users WHERE id = %s RETURNING id", (id_,))
            return db.cur.fetchone() is not None

@dataclass
class Dish:
    dish_name: str
    price: float
    id: int | None = None

    @classmethod
    def all(cls) -> list["Dish"]:

        with DatabaseConnection() as db:
            rows = db.query("SELECT dish_name, price, id FROM dishes")
            return [cls(*row) for row in rows]

    @classmethod
    def filter(cls, **filters) -> list["Dish"]:

        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())

        with DatabaseConnection() as db:
            rows = db.query(
                f"SELECT dish_name, price, id FROM dishes WHERE {conditions}",
                values,
            )
            return [cls(*row) for row in rows]

    @classmethod
    def get(cls, **filters) -> "Dish":

        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())

        with DatabaseConnection() as db:
            rows = db.query(
                f"SELECT dish_name, price, id FROM dishes WHERE {conditions}",
                values,
            )
            dish_name, price, id_ = rows[0]

            return cls(id=id_, dish_name=dish_name, price=price)

    def create(self) -> "Dish":
        with DatabaseConnection() as db:
            db.cur.execute(
                "INSERT INTO dishes (dish_name, price) VALUES (%s, %s) RETURNING id",
                (self.dish_name, self.price)
            )

            self.id = db.cur.fetchone()[0]

            return self

    def update(self, **payload) -> "Dish | None":
        fields = ", ".join([f"{key} = %s" for key in payload])
        values = tuple(payload.values())

        if self.id is None:
            raise ValueError("Can not update dish without ID")

        with DatabaseConnection() as db:
            db.cur.execute(
                f"UPDATE dishes SET {fields} WHERE id = %s RETURNING id, dish_name, price",
                (*values, self.id),
            )

            row = db.cur.fetchone()

        if not row:
            return None
        else:
            dish_name, price = row
            self.dish_name = dish_name
            self.price = price
            return self

    @classmethod
    def delete(cls, id_: int) -> bool:
        with DatabaseConnection() as db:
            db.cur.execute("DELETE FROM dishes WHERE id = %s RETURNING id", (id_,))
            return db.cur.fetchone() is not None


@dataclass
class Order:
    user_id: int
    order_item_id: int
    total: float
    id: int | None = None

    @classmethod
    def all(cls) -> list["Order"]:

        with DatabaseConnection() as db:
            rows = db.query("SELECT user_id, order_item_id, total, id FROM orders")
            return [cls(*row) for row in rows]

    @classmethod
    def filter(cls, **filters) -> list["Order"]:

        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())

        with DatabaseConnection() as db:
            rows = db.query(
                f"SELECT user_id, order_item_id, total, id FROM orders WHERE {conditions}",
                values,
            )
            return [cls(*row) for row in rows]

    @classmethod
    def get(cls, **filters) -> "Order":

        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())

        with DatabaseConnection() as db:
            rows = db.query(
                f"SELECT user_id, order_item_id, total, id FROM orders WHERE {conditions}",
                values,
            )
            user_id, order_item_id, total, id_ = rows[0]

            return cls(id=id_, user_id=user_id, order_item_id=order_item_id, total=total)

    def create(self) -> "Order":
        with DatabaseConnection() as db:
            db.cur.execute(
                "INSERT INTO orders (user_id, order_item_id, total) VALUES (%s, %s, %s) RETURNING id",
                (self.user_id, self.order_item_id, self.total)
            )

            self.id = db.cur.fetchone()[0]

            return self

    def update(self, **payload) -> "Order | None":
        fields = ", ".join([f"{key} = %s" for key in payload])
        values = tuple(payload.values())

        if self.id is None:
            raise ValueError("Can not update order without ID")

        with DatabaseConnection() as db:
            db.cur.execute(
                f"UPDATE orders SET {fields} WHERE id = %s RETURNING id, user_id, order_item_id, total",
                (*values, self.id),
            )

            row = db.cur.fetchone()

        if not row:
            return None
        else:
            user_id, order_item_id, total = row
            self.user_id = user_id
            self.order_item_id = order_item_id
            self.total = total
            return self

    @classmethod
    def delete(cls, id_: int) -> bool:
        with DatabaseConnection() as db:
            db.cur.execute("DELETE FROM orders WHERE id = %s RETURNING id", (id_,))
            return db.cur.fetchone() is not None


@dataclass
class OrderItem:
    dish_id: int
    quantity: int
    id: int | None = None

    @classmethod
    def all(cls) -> list["OrderItem"]:

        with DatabaseConnection() as db:
            rows = db.query("SELECT dish_id, quantity, id FROM order_item")
            return [cls(*row) for row in rows]

    @classmethod
    def filter(cls, **filters) -> list["OrderItem"]:

        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())

        with DatabaseConnection() as db:
            rows = db.query(
                f"SELECT dish_id, quantity, id FROM order_item WHERE {conditions}",
                values,
            )
            return [cls(*row) for row in rows]

    @classmethod
    def get(cls, **filters) -> "OrderItem":

        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())

        with DatabaseConnection() as db:
            rows = db.query(
                f"SELECT dish_id, quantity, id FROM order_item WHERE {conditions}",
                values,
            )
            dish_id, quantity, id_ = rows[0]

            return cls(id=id_, dish_id=dish_id, quantity=quantity)

    def create(self) -> "OrderItem":
        with DatabaseConnection() as db:
            db.cur.execute(
                "INSERT INTO order_item (dish_id, quantity) VALUES (%s, %s) RETURNING id",
                (self.dish_id, self.quantity)
            )

            self.id = db.cur.fetchone()[0]

            return self

    def update(self, **payload) -> "OrderItem | None":
        fields = ", ".join([f"{key} = %s" for key in payload])
        values = tuple(payload.values())

        if self.id is None:
            raise ValueError("Can not update order item without ID")

        with DatabaseConnection() as db:
            db.cur.execute(
                f"UPDATE order_item SET {fields} WHERE id = %s RETURNING id, dish_id, quantity",
                (*values, self.id),
            )

            row = db.cur.fetchone()

        if not row:
            return None
        else:
            dish_id, quantity = row
            self.dish_id = dish_id
            self.quantity = quantity
            return self

    @classmethod
    def delete(cls, id_: int) -> bool:
        with DatabaseConnection() as db:
            db.cur.execute("DELETE FROM order_item WHERE id = %s RETURNING id", (id_,))
            return db.cur.fetchone() is not None


dish = Dish(dish_name="Avocado", price=34.0)
dish.create()

print(Dish.get(id=1))