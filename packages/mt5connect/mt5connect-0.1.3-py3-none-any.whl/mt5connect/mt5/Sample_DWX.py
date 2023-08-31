from datetime import datetime, timedelta
import pandas as pd
import json

from .Base import Base


class Sample_DWX(Base):
    def __init__(self, USER, inform=True, should_update_equity=False, min_days=3):
        super().__init__(
            USER,
            inform=inform,
            should_update_equity=should_update_equity,
            min_days=min_days,
        )

    # ====================================================== #
    # DWX Client Callbacks                                   #
    # ====================================================== #

    def event_new_bar(self, symbol, timeframe, data):
        print()
        print("New Bar Data fetched")
        print(symbol, timeframe)
        print(data)
