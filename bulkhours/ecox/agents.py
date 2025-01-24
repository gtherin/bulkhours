import pandas as pd
import numpy as np
from .lob import OrderBook

try:
    from mesa import Agent, Model
    from mesa.time import RandomActivation
    from mesa.datacollection import DataCollector

except ImportError:
    class Agent:
        def __init__(self, unique_id, model):
            print("mesa is not available. Using dummy class.")

        def perform_action(self, *args, **kwargs):
            print("Dummy action performed")
            return None

    class Model:
        def __init__(self, *args, **kwargs):
            print("mesa is not available. Using dummy class.")        

    class RandomActivation:
        def __init__(self, *args, **kwargs):
            print("mesa is not available. Using dummy class.")        

    class DataCollector:
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


class Seller(Agent):
    """A seller places an ask order in the stock market."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # Generate a random ask (price and quantity)
        price = np.random.uniform(90, 110)  # Random price between 90 and 110
        quantity = np.random.randint(1, 10)  # Random quantity between 1 and 10
        order = Order(order_type="sell", price=price, quantity=quantity)
        self.model.asks.append(order)
        #print(f"Seller {self.unique_id} placed an ask: Price={price}, Quantity={quantity}")


class MarketMaker(Agent):
    """A market maker places both bid and ask orders around the estimated market price."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # Estimate a market price as the midpoint between highest bid and lowest ask
        if self.model.bids and self.model.asks:
            best_bid = max(self.model.bids, key=lambda x: x.price).price
            best_ask = min(self.model.asks, key=lambda x: x.price).price
            market_price = (best_bid + best_ask) / 2
        else:
            market_price = np.random.uniform(95, 105)  # Default to a random market price

        # Place bid and ask orders around the market price
        bid_price = market_price * np.random.uniform(0.99, 1.01)  # Slightly below market price
        ask_price = market_price * np.random.uniform(1.01, 1.03)  # Slightly above market price
        quantity = np.random.randint(1, 10)  # Random quantity

        # Create and submit the orders
        bid_order = Order(order_type="buy", price=bid_price, quantity=quantity)
        ask_order = Order(order_type="sell", price=ask_price, quantity=quantity)
        self.model.bids.append(bid_order)
        self.model.asks.append(ask_order)
        #print(f"Market Maker {self.unique_id} placed a bid: Price={bid_price}, Quantity={quantity}")
        #print(f"Market Maker {self.unique_id} placed an ask: Price={ask_price}, Quantity={quantity}")


class SniperAgent(Agent):
    """A sniper agent waits for favorable market conditions and places large orders opportunistically."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # The sniper monitors the market and waits for favorable conditions
        if self.model.bids and self.model.asks:
            best_bid = max(self.model.bids, key=lambda x: x.price).price
            best_ask = min(self.model.asks, key=lambda x: x.price).price

            # If the bid-ask spread is favorable, snipe with a large order
            if (best_ask - best_bid) < 1:  # Arbitrary threshold for favorable conditions
                quantity = np.random.randint(10, 20)  # Large quantity for sniper trade

                # Place a buy order at the best ask price
                sniper_order = Order(order_type="buy", price=best_ask, quantity=quantity)
                self.model.bids.append(sniper_order)
                #print(f"Sniper {self.unique_id} placed a snipe bid at Price={best_ask} for Quantity={quantity}")


class GuerillaAgent(Agent):
    """A guerilla agent breaks large orders into smaller chunks and executes them stealthily."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.remaining_quantity = np.random.randint(20, 50)  # Initial large order quantity

    def step(self):
        if self.remaining_quantity > 0:
            # Determine chunk size (small random portion of remaining order)
            chunk_size = min(self.remaining_quantity, np.random.randint(1, 5))
            self.remaining_quantity -= chunk_size

            # Randomly choose a limit price within a reasonable range
            if self.model.bids and self.model.asks:
                best_bid = max(self.model.bids, key=lambda x: x.price).price
                best_ask = min(self.model.asks, key=lambda x: x.price).price
                target_price = (best_bid + best_ask) / 2
                price_variation = np.random.uniform(0.99, 1.01)
                limit_price = target_price * price_variation
            else:
                limit_price = np.random.uniform(95, 105)

            # Place a buy order (for simplicity, this example uses buy orders)
            guerilla_order = Order(order_type="buy", price=limit_price, quantity=chunk_size)
            self.model.bids.append(guerilla_order)
            #print(f"Guerilla Agent {self.unique_id} placed a buy order: Price={limit_price}, Quantity={chunk_size}")


class BlastAgent(Agent):
    """A blast agent places a large order all at once, impacting the market."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # Place a large buy order with significant quantity at the best ask price
        quantity = np.random.randint(50, 100)
        if self.model.asks:
            best_ask = min(self.model.asks, key=lambda x: x.price).price
            blast_order = Order(order_type="buy", price=best_ask, quantity=quantity)
            self.model.bids.append(blast_order)
            #print(f"Blast Agent {self.unique_id} placed a large buy order at Price={best_ask}, Quantity={quantity}")


class IcebergAgent(Agent):
    """An iceberg agent hides part of a large order by placing smaller chunks over time."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.remaining_quantity = np.random.randint(100, 200)  # Large initial order size
        self.visible_chunk_size = 10  # Size of each visible portion of the order

    def step(self):
        if self.remaining_quantity > 0:
            chunk_size = min(self.visible_chunk_size, self.remaining_quantity)
            self.remaining_quantity -= chunk_size
            if self.model.asks:
                best_ask = min(self.model.asks, key=lambda x: x.price).price
                iceberg_order = Order(order_type="buy", price=best_ask, quantity=chunk_size)
                self.model.bids.append(iceberg_order)
                #print(f"Iceberg Agent {self.unique_id} placed a chunk buy order at Price={best_ask}, Quantity={chunk_size}")


class SharkAgent(Agent):
    """A shark agent detects large orders and trades around them to profit."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # Detect if there are large orders in the order book
        large_orders = [order for order in self.model.bids if order.quantity > 20]
        if large_orders:
            target_order = large_orders[0]  # Target the first large order
            # Place a sell order slightly above the large order price
            shark_price = target_order.price * 1.01  # Slightly above the large order price
            shark_order = Order(order_type="sell", price=shark_price, quantity=5)
            self.model.asks.append(shark_order)
            #print(f"Shark Agent {self.unique_id} placed a sell order at Price={shark_price}, Quantity=5")


class StealthAgent(Agent):
    """A stealth agent executes small trades at random intervals to avoid detection."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # Randomly decide if the agent should trade in this step
        if np.random.rand() < 0.5:  # 50% chance to place an order
            quantity = np.random.randint(1, 3)  # Small quantity for stealth
            if self.model.asks:
                best_ask = min(self.model.asks, key=lambda x: x.price).price
                stealth_order = Order(order_type="buy", price=best_ask, quantity=quantity)
                self.model.bids.append(stealth_order)
                #print(f"Stealth Agent {self.unique_id} placed a small buy order at Price={best_ask}, Quantity={quantity}")


class SumoAgent(Agent):
    """A sumo agent aggressively places large orders to impact market direction."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # Place a large bid to push the market in a certain direction
        quantity = np.random.randint(20, 50)  # Large quantity for impact
        if self.model.asks:
            best_ask = min(self.model.asks, key=lambda x: x.price).price
            sumo_order = Order(order_type="buy", price=best_ask, quantity=quantity)
            self.model.bids.append(sumo_order)
            #print(f"Sumo Agent {self.unique_id} placed an aggressive buy order at Price={best_ask}, Quantity={quantity}")
