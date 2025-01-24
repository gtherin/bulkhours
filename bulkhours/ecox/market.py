import pandas as pd
import numpy as np
from .lob import OrderBook
from . import agents

known_agents = {
   "Buyer": agents.Buyer,
   "Seller": agents.Buyer,
   "MarketMaker": agents.Buyer,
   "SniperAgent": agents.Buyer,
}


class Market1(agents.Model):
    """A simple stock market model with buyers, sellers, and a market maker."""
    def __init__(self, num_buyers, num_sellers, num_market_makers=1):
        super().__init__()
        self.num_buyers = num_buyers
        self.num_sellers = num_sellers
        self.num_market_makers = num_market_makers

        # Order books for bids and asks
        self.bids = []  # List of buy orders
        self.asks = []  # List of sell orders

        # Create buyer and seller agents
        for i in range(self.num_buyers):
            buyer = agents.Buyer(i, self)
            self.schedule.add(buyer)

        for i in range(self.num_sellers):
            seller = agents.Seller(i + self.num_buyers, self)
            self.schedule.add(seller)

        # Create market maker agents
        for i in range(self.num_market_makers):
            market_maker = agents.MarketMaker(i + self.num_buyers + self.num_sellers, self)
            self.schedule.add(market_maker)

        # Create sniper agents
        self.num_snipers = 1
        for i in range(self.num_snipers):
            sniper = agents.SniperAgent(i + self.num_buyers + self.num_sellers + self.num_market_makers, self)
            self.schedule.add(sniper)

        # Data collector to record the state of the order book at each step
        self.datacollector = agents.DataCollector(
            model_reporters={"Order Book": self.collect_order_book}
        )

    def step(self):
        """Advance the model by one step."""
        self.datacollector.collect(self)
        self.schedule.step()
        self.match_orders()  # Match buy and sell orders after each step

    def match_orders(self):
        """Match buy and sell orders if the bid >= ask."""
        self.bids.sort(key=lambda x: x.price, reverse=True)  # Highest price first
        self.asks.sort(key=lambda x: x.price)  # Lowest price first

        while self.bids and self.asks and self.bids[0].price >= self.asks[0].price:
            # Match the highest bid with the lowest ask
            bid = self.bids.pop(0)
            ask = self.asks.pop(0)

            # Execute the trade at the ask price
            trade_price = ask.price
            trade_quantity = min(bid.quantity, ask.quantity)

            # Adjust quantities if partial trade
            bid.quantity -= trade_quantity
            ask.quantity -= trade_quantity

            if bid.quantity > 0:
                self.bids.insert(0, bid)  # Put the remaining part of the bid back

            if ask.quantity > 0:
                self.asks.insert(0, ask)  # Put the remaining part of the ask back

            print(f"Trade executed: Price={trade_price}, Quantity={trade_quantity}")

    def collect_order_book(self):
        """Collect the current state of the order book (bids and asks)."""
        bid_orders = [(order.price, order.quantity) for order in self.bids]
        ask_orders = [(order.price, order.quantity) for order in self.asks]
        return {"bids": bid_orders, "asks": ask_orders}


class Market(agents.Model):
    def __init__(self, lob=None, seed=None):
        super().__init__(seed=seed)
        self.lob = OrderBook() if lob is None else lob
        self.num_agents = 0

    def get_name(self, agent):
        return type(agent).__name__ + str(agent.unique_id)

    def init_collector(self):
        self.mid_price, self.spread = self.lob.get_mid_price_and_spread()
        model_reporters = {"mid_price": lambda m: self.mid_price, "spread": lambda m: self.spread}
        model_reporters.update({self.get_name(a): lambda m: a.wanted_position for a in self.agents})
        self.datacollector = agents.DataCollector(model_reporters=model_reporters)

    def lob_snapshot(self):
        self.mid_price, self.spread = self.lob.get_mid_price_and_spread()

    def trade_round(self):
        self.lob_snapshot()
        self.datacollector.collect(self)
        self.agents.shuffle_do("trade_round")
        # self.agents.do("trade_round")

    def create_agents(self, agent_class, n=1):

        if type(agent_class) == str:
            agent_class = known_agents[agent_class]

        # Create n agents
        agent_class.create_agents(model=self, n=n)
        self.num_agents += n

        # Init data collector to record the state of the order book at each step
        self.init_collector()
