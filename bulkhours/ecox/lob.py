import matplotlib.pyplot as plt
import pandas as pd
import heapq
import numpy as np                             # Python basic data science library
import pandas as pd                            # Python standard data science library


class OrderBook:
    def __init__(self):
        # Using heaps for bids and asks (priority queues)
        self.bids = []  # Max-heap for bids (negate prices for max-heap behavior)
        self.asks = []  # Min-heap for asks
        self.trade_history = []  # Store trade executions

    def place_limit_order(self, side, price, quantity):
        """Place a limit order in the order book."""
        if side == "bid":
            heapq.heappush(self.bids, (-price, quantity))  # Max-heap for bids
        elif side == "ask":
            heapq.heappush(self.asks, (price, quantity))  # Min-heap for asks
        self.match_orders()

    def place_order(self, traderid, ordertype, quantity, price_level=-1, verbose=False):
        if ordertype == 'BID_MKT_ORDER':
            self.place_market_order('bid', quantity)
        elif ordertype == 'ASK_MKT_ORDER':
            self.place_market_order('ask', quantity)
        elif ordertype == 'BID_LMT_ORDER':
            self.place_limit_order('bid', price_level, quantity)
        elif ordertype == 'ASK_LMT_ORDER':
            self.place_limit_order('ask', price_level, quantity)
        elif ordertype == 'BID_CCL_ORDER':
            self.cancel_order('bid', price_level, quantity)
        elif ordertype == 'ASK_CCL_ORDER':
            self.cancel_order('ask', price_level, quantity)
        if verbose:
            print(f"'{traderid}' order {quantity}@{price_level} on side {ordertype} {self.get_best_bid()} {self.get_best_ask()}") 

    def place_market_order(self, side, quantity):
        """Place a market order, matching with the best available prices."""
        if side == "bid":
            self.match_market_order(self.asks, quantity, "ask")
        elif side == "ask":
            self.match_market_order(self.bids, quantity, "bid")

    def cancel_order(self, side, price, quantity):
        """Cancel a specific quantity of a limit order at a given price."""
        if side == "bid":
            self.bids = self._cancel_from_heap(self.bids, -price, quantity)
        elif side == "ask":
            self.asks = self._cancel_from_heap(self.asks, price, quantity)

    def _cancel_from_heap(self, heap, target_price, quantity):
        """Helper function to cancel an order from a heap."""
        new_heap = []
        for price, qty in heap:
            if price == target_price:
                qty -= quantity
                if qty > 0:
                    new_heap.append((price, qty))
            else:
                new_heap.append((price, qty))
        heapq.heapify(new_heap)
        return new_heap
    
    def match_orders(self):
        """Match limit orders in the book."""
        while self.bids and self.asks:
            bid_price, bid_qty = -self.bids[0][0], self.bids[0][1]
            ask_price, ask_qty = self.asks[0][0], self.asks[0][1]

            if bid_price >= ask_price:
                trade_qty = min(bid_qty, ask_qty)
                self.trade_history.append((ask_price, trade_qty))

                # Update or remove the top bid
                if bid_qty > trade_qty:
                    self.bids[0] = (-bid_price, bid_qty - trade_qty)
                    heapq.heapify(self.bids)
                else:
                    heapq.heappop(self.bids)

                # Update or remove the top ask
                if ask_qty > trade_qty:
                    self.asks[0] = (ask_price, ask_qty - trade_qty)
                    heapq.heapify(self.asks)
                else:
                    heapq.heappop(self.asks)
            else:
                break

    def match_market_order(self, opposite_book, quantity, opposite_side):
        """Match a market order with the opposite side of the book."""
        while quantity > 0 and opposite_book:
            best_price, best_qty = opposite_book[0]

            trade_qty = min(quantity, best_qty)
            self.trade_history.append((best_price, trade_qty))

            # Update or remove the top order
            if best_qty > trade_qty:
                opposite_book[0] = (best_price, best_qty - trade_qty)
                heapq.heapify(opposite_book)
            else:
                heapq.heappop(opposite_book)

            quantity -= trade_qty

        if quantity > 0:
            print(f"Market order of {quantity} {opposite_side} could not be fully filled.")

    def get_order_book_as_dataframe(self):
        """Retrieve the order book as a pandas DataFrame."""
        bids_df = pd.DataFrame(
            [(-price, quantity) for price, quantity in self.bids],
            columns=["Price", "Quantity"]
        ).sort_values(by="Price", ascending=False)

        asks_df = pd.DataFrame(
            [(price, quantity) for price, quantity in self.asks],
            columns=["Price", "Quantity"]
        ).sort_values(by="Price", ascending=True)

        return bids_df, asks_df

    def get_trade_history(self):
        """Retrieve the trade history as a pandas DataFrame."""
        return pd.DataFrame(self.trade_history, columns=["Price", "Quantity"])

    def get_mid_price_and_spread(self):
        """Calculate and return the mid-price and spread."""
        if self.bids and self.asks:
            best_bid = -self.bids[0][0]  # Highest bid
            best_ask = self.asks[0][0]  # Lowest ask
            mid_price = (best_bid + best_ask) / 2
            spread = best_ask - best_bid
            return mid_price, spread
        return None, None  # If either side is empty

    def add_lobdata(self, nlobdata):
        # Plot bids

        nlobdata["price"] = nlobdata["price"].round(1)
        self.lobdata["price"] = self.lobdata["price"].round(1)

        if "bid_new" in self.lobdata.columns:
            del self.lobdata["bid_new"]
        if "ask_new" in self.lobdata.columns:
            del self.lobdata["ask_new"]

        self.lobdata = self.lobdata.merge(nlobdata, on="price", how="outer", suffixes=("", "_new")).fillna(0)

        p = self.ax.bar(self.lobdata["price"], self.lobdata["bid_new"], bottom=self.lobdata["bid"], color='#52DE97', edgecolor='black', label="Waiting limit Bid Orders", width=0.08)
        self.ax.bar_label(p, labels=[str(self.counter) if self.lobdata["bid_new"][e]!= 0.0 else "" for e in self.lobdata.index], label_type='center', color="white")
        p = self.ax.bar(self.lobdata["price"], self.lobdata["ask_new"], bottom=self.lobdata["ask"], color='#C70039', edgecolor='black', label="Waiting limit Ask Orders", width=0.08)
        self.ax.bar_label(p, labels=[str(self.counter) if self.lobdata["ask_new"][e]!= 0.0 else "" for e in self.lobdata.index], label_type='center', color="white")

        self.lobdata["bid"] = self.lobdata["bid_new"]
        self.lobdata["ask"] = self.lobdata["ask_new"]
        self.counter += 1

    def get_best_bid(self):
        return -self.bids[0][0]

    def get_best_ask(self):
        return self.asks[0][0]

    def get_mid_price(self):
        return (self.get_best_bid() + self.get_best_ask()) / 2

    def get_spread(self):
        return self.get_best_ask() - self.get_best_bid()

    def plot(self, width=1) -> None:
        # Plot the order book
        bids_df, asks_df = self.get_order_book_as_dataframe()
        self.width = width

        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot bids
        ax.bar(bids_df["Price"], bids_df["Quantity"], color='#52DE97', edgecolor='black', label="Waiting limit Bid Orders", width=self.width)

        # Plot asks
        ax.bar(asks_df["Price"], asks_df["Quantity"], color='#C70039', edgecolor='black', label="Waiting limit Ask Orders", width=self.width)

        # Customize the plot
        ax.axhline(0, color='black', linestyle='--', linewidth=0.5)  # Separate bid and ask sides
        ax.set_ylabel("Volume available", fontsize=12)
        ax.set_xlabel("Price", fontsize=12)
        ax.set_title("Limit Order Book", fontsize=14)
        ax.legend(loc=1)
        ax.grid(True, color='lightgray', linestyle='--', linewidth=0.5)
        self.ax = ax

    def add_plot_spread(self, y=None):
        if y is None:
            y = 8
        mid_price, spread = self.get_mid_price_and_spread()
        best_bid = -self.bids[0][0]  # Highest bid
        best_ask = self.asks[0][0]  # Lowest ask

        plt.text(x=best_bid, y=self.bids[0][1]+0.5, s='bid', color='#52DE97', ha='center', fontweight='bold')

        plt.text(x=best_ask, y=self.asks[0][1]+0.5, s='ask', color='#C70039', ha='center', fontweight='bold')

        plt.text(x=mid_price, y=y+0.5, s='spread', ha='center', fontweight='bold')
        plt.annotate('', xy=(best_bid, y), xytext=(best_ask, y), arrowprops=dict(arrowstyle='<|-|>'))

        #plt.text(x=104.5, y=9.3, s='tick', ha='center', fontweight='bold')
        #plt.annotate('', xy=(104, 9), xytext=(105, 9), arrowprops=dict(arrowstyle='<|-|>'))

    def add_plot_mid(self, y=None):
        if y is None:
            y = 8
        mid_price, spread = self.get_mid_price_and_spread()
        plt.text(x=mid_price-0.03, y=y, s='mid', ha='center', color="gray", fontweight='bold', rotation=90)
        plt.axvline(mid_price, color='lightgray', linestyle='--', linewidth=2)

    def add_plot_order(self, price, size, rbottom=50, ttype="BID_LMT_ORDER"):
        ax = self.ax
        color = '#52DE97' if "BID" in ttype else '#C70039'
        arrowstyle = '-|>' if "LMT" in ttype else '<|-'
        labels = {"BID_LMT_ORDER": "New limit order", "BID_MKT_ORDER": "New market order", "BID_CCL_ORDER": "Cancellation",
                  "ASK_LMT_ORDER": "New limit order", "ASK_MKT_ORDER": "New market order", "ASK_CCL_ORDER": "Cancellation"}
        label = labels[ttype]
        width = self.width

        bids_df, asks_df = self.get_order_book_as_dataframe()
        lobdata = bids_df if "BID" in ttype else asks_df

        bottoms = lobdata[np.abs(lobdata['Price']-price)<1e-4].copy()
        if bottoms.empty:
            abottom = 0
        else:
            abottom = bottoms.bid.iloc[0] if "BID" in ttype else bottoms.ask.iloc[0]

        bottom = abottom + rbottom

        if "CCL" in ttype:
            ax.bar([price], [size], bottom=abottom, color=color, alpha=0.2, edgecolor='gray', width=self.width, hatch="///")
            plt.annotate('', xy=(price, abottom+size), xytext=(price, bottom), arrowprops=dict(arrowstyle=arrowstyle))
            plt.text(x=price, y=bottom+5, s=label, ha='center')
        elif "MKT" in ttype:
            ax.bar([price], [size], bottom=abottom, color=color, alpha=0.2, edgecolor='gray', width=self.width, hatch="///")
            ax.bar([price], [size], bottom=bottom, color=color, alpha=0.4, edgecolor='black', width=self.width)
            plt.annotate('', xy=(price, abottom+size), xytext=(price, bottom), arrowprops=dict(arrowstyle=arrowstyle))
            plt.text(x=price, y=bottom+size+5, s=label, ha='center')
        else:
            ax.bar([price], [size], bottom=bottom, color=color, alpha=0.2, edgecolor='black', width=self.width, hatch="///")
            ax.bar([price], [size], bottom=abottom, color=color, alpha=0.4, edgecolor='black', width=self.width)
            plt.annotate('', xy=(price, abottom+size), xytext=(price, bottom), arrowprops=dict(arrowstyle=arrowstyle))
            plt.text(x=price, y=bottom+size+5, s=label, ha='center')