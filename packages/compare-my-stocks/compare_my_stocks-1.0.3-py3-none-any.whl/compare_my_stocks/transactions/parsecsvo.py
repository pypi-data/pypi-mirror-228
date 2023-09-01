import csv
from datetime import datetime
from decimal import Decimal
from typing import List
from enum import Enum, unique
from dataclasses import dataclass

@dataclass(frozen=True)
class Trade:
    transactionType: str
    currency: str
    fxRateToBase: Decimal
    symbol: str
    strike: str
    expiry: str
    putCall: str
    tradeDate: datetime
    quantity: Decimal
    tradePrice: Decimal
    cost: Decimal
    fifoPnlRealized: Decimal
    fxPnl: Decimal
    buySell: BuySell

@unique
class BuySellEnum(Enum):
    BUY = "BUY"
    CANCELBUY = "BUY (Ca.)"
    SELL = "SELL"
    CANCELSELL = "SELL (Ca.)"

def parse_trade(row: List[str]) -> Trade:
    dt_format = "%Y%m%d"
    return Trade(
        transactionType="",
        currency=row[0],
        fxRateToBase=Decimal(row[1]),
        symbol=row[2],
        strike=row[3],
        expiry=row[4],
        putCall=row[5],
        tradeDate=datetime.strptime(row[6], dt_format),
        quantity=Decimal(row[7]),
        tradePrice=Decimal(row[8]),
        cost=Decimal(row[9]),
        fifoPnlRealized=Decimal(row[10]),
        fxPnl=Decimal(row[11]),
        buySell=BuySellEnum(row[12])
    )

with open("trades.csv") as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    trades = [parse_trade(row) for row in reader]
