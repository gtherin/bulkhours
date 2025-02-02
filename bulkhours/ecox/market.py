import pandas as pd
import numpy as np
from .lob import OrderBook
from . import agents as bkXmesa

known_agents = {
   "FundamentalAgent": bkXmesa.FundamentalAgent,
   "BuyerAgent": bkXmesa.BuyerAgent,
   "SellerAgent": bkXmesa.SellerAgent,
   "RandomAgent": bkXmesa.RandomAgent,
   "MarketMaker": bkXmesa.MarketMaker,
   "SniperAgent": bkXmesa.SniperAgent,
   "GuerillaAgent": bkXmesa.GuerillaAgent,
   "BlastAgent": bkXmesa.BlastAgent,
   "IcebergAgent": bkXmesa.IcebergAgent,
   "SharkAgent": bkXmesa.SharkAgent,
   "StealthAgent": bkXmesa.StealthAgent,
   "SumoAgent": bkXmesa.SumoAgent,
}


class Market1(bkXmesa.Model):
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
            buyer = bkXmesa.Buyer(i, self)
            self.schedule.add(buyer)

        for i in range(self.num_sellers):
            seller = bkXmesa.Seller(i + self.num_buyers, self)
            self.schedule.add(seller)

        # Create market maker agents
        for i in range(self.num_market_makers):
            market_maker = bkXmesa.MarketMaker(i + self.num_buyers + self.num_sellers, self)
            self.schedule.add(market_maker)

        # Create sniper agents
        self.num_snipers = 1
        for i in range(self.num_snipers):
            sniper = bkXmesa.SniperAgent(i + self.num_buyers + self.num_sellers + self.num_market_makers, self)
            self.schedule.add(sniper)

        # Data collector to record the state of the order book at each step
        self.datacollector = bkXmesa.DataCollector(
            model_reporters={"Order Book": self.collect_order_book}
        )

    def trade_round(self):
        """Advance the model by one step."""
        self.datacollector.collect(self)
        self.agents.shuffle_do("trade_round")
        # self.agents.do("trade_round")
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


class Market(bkXmesa.Model):

    def __init__(self, lob=None, seed=None, mid_price=100., spread=0.1, pop_volume=None):
        super().__init__(seed=seed)
        self.lob = OrderBook() if lob is None else lob

        self.mid_price100, self.mid_price, self.spread, self.prev_mid_price = mid_price, mid_price, spread, mid_price

        if pop_volume is not None:
            self.lob.place_order("MarketMaker0", "BID_LMT_ORDER", pop_volume // 4, self.mid_price-2*self.spread)
            self.lob.place_order("MarketMaker0", "BID_LMT_ORDER", pop_volume // 4, self.mid_price-self.spread)
            self.lob.place_order("MarketMaker0", "ASK_LMT_ORDER", pop_volume // 4, self.mid_price+self.spread)
            self.lob.place_order("MarketMaker0", "ASK_LMT_ORDER", pop_volume // 4, self.mid_price+2*self.spread)

        self.lob_snapshot()
        self.datacollector = bkXmesa.DataCollector(model_reporters={"mid_price": "mid_price", "spread": "spread"}, 
                                                   agent_reporters={"position": "position", "wanted_position": "wanted_position"}
                                                   )

    def get_name(self, agent):
        return type(agent).__name__ + str(agent.unique_id)

    def lob_snapshot(self):
        mid_price, spread = self.lob.get_mid_price_and_spread()
        if mid_price is not None:
            self.prev_mid_price = self.mid_price
            self.mid_price = mid_price
            self.mid_price100 = mid_price*0.01 + 0.99*self.mid_price100
        if spread is not None:
            self.spread = spread

    def trade_round(self, do_old_snapshot=True, do_lob_snapshot=False):
        if do_old_snapshot:
            self.lob_snapshot()
            self.datacollector.collect(self)
        self.agents.shuffle_do("trade_round")
        # self.agents.do("trade_round")
        self.lob.snapshot(lob=do_lob_snapshot)

    def create_agents(self, agent_class, n=1, **kwargs):
        if type(agent_class) == str:
            agent_class = known_agents[agent_class]

        # Create n agents
        agent_class.create_agents(model=self, n=n, **kwargs)
