from time import sleep
from datetime import datetime, timedelta
import pandas as pd

from .dwx_client import dwx_client
from .Base import Base
from ..tg_send import tg_send
import math


class Trader(Base):
    def __init__(
        self,
        config=None,
        account=None,
        strategy=None,
    ):
        conf = get_config(config, account)
        self.conf = conf
        self.strategy = strategy
        self.size = conf["default_lot_size"]

        self.assets = conf["assets"]
        self.data = {}
        self.completed_initial_load = False

        self.dwx = dwx_client(
            self,
            conf["MT5_directory_path"],
            0.005,  # sleep_delay
            10,  # max_retry_command_seconds
            verbose=False,
        )

        sleep(1)
        self.dwx.start()

        # Second sleep is needed to give it time to reload the keys
        sleep(1)

        if len(self.dwx.account_info.keys()) == 0:
            self.log("No account information found. Check your MT5 client.")

        print("Account info:", self.dwx.account_info)
        self.dwx.subscribe_symbols_bar_data(self.assets)

        print("Default lot size is: ", self.size)

        if self.test:
            self.test()

    # ====================================================== #
    # logging                                                #
    # ====================================================== #
    def log(self, msg):
        print(msg)
        tg_send(msg, self.conf)

    # ====================================================== #
    # DWX Client Callbacks                                   #
    # ====================================================== #
    def request_all_ohlc(self):
        for asset in self.assets:
            self.request_historical_ohlc(asset)

    def request_historical_ohlc(self, asset):
        end = datetime.now()
        start = end - timedelta(days=5)  # last 30 days
        self.dwx.get_historic_data(
            asset[0], asset[1], start.timestamp(), end.timestamp()
        )

    def has_position(self, symbol, direction):
        df = pd.DataFrame.from_dict(self.dwx.open_orders, orient="index")
        if len(df) == 0:
            return False
        df = df[(df["symbol"] == symbol) & (df["type"] == direction)]
        return len(df) > 0

    def close_all_pending_orders(self):
        df = pd.DataFrame.from_dict(self.dwx.open_orders, orient="index")
        if len(df) == 0:
            return
        df = df[(df["type"] != "sell") & (df["type"] != "buy")]

        if len(df) > 0:
            for magic in df.index:
                self.dwx.close_order(magic)
                sleep(0.1)
        return df

    def close_pending_orders(self, symbol):
        df = pd.DataFrame.from_dict(self.dwx.open_orders, orient="index")
        if len(df) == 0:
            return

        df = df[
            (df["symbol"] == symbol) & (df["type"] != "sell") & (df["type"] != "buy")
        ]

        if len(df) > 0:
            for magic in df.index:
                self.dwx.close_order(magic)
                sleep(0.1)
        return df

    # ====================================================== #
    # DWX Client Callbacks                                   #
    # ====================================================== #
    # def trading(self, symbol):
    #     # 1. Remove all pending orders
    #     self.close_pending_orders(symbol)
    #
    #     # Generate signal
    #     data = ohlc[-100:]
    #     ind = don.run(data.open, data.high, data.low, data.close, 33, 1)
    #     orders = ind.pending_orders
    #     # =======================
    #
    #     order = orders[-1]
    #     if order > 0:
    #         lots = 1
    #         if self.has_position(symbol, "sell"):
    #             lots = 2
    #         if not self.has_position(symbol, "buy"):
    #             print("PLACING LONGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")
    #             self.dwx.open_order(
    #                 symbol, order_type="buystop", lots=lots, price=order
    #             )
    #     elif order < 0:
    #         lots = 1
    #         if self.has_position(symbol, "buy"):
    #             lots = 2
    #         if not self.has_position(symbol, "sell"):
    #             print("GOING SHOOORRTTTTTTTTTTTTTTTTTTTT")
    #             self.dwx.open_order(
    #                 symbol, order_type="sellstop", lots=lots, price=math.fabs(order)
    #             )
    #     print(orders.index[-1], orders[-1])
    #     print("==========================")
    #     print()
    #     print()

    # ====================================================== #
    #                   DWX Client Callbacks                 #
    # ====================================================== #
    def on_historic_data(self, symbol, time_frame, data):
        # you can also access the historic data via self.dwx.historic_data.
        # print("HIST DATA | ", symbol, time_frame, f"{datetime.now()}")
        data = pd.DataFrame.from_dict(data, orient="index")
        data.index = pd.to_datetime(data.index, format="%Y.%m.%d %H:%M")
        self.data[f"{symbol}-{time_frame}"] = data
        # print(data)

    def on_tick(self, symbol, bid, ask):
        now = datetime.utcnow()

    def on_message(self, message):
        if message["type"] == "ERROR":
            msg = (
                message["type"],
                "|",
                message["error_type"],
                "|",
                message["description"],
            )
            self.log(msg)
        elif message["type"] == "INFO":
            print(message["type"], "|", message["message"])

    def on_bar_data(
        self, symbol, time_frame, time, open_price, high, low, close_price, tick_volume
    ):
        print("==================================")
        print("NEW BAR | ", symbol, time_frame, datetime.utcnow(), time)
        name = f"{symbol}-{time_frame}"

        # In case this is NOT the first run
        if name in self.data.keys():
            newdf = pd.DataFrame(
                {
                    "open": open_price,
                    "high": high,
                    "low": low,
                    "close": close_price,
                    "tick_volume": tick_volume,
                },
                index=[time],
            )
            self.data[name] = pd.concat([self.data[name], newdf])
            self.trading(symbol, time_frame)

        # Update self data from historical
        self.request_historical_ohlc([symbol, time_frame])

    def on_order_event(self):
        print(f"on_order_event. open_orders: {len(self.dwx.open_orders)} open orders")


# MT5_files_dir = "../dev_Metatrader/MQL5/Files/"

# import os
#
# directory = MT5_files_dir + "DWX"
# for filename in os.listdir(directory):
#     file_path = os.path.join(directory, filename)
#     if os.path.isfile(file_path):
#         os.remove(file_path)
#     else:
#         print("cant' find")

# processor = tick_processor(MT5_files_dir)
# processor.close_all_pending_orders()


#
# #
# # processor.request_ohlc()
# # processor.dwx.historic_data
# #
# # pd.DataFrame.from_dict(processor.dwx.historic_data, orient="index")
#
#
# # end = datetime.utcnow()
# # start = end - timedelta(days=1)  # last 30 days
# # print(start, end)
# while processor.dwx.ACTIVE:
#     sleep(1)
