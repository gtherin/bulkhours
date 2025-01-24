import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time

class OrderBook:
    def __init__(self, price_rounding=1, traders_style={}):
        self.data = pd.DataFrame(columns=["Side", "Price", "Quantity", "TraderID", "EventTime"])
        self.trade_history = []  # Store executed trades
        self.price_rounding = price_rounding
        self.order_counter = 0  # To keep track of order timestamps
        self.traders_style = traders_style

    def round_price(self, price):
        return round(price, self.price_rounding)

    def place_order(self, trader_id, order_type, quantity, price_level=None, verbose=False):
        if order_type == 'MKT_ORDER':
            if quantity > 0:
                self.match_market_order("ask", quantity, trader_id)
            else:
                self.match_market_order("bid", quantity, trader_id)
        elif order_type == 'BID_MKT_ORDER':
            self.match_market_order("bid", quantity, trader_id)
        elif order_type == 'ASK_MKT_ORDER':
            self.match_market_order("ask", quantity, trader_id)
        elif order_type == 'BID_LMT_ORDER':
            self.place_limit_order("bid", self.round_price(price_level), quantity, trader_id)
        elif order_type == 'ASK_LMT_ORDER':
            self.place_limit_order("ask", self.round_price(price_level), quantity, trader_id)
        elif order_type == 'BID_CCL_ORDER':
            self.cancel_order("bid", self.round_price(price_level), quantity, trader_id)
        elif order_type == 'ASK_CCL_ORDER':
            self.cancel_order("ask", self.round_price(price_level), quantity, trader_id)

        if verbose:
            print(f"{trader_id} placed {order_type} for {quantity}@{price_level}")

    def place_limit_order(self, side, price, quantity, trader_id):
        self.order_counter += 1
        new_order = {
            "Side": side,
            "Price": price,
            "Quantity": quantity,
            "TraderID": trader_id,
            "EventTime": self.order_counter
        }
        self.data = pd.concat([self.data, pd.DataFrame([new_order])], ignore_index=True)

    def cancel_order(self, side, price, quantity, trader_id):
        matching_orders = (self.data["Side"] == side) & (self.data["Price"] == price) & (self.data["TraderID"] == trader_id)
        
        for idx in self.data[matching_orders].index:
            if self.data.at[idx, "Quantity"] > quantity:
                self.data.at[idx, "Quantity"] -= quantity
                break
            else:
                quantity -= self.data.at[idx, "Quantity"]
                self.data.drop(idx, inplace=True)

    def match_market_order(self, opposite_side, quantity, trader_id):
        side = "ask" if opposite_side == "bid" else "bid"
        side = opposite_side
        available_orders = self.data[self.data["Side"] == opposite_side].sort_values(by="Price", ascending=(side == "ask"))

        for idx, order in available_orders.iterrows():
            trade_qty = min(quantity, order["Quantity"])
            self.trade_history.append({
                "Price": order["Price"],
                "Quantity": trade_qty,
                "Buyer": trader_id if side == "bid" else order["TraderID"],
                "Seller": trader_id if side == "ask" else order["TraderID"]
            })

            if order["Quantity"] > trade_qty:
                self.data.at[idx, "Quantity"] -= trade_qty
                break
            else:
                quantity -= order["Quantity"]
                self.data.drop(idx, inplace=True)

        if quantity > 0:
            print(f"Market order for {quantity} {side} could not be fully filled.")

    def get_order_book_as_dataframe(self):
        bids = self.data[self.data["Side"] == "bid"].sort_values(by="Price", ascending=False)
        asks = self.data[self.data["Side"] == "ask"].sort_values(by="Price", ascending=True)
        return bids, asks

    def get_trade_history(self):
        return pd.DataFrame(self.trade_history)

    def get_mid_price_and_spread(self):
        bids, asks = self.get_order_book_as_dataframe()
        if not bids.empty and not asks.empty:
            best_bid = bids.iloc[0]["Price"]
            best_ask = asks.iloc[0]["Price"]
            mid_price = (best_bid + best_ask) / 2
            spread = best_ask - best_bid
            return mid_price, spread
        return None, None

    def plot_bars(self, side, dfs, cumsum=False):
        color = "#52DE97" if side == "bid" else "#C70039"

        bottom, label = dfs.groupby("Price")["Quantity"].sum()*0., f"Waiting limit {side.capitalize()} Orders"
        for tradeid, df in dfs.groupby("TraderID"):
            talpha = self.traders_style[tradeid]["alpha"] if tradeid in self.traders_style and "alpha" in self.traders_style[tradeid] else 1
            tcolor = self.traders_style[tradeid][f"{side}_color"] if tradeid in self.traders_style and f"{side}_color" in self.traders_style[tradeid] else color

            qty = df.groupby("Price")["Quantity"].sum()
            if cumsum:
                qty = qty.cumsum()

            qty = qty.reindex(bottom.index, fill_value=0)
            p = self.ax.bar(qty.index, qty, color=tcolor, bottom=bottom, edgecolor='black', label=label, width=self.width, alpha=talpha)

            if tradeid in self.traders_style and "label" in self.traders_style[tradeid]:
                self.ax.bar_label(p, labels=[self.traders_style[tradeid]["label"]]*len(qty.index), label_type='center', color="white")

            bottom, label = bottom.add(qty, fill_value=0), ""

    def plot(self, width=1, ax=None, cumsum=False, title=None, sleep=None, xlim=None, ylim=None) -> None:
        bids, asks = self.get_order_book_as_dataframe()
        self.width = width

        if ax is None:
            fig, self.ax = plt.subplots(figsize=(10, 6))
        else:
            self.ax = ax
            self.ax.cla()

        # Plot bids
        self.plot_bars("bid", bids, cumsum=cumsum)

        # Plot asks
        self.plot_bars("ask", asks, cumsum=cumsum)

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