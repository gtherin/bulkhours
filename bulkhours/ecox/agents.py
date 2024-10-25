import pandas as pd
import numpy as np



try:
    from mesa import Agent, Model
        
except ImportError:
    # Define a dummy class if the library is not available
    class Agent:
        def __init__(self, unique_id, model):
            print("mesa is not available. Using dummy class.")

        def perform_action(self, *args, **kwargs):
            print("Dummy action performed")
            return None
    class Model:
        def __init__(self, *args, **kwargs):
            print("mesa is not available. Using dummy class.")        

class Order:
    """Represents a single order (buy or sell) in the order book."""
    def __init__(self, order_type, price, quantity):
        self.order_type = order_type  # 'buy' or 'sell'
        self.price = price
        self.quantity = quantity


class Buyer(Agent):
    """A buyer places a bid order in the stock market."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # Generate a random bid (price and quantity)
        price = np.random.uniform(90, 110)  # Random price between 90 and 110
        quantity = np.random.randint(1, 10)  # Random quantity between 1 and 10
        order = Order(order_type="buy", price=price, quantity=quantity)
        self.model.bids.append(order)
        #print(f"Buyer {self.unique_id} placed a bid: Price={price}, Quantity={quantity}")
