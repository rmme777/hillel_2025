import uuid
from dataclasses import dataclass
import random
from datetime import datetime, timedelta
import queue
import threading
import time


OrderRequestBody = tuple[str, datetime]
OrderDeliveryBody = tuple[str, datetime, str]


storage = {
    "delivery": {},
    "users": [],
    "dishes": [
        {
            "id": 1,
            "name": "Salad",
            "value": 1099,
            "restaurant": "Silpo",
        },
        {
            "id": 2,
            "name": "Soda",
            "value": 199,
            "restaurant": "Silpo",
        },
        {
            "id": 3,
            "name": "Pizza",
            "value": 599,
            "restaurant": "Kvadrat",
        },
    ],
    # ...
}


class Scheduler:
    def __init__(self):
        self.orders: queue.Queue[OrderRequestBody] = queue.Queue()

    def process_orders(self) -> None:
        print("SCHEDULER PROCESSING...")

        while True:
            order = self.orders.get(True)

            time_to_wait = order[1] - datetime.now()

            if time_to_wait.total_seconds() > 0:
                self.orders.put(order)
                time.sleep(0.5)
            else:
                delivery = DeliveryProcess()
                delivery.create_delivery_order(order)


    def add_order(self, order: OrderRequestBody) -> None:
        self.orders.put(order)
        print(f"\n\t{order[0]} ADDED FOR PROCESSING")



class DeliveryProviderRegistry:
    registry: list[type] = []

    @classmethod
    def register(cls, provider_cls: type):
        instance = provider_cls()
        cls.registry.append(instance)


class DeliveryProcess:
    def __init__(self):
        self.deliveries: queue.Queue[tuple[OrderDeliveryBody, uuid.UUID]] = queue.Queue()
        self.providers: dict[str, int] = {}
        self.providers_delivery_time = {}


    def _check_providers_orders(self):
        for provider_instance in DeliveryProviderRegistry.registry:
            provider_name = type(provider_instance).__name__.lower()
            self.providers[provider_name] = getattr(provider_instance, f"{provider_name}_number_of_orders")


    def _get_providers_delivery_time(self):
        for provider_instance in DeliveryProviderRegistry.registry:
            provider_name = type(provider_instance).__name__.lower()
            self.providers_delivery_time[provider_name] = getattr(provider_instance, f"{provider_name}_delivery_time")

    def _select_random_provider(self):
        provider_chose = random.choice(list(self.providers_delivery_time.keys()))
        for i in DeliveryProviderRegistry.registry:
            if type(i).__name__.lower() == provider_chose:
                i.add_order()
        return provider_chose

    def _select_least_loaded_provider(self):
        least_loaded = min(self.providers, key=self.providers.get)
        for i in DeliveryProviderRegistry.registry:
            if type(i).__name__.lower() == least_loaded:
                i.add_order()
        return least_loaded


    def create_delivery_order(self, order: str):
        self._get_providers_delivery_time()
        self._check_providers_orders()
        if self.providers:
            least_loaded = self._select_least_loaded_provider()
            delivery_time = self.providers_delivery_time.get(least_loaded)
            self.ship((order, delivery_time, least_loaded))
        else:
            provider_chose = self._select_random_provider()
            delivery_time = self.providers_delivery_time.get(provider_chose)
            self.ship((order, delivery_time, provider_chose))


    def ship(self,  order: OrderDeliveryBody):
        order_to_put = (order, uuid.uuid4())
        self.deliveries.put(order_to_put)
        print(f'\n\t🚚 ORDER {order[0][0]} IN THE PROCESS OF DELIVERY. WILL ARRIVE IN {order[1]} BY {order[2].upper()}.')
        storage['delivery'][order_to_put[1]] = [order[2], 'ongoing']
        print(F'[DEBUG] Orders: {self.providers}')
        print('[DEBUG] Storage:', storage['delivery'])
        self._ship(order_to_put)


    @staticmethod
    def _ship(order: tuple[OrderDeliveryBody, uuid.uuid4()]):

        def _callback():
            time.sleep(order[0][1])
            storage["delivery"][order[1]] = (
                order[0][2], "finished"
            )
            print(f"\n\t🚚 DELIVERED {order[0][0][0]}")

        thread = threading.Thread(target=_callback)
        thread.start()


    def process_delivery(self):
        print('DELIVERY PROCESSING...')

        while True:

            order_to_remove: dict[uuid.UUID, str] = {}

            for order_id, value in storage['delivery'].items():
                if value[1] == 'finished':
                    order_to_remove[order_id] = value[0]
                    print(F'[SYSTEM NOTIFICATION]: ORDER {order_id} DELIVERY IS FINISHED✅')

            for order_id, provider in order_to_remove.items():
                for j in DeliveryProviderRegistry.registry:
                    if type(j).__name__.lower() == provider:
                        j.delete_order()

            for order_id in order_to_remove.keys():
                del storage['delivery'][order_id]
                print(f'[SYSTEM NOTIFICATION]: {order_id} REMOVED FROM STORAGE🗑')
                print(F'[DEBUG] Orders: {self.providers}')
                print('[DEBUG] Storage:', storage['delivery'])



@dataclass
class Uklon(DeliveryProcess):
    uklon_number_of_orders = 0
    uklon_delivery_time = 5

    def add_order(self):
        self.uklon_number_of_orders += 1

    def delete_order(self):
        self.uklon_number_of_orders -= 1

DeliveryProviderRegistry.register(Uklon)

@dataclass
class Uber(DeliveryProcess):
    uber_number_of_orders = 0
    uber_delivery_time = 3

    def add_order(self):
        self.uber_number_of_orders += 1

    def delete_order(self):
        self.uber_number_of_orders -= 1

DeliveryProviderRegistry.register(Uber)


def main():
    scheduler = Scheduler()
    delivery = DeliveryProcess()
    order_thread = threading.Thread(target=scheduler.process_orders, daemon=True)
    order_thread.start()
    delivery_thread = threading.Thread(target=delivery.process_delivery, daemon=True)
    delivery_thread.start()

    # user input:
    # A 5 (in 5 days)
    # B 3 (in 3 days)
    while True:
        order_details = input("Enter order details: ")
        data = order_details.split(" ")
        order_name = data[0]
        print(order_name)
        delay = datetime.now() + timedelta(seconds=int(data[1]))
        scheduler.add_order(order=(order_name, delay))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        raise SystemExit(0)