import pandas as pd
import numpy as np
from .lob import OrderBook

try:
    from mesa import Agent, Model
    from mesa.datacollection import DataCollector

except ImportError:
    class Agent:
        def __init__(self, unique_id, model):
            print("mesa is not available. Using dummy class.")

    class Model:
        def __init__(self, *args, **kwargs):
            print("mesa is not available. Using dummy class.")        

    class DataCollector:
        def __init__(self, *args, **kwargs):
            print("mesa is not available. Using dummy class.")        


class TradingAgent(Agent):
    def __init__(self, model, hit_rate=1, max_position=500, max_trade=20, order_duration=None):
        super().__init__(model)
        self.position, self.wanted_position = 0., 0.
        self.max_position, self.max_trade = max_position, max_trade
        self.hit_rate, self.order_duration = hit_rate, order_duration
        self.unique_name = type(self).__name__ + str(self.unique_id)

    def heads_or_tails(self, heads_bias=None):
        if heads_bias is not None:
            return np.random.random() < heads_bias
        return np.random.choice([True, False])

    def send_order(self, quantity, price_info, verbose=False, quiet=True):
        if quantity > 0: # You want to buy
            if type(price_info) in [float, int]:
                self.model.lob.place_order(self.unique_name, "BID_LMT_ORDER", quantity, price_level=float(price_info), verbose=verbose, quiet=quiet)
            elif "BID" in price_info:
                price_level = self.model.mid_price - int(price_info[3:]) * self.model.spread
                self.model.lob.place_order(self.unique_name, "BID_LMT_ORDER", quantity, price_level=price_level, verbose=verbose, quiet=quiet)
            else:
                self.model.lob.place_order(self.unique_name, "ASK_MKT_ORDER", quantity, verbose=verbose, quiet=quiet)
        elif quantity < 0: # You want to sell
            if type(price_info) in [float, int]:
                self.model.lob.place_order(self.unique_name, "ASK_LMT_ORDER", -quantity, price_level=float(price_info), verbose=verbose, quiet=quiet)
            elif "ASK" in price_info:
                price_level = self.model.mid_price + int(price_info[3:]) * self.model.spread
                self.model.lob.place_order(self.unique_name, "ASK_LMT_ORDER", -quantity, price_level=price_level, verbose=verbose, quiet=quiet)
            else:
                self.model.lob.place_order(self.unique_name, "BID_MKT_ORDER", -quantity, verbose=verbose, quiet=quiet)

    def place_order(self, order_type, quantity, price_level=None, verbose=False, quiet=True):
        self.model.lob.place_order(self.unique_name, order_type, quantity, price_level=price_level, verbose=verbose, quiet=quiet)

    def trade_round(self):
        # Trade hit_rate% of time
        if np.random.random() < self.hit_rate: return

        # Update trader info
        self.trade_round()

        # Fundamental value increase with time
        self.position = self.wanted_position

        # Delete old trades
        if self.order_duration is not None:
            old_trades = self.market.lob.data[(self.market.lob.data["TraderID"] == self.unique_name) & (self.market.lob.order_counter-self.market.lob.data["EventTime"] > self.order_duration)]
            self.market.lob.data.drop(old_trades.index, inplace=True)


class FundamentalAgent(TradingAgent):
    """Wants to go back to a fundamental value"""
    def __init__(self, model, fundamental_price=4, long_term_drift=0.1, **kwargs):
        super().__init__(model, **kwargs)
        self.fundamental_price = fundamental_price
        self.long_term_drift = long_term_drift

    def trade_round(self):
        # Fundamental value increase with time
        self.fundamental_price += self.long_term_drift + np.random.normal(self.model.mid_price, 0.1)

        # Fundamental value increase with time
        self.wanted_position = self.fundamental_price - self.model.mid_price

        # Trade signal
        self.place_order('MKT_ORDER', self.wanted_position-self.position)


class BuyerAgent(TradingAgent):
    def trade_round(self):
        # Fundamental value increase with time
        self.wanted_position = min(self.max_position - self.position, self.max_trade)
        if self.heads_or_tails():
            self.send_order(self.wanted_position-self.position, "BID1", quiet=True)
        else:
            self.send_order(self.wanted_position-self.position, "ASK1", quiet=True)

class SellerAgent(TradingAgent):
    def trade_round(self):
        # Fundamental value increase with time
        self.wanted_position = -min(self.max_position + self.position, self.max_trade)
        if self.heads_or_tails():
            self.send_order(self.wanted_position-self.position, "ASK1", quiet=True)
        else:
            self.send_order(self.wanted_position-self.position, "BID1", quiet=True)

class RandomAgent(TradingAgent):
    def trade_round(self):
        # Get random trade
        random_trade_2_cancel = self.model.lob.data.sample()

        # Drop random trade
        self.model.lob.data.drop(random_trade_2_cancel.index, inplace=True)

        # 
        side = random_trade_2_cancel.Side.iloc[0]
        self.place_order("BID_LMT_ORDER" if side == "bid" else "ASK_LMT_ORDER", 
                               int(np.random.uniform(5, 15)),
                               round(self.model.mid_price + (-1 if side == "bid" else 1) * np.random.choice([1, 2, 3]) * self.model.spread, 0))

class BuyerAgent(TradingAgent):
    def trade_round(self):
        # Fundamental value increase with time
        self.wanted_position = min(self.max_position - self.position, self.max_trade)
        if self.heads_or_tails():
            self.send_order(self.wanted_position-self.position, "BID1")
        else:
            self.send_order(self.wanted_position-self.position, "ASK1")

class SellerAgent(TradingAgent):
    def trade_round(self):
        # Fundamental value increase with time
        self.wanted_position = -min(self.max_position + self.position, self.max_trade)
        if self.heads_or_tails():
            self.send_order(self.wanted_position-self.position, "ASK1")
        else:
            self.send_order(self.wanted_position-self.position, "BID1")


class TrendingAgent(TradingAgent):
    def __init__(self, model, trend_force=100, **kwargs):
        super().__init__(model, **kwargs)
        self.trend_force = trend_force

    def trade_round(self):
        # Fundamental value increase with time
        if self.model.mid_price is None or self.model.prev_mid_price is None:
            return

        predictor = 10*(self.model.mid_price - self.model.prev_mid_price)
        self.wanted_position = 20 if predictor > 0 else -20

        # Trade signal
        self.place_order('MKT_ORDER', self.wanted_position-self.position, quiet=True)


class MarketMaker(TradingAgent):
    def __init__(self, model, spread=0.5, **kwargs):
        super().__init__(model, **kwargs)
        self.position, self.wanted_position = 0., 0.
        self.spread = spread
        self.min_qty = 15

    def trade_round(self):
        qtys = self.model.lob.data[self.model.lob.data["TraderID"] == self.unique_name].groupby("Side")["Quantity"].sum()
        bid_volume = qtys["bid"] if "bid" in qtys.index else 0
        if bid_volume < self.min_qty:
            qty = np.random.choice(range(10, 20))
            for l in range(1, 10):
                self.place_order('BID_LMT_ORDER', qty, self.model.mid_price-l*self.spread, verbose=False)

        ask_volume = qtys["ask"] if "ask" in qtys.index else 0
        if ask_volume < self.min_qty:
            qty = np.random.choice(range(10, 20))
            for l in range(1, 10):
                self.place_order('ASK_LMT_ORDER', qty, self.model.mid_price+l*self.spread, verbose=False)


class Order:
    """Represents a single order (buy or sell) in the order book."""
    def __init__(self, order_type, price, quantity):
        self.order_type = order_type  # 'buy' or 'sell'
        self.price = price
        self.quantity = quantity



class SniperAgent(TradingAgent):
    """A sniper agent waits for favorable market conditions and places large orders opportunistically."""
    def trade_round(self):
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


class GuerillaAgent(TradingAgent):
    """A guerilla agent breaks large orders into smaller chunks and executes them stealthily."""
    def __init__(self, model, **kwargs):
        super().__init__(model, **kwargs)
        self.remaining_quantity = np.random.randint(20, 50)  # Initial large order quantity

    def trade_round(self):
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


class BlastAgent(TradingAgent):
    """A blast agent places a large order all at once, impacting the market."""
    def trade_round(self):
        # Place a large buy order with significant quantity at the best ask price
        quantity = np.random.randint(50, 100)
        if self.model.asks:
            best_ask = min(self.model.asks, key=lambda x: x.price).price
            blast_order = Order(order_type="buy", price=best_ask, quantity=quantity)
            self.model.bids.append(blast_order)
            #print(f"Blast Agent {self.unique_id} placed a large buy order at Price={best_ask}, Quantity={quantity}")


class IcebergAgent(TradingAgent):
    """An iceberg agent hides part of a large order by placing smaller chunks over time."""
    def __init__(self, model, **kwargs):
        super().__init__(model, **kwargs)
        self.remaining_quantity = np.random.randint(100, 200)  # Large initial order size
        self.visible_chunk_size = 10  # Size of each visible portion of the order

    def trade_round(self):
        if self.remaining_quantity > 0:
            chunk_size = min(self.visible_chunk_size, self.remaining_quantity)
            self.remaining_quantity -= chunk_size
            if self.model.asks:
                best_ask = min(self.model.asks, key=lambda x: x.price).price
                iceberg_order = Order(order_type="buy", price=best_ask, quantity=chunk_size)
                self.model.bids.append(iceberg_order)
                #print(f"Iceberg Agent {self.unique_id} placed a chunk buy order at Price={best_ask}, Quantity={chunk_size}")


class SharkAgent(TradingAgent):
    """A shark agent detects large orders and trades around them to profit."""
    def trade_round(self):
        # Detect if there are large orders in the order book
        large_orders = [order for order in self.model.bids if order.quantity > 20]
        if large_orders:
            target_order = large_orders[0]  # Target the first large order
            # Place a sell order slightly above the large order price
            shark_price = target_order.price * 1.01  # Slightly above the large order price
            shark_order = Order(order_type="sell", price=shark_price, quantity=5)
            self.model.asks.append(shark_order)
            #print(f"Shark Agent {self.unique_id} placed a sell order at Price={shark_price}, Quantity=5")


class StealthAgent(TradingAgent):
    """A stealth agent executes small trades at random intervals to avoid detection."""
    def trade_round(self):
        # Randomly decide if the agent should trade in this step
        if np.random.rand() < 0.5:  # 50% chance to place an order
            quantity = np.random.randint(1, 3)  # Small quantity for stealth
            if self.model.asks:
                best_ask = min(self.model.asks, key=lambda x: x.price).price
                stealth_order = Order(order_type="buy", price=best_ask, quantity=quantity)
                self.model.bids.append(stealth_order)
                #print(f"Stealth Agent {self.unique_id} placed a small buy order at Price={best_ask}, Quantity={quantity}")


class SumoAgent(TradingAgent):
    """A sumo agent aggressively places large orders to impact market direction."""
    def trade_round(self):
        # Place a large bid to push the market in a certain direction
        quantity = np.random.randint(20, 50)  # Large quantity for impact
        if self.model.asks:
            best_ask = min(self.model.asks, key=lambda x: x.price).price
            sumo_order = Order(order_type="buy", price=best_ask, quantity=quantity)
            self.model.bids.append(sumo_order)
            #print(f"Sumo Agent {self.unique_id} placed an aggressive buy order at Price={best_ask}, Quantity={quantity}")

# Function to generate a random process
def generate_poisson_process(rate, duration, value=True):
    time_intervals = np.arange(0, duration, 1)

    event_counts = np.random.poisson(rate, size=len(time_intervals))
    event_times = []
    for t, count in zip(time_intervals, event_counts):
        event_times.extend(np.random.uniform(t, t + 1, size=count))  # Distribute events randomly within the interval

    return pd.Series(value, index=np.sort(event_times))


def update_santafe_lob(lob, df, frame, ref_price=100):
    layer, order = df.iloc[frame].split("_")
    pside = "BID_" if int(layer) < 0 else "ASK_"
    oside = "ASK_" if int(layer) < 0 else "BID_"
    if order == "Limit":
        lob.place_order("guy", f"{pside}LMT_ORDER", 1, int(layer)+ref_price, verbose=True)
    elif order == "Cancel":
        lob.place_order("guy", f"{pside}CCL_ORDER", 1, int(layer)+ref_price, verbose=True)
    elif order == "Market":
        lob.place_order("guy", f"{oside}MKT_ORDER", 1, verbose=True)
