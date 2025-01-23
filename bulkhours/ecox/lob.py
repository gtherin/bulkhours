import matplotlib.pyplot as plt
import heapq
import numpy as np                             # Python basic data science library
import pandas as pd                            # Python standard data science library
import datetime
import time


class OrderBook:
    def __init__(self):
        # Using heaps for bids and asks (priority queues)
        self.bids = []  # Max-heap for bids (negate prices for max-heap behavior)
        self.asks = []  # Min-heap for asks
        self.trade_history = []  # Store trade executions
        self.traders_style = {}

    def place_order(self, traderid, ordertype, quantity, price_level=-1, verbose=False):
        if ordertype == 'BID_MKT_ORDER':
            #price_level = self.match_market_order(self.asks, quantity, "ask", traderid)  # Place a market order, matching with the best available prices (opposite)
            price_level = self.match_market_order(self.bids, quantity, "bid", traderid)  # Place a market order, matching with the best available prices (opposite)
            #price_level = self.match_market_order(self.asks, quantity, "ask", traderid)  # Place a market order, matching with the best available prices (opposite)
        elif ordertype == 'ASK_MKT_ORDER':
            price_level = self.match_market_order(self.asks, quantity, "ask", traderid)  # Place a market order, matching with the best available prices (opposite)
            #price_level = self.match_market_order(self.bids, quantity, "bid", traderid)  # Place a market order, matching with the best available prices (opposite)
        elif ordertype == 'BID_LMT_ORDER':
            self.place_limit_order('bid', price_level, quantity, traderid=traderid)
        elif ordertype == 'ASK_LMT_ORDER':
            self.place_limit_order('ask', price_level, quantity, traderid=traderid)
        elif ordertype == 'BID_CCL_ORDER':
            self.cancel_order('bid', price_level, quantity, traderid=traderid)
        elif ordertype == 'ASK_CCL_ORDER':
            self.cancel_order('ask', price_level, quantity, traderid=traderid)
        if verbose:
            print(f"'{traderid}' order {quantity}@{price_level} on side {ordertype} {self.get_best_bid()} {self.get_best_ask()}") 

    def place_limit_order(self, side, price, quantity, traderid="anonymous"):
        """Place a limit order in the order book."""
        if side == "bid":
            heapq.heappush(self.bids, (-price, quantity, traderid))  # Max-heap for bids
        elif side == "ask":
            heapq.heappush(self.asks, (price, quantity, traderid))  # Min-heap for asks
        self.match_orders()

    def cancel_order(self, side, price, quantity, traderid):
        """Cancel a specific quantity of a limit order at a given price."""
        if side == "bid":
            self.bids = self._cancel_from_heap(self.bids, -price, quantity, traderid)
        elif side == "ask":
            self.asks = self._cancel_from_heap(self.asks, price, quantity, traderid)

    def _cancel_from_heap(self, heap, target_price, quantity, traderid):
        """Helper function to cancel an order from a heap."""
        new_heap = []
        for price, qty, tid in heap:
            if price == target_price and tid == traderid:
                qty -= quantity
                if qty > 0:
                    new_heap.append((price, qty, tid))
            else:
                new_heap.append((price, qty, tid))
        heapq.heapify(new_heap)
        return new_heap

    def match_orders(self):
        """Match limit orders in the book."""

        # Sort the opposite book to ensure it is in the correct order
        self.bids.sort(key=lambda x: x[0])  # Sort by ascending price
        self.asks.sort(key=lambda x: x[0])  # Sort by ascending price

        while self.bids and self.asks:
            bid_price, bid_qty, bid_traderid = self.bids[0]
            ask_price, ask_qty, ask_traderid = self.asks[0]

            if -bid_price >= ask_price:
                trade_qty = min(bid_qty, ask_qty)
                self.trade_history.append((ask_price, trade_qty, bid_traderid, ask_traderid))

                # Update or remove the top bid
                if bid_qty > trade_qty:
                    self.bids[0] = (bid_price, bid_qty - trade_qty, bid_traderid)
                    heapq.heapify(self.bids)
                else:
                    heapq.heappop(self.bids)

                # Update or remove the top ask
                if ask_qty > trade_qty:
                    self.asks[0] = (ask_price, ask_qty - trade_qty, ask_traderid)
                    heapq.heapify(self.asks)
                else:
                    heapq.heappop(self.asks)
            else:
                break

    def match_market_order(self, opposite_book, quantity, opposite_side, traderid):
        """Match a market order with the opposite side of the book."""

        # Sort the opposite book to ensure it is in the correct order
        opposite_book.sort(key=lambda x: x[0])  # Sort by ascending price

        sign = -1 if opposite_side == "bid" else 1 

        best_price = np.nan
        while quantity > 0 and opposite_book:
            best_price, best_qty, best_tid = opposite_book[0]

            trade_qty = min(quantity, best_qty)
            self.trade_history.append((sign*best_price, trade_qty, traderid, best_tid))

            # Update or remove the top order
            if best_qty > trade_qty:
                opposite_book[0] = (best_price, best_qty - trade_qty, best_tid)
                heapq.heapify(opposite_book)
            else:
                heapq.heappop(opposite_book)

            quantity -= trade_qty

        if quantity > 0:
            print(f"Market order of {quantity} {opposite_side} could not be fully filled.")
        return sign*best_price

    def get_order_book_as_dataframe(self):
        """Retrieve the order book as a pandas DataFrame."""
        bids_df = pd.DataFrame(
            [(-price, quantity, traderid) for price, quantity, traderid in self.bids],
            columns=["Price", "Quantity", "TraderID"]
        ).sort_values(by="Price", ascending=False)

        asks_df = pd.DataFrame(
            [(price, quantity, traderid) for price, quantity, traderid in self.asks],
            columns=["Price", "Quantity", "TraderID"]
        ).sort_values(by="Price", ascending=True)

        return bids_df, asks_df

    def get_trade_history(self):
        """Retrieve the trade history as a pandas DataFrame."""
        return pd.DataFrame(self.trade_history, columns=["Price", "Quantity", "BidTraderID", "AskTraderID"])

    def get_mid_price_and_spread(self):
        """Calculate and return the mid-price and spread."""
        if self.bids and self.asks:
            best_bid = self.get_best_bid()
            best_ask = self.get_best_ask()
            mid_price = (best_bid + best_ask) / 2
            spread = best_ask - best_bid
            return mid_price, spread
        return None, None  # If either side is empty

    def get_best_bid(self):
        if self.bids:
            return max([-price for price, _, _ in self.bids])  # Correct highest bid
        return -1

    def get_best_ask(self):
        if self.asks:
            return min([price for price, _, _ in self.asks])   # Correct lowest ask
        return -1

    def get_mid_price(self):
        return (self.get_best_bid() + self.get_best_ask()) / 2

    def get_spread(self):
        return self.get_best_ask() - self.get_best_bid()

    def plot_bars(self, side, dfs, cumsum=False):
        color = "#52DE97" if side == "bid" else "#C70039"

        bottom, label = None, f"Waiting limit {side.capitalize()} Orders"
        for tradeid, df in dfs.groupby("TraderID"):
            talpha = self.traders_style[tradeid]["alpha"] if tradeid in self.traders_style and "alpha" in self.traders_style[tradeid] else 1
            tcolor = self.traders_style[tradeid][f"{side}_color"] if tradeid in self.traders_style and f"{side}_color" in self.traders_style[tradeid] else color

            qty = df.groupby("Price")["Quantity"].sum()
            if cumsum:
                qty = qty.cumsum()
            p = self.ax.bar(qty.index, qty, color=tcolor, bottom=bottom, edgecolor='black', label=label, width=self.width, alpha=talpha)

            if tradeid in self.traders_style and "label" in self.traders_style[tradeid]:
                self.ax.bar_label(p, labels=[self.traders_style[tradeid]["label"]]*len(qty.index), label_type='center', color="white")

            if bottom is None:
                bottom, label = 0.*qty, ""
            bottom += qty

    def plot(self, width=1, ax=None, cumsum=False, title=None, sleep=None, xlim=None, ylim=None) -> None:

        # Plot the order book
        bids_df, asks_df = self.get_order_book_as_dataframe()
        self.width = width

        if ax is None:
            fig, self.ax = plt.subplots(figsize=(10, 6))
        else:
            self.ax = ax
            self.ax.cla()

        # Plot bids
        self.plot_bars("bid", bids_df, cumsum=cumsum)

        # Plot asks
        self.plot_bars("ask", asks_df, cumsum=cumsum)

        if xlim is not None:
            self.ax.set_xlim(xlim)
        else:
            # Use slicing to select equidistant rows
            if 0:
                n = 5
                step = len(df) // (n - 1)
                if step > 0:
                    df_equidistant = df.iloc[::step][:n]
                    ax.set_xticks(df_equidistant[xaxis])
                    ax.set_xticklabels(df_equidistant["Price"].round(2))
                    ax.tick_params(axis='x', labelrotation=15)

        if ylim is not None:
            ax.set_ylim(ylim)

        if sleep is not None:
            time.sleep(sleep)

        # Customize the plot
        self.ax.axhline(0, color='black', linestyle='--', linewidth=0.5)  # Separate bid and ask sides
        self.ax.set_ylabel("Volume available", fontsize=12)
        self.ax.set_xlabel("Price", fontsize=12)

        if title is not None:
            now = (datetime.datetime.now() + datetime.timedelta(hours=2)).strftime('%H:%M:%S')
            self.ax.set_title(title.replace("NOW", now)) # "Limit Order Book", fontsize=14

        self.ax.legend(loc=1)
        self.ax.grid(True, color='lightgray', linestyle='--', linewidth=0.5)

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