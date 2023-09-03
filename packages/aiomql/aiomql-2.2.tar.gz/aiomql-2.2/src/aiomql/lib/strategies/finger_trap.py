import asyncio
import logging
from typing import Literal
from dataclasses import dataclass

from ..traders.simple_deal_trader import DealTrader
from ... import Symbol
from ...strategy import Strategy
from ...core.constants import TimeFrame, OrderType
from ...candle import Candle, Candles

logger = logging.getLogger(__name__)


@dataclass
class Entry:
    """
    Entry class for FingerTrap strategy.Will be used to store entry conditions and other entry related data.

    Attributes:
        bearish (bool): True if the market is bearish
        bullish (bool): True if the market is bullish
        ranging (bool): True if the market is ranging
        snooze (float): Time to wait before checking for entry conditions
        trend (str): The current trend of the market
        last_candle (Candle): The last candle of the market
        new (bool): True if the last candle is new
        order_type (OrderType): The type of order to place
        pips (int): The number of pips to place the order from the current price
    """
    bearish: bool = False
    bullish: bool = False
    ranging: bool = True
    snooze: float = 0
    trend: Literal['ranging', 'bullish', 'bearish'] = 'ranging'
    last_candle: Candle = Candle()
    new: bool = True
    order_type: OrderType | None = None
    pips: int = 10

    def update(self, **kwargs):
        fields = self.__dict__
        for key in kwargs:
            if key in fields:
                setattr(self, key, kwargs[key])
        match self.trend:
            case 'ranging':
                self.ranging = True
                self.bullish = False
                self.bearish = False
            case 'bullish':
                self.ranging = False
                self.bullish = True
                self.bearish = False
            case 'bearish':
                self.ranging = False
                self.bullish = False
                self.bearish = True


class FingerTrap(Strategy):
    trend_time_frame: TimeFrame
    entry_time_frame: TimeFrame
    trend: int
    fast_period: int
    slow_period: int
    entry_period: int
    parameters: dict
    prices: Candles
    name = "FingerTrap"
    candles: Candles
    entry_candles: Candles
    def __init__(self, *, symbol: Symbol, params: dict | None = None):
        super().__init__(symbol=symbol, params=params)
        self.trend = self.parameters.get('trend', 3)
        self.fast_period = self.parameters.setdefault('fast_period', 8)
        self.slow_period = self.parameters.setdefault('slow_period', 34)
        self.entry_time_frame = self.parameters.setdefault('entry_time_frame', TimeFrame.H1)
        self.trend_time_frame = self.parameters.setdefault('trend_time_frame', TimeFrame.M5)
        self.trader = DealTrader(symbol=self.symbol)
        self.entry: Entry = Entry(snooze=self.trend_time_frame.time)
        self.entry_period = self.parameters.setdefault('entry_period', 8)
        self.interval = self.parameters.setdefault('interval', )


    async def check_trend(self):
        try:
            self.candles = await self.symbol.copy_rates_from_pos(timeframe=self.trend_time_frame)
            current = self.candles[-1]

            if current > self.entry.last_candle:
                self.entry.update(new=True, last_candle=current)
            else:
                self.entry.update(new=False)
                return

            self.candles.ta.ema(length=self.fast_period, append=True, fillna=0)
            self.candles.ta.ema(length=self.slow_period, append=True, fillna=0)
            cols = {f'EMA_{self.fast_period}': 'fast', f'EMA_{self.slow_period}': 'slow'}
            self.candles.rename(inplace=True, **cols)

            # Compute cross-overs
            fxas = self.candles.ta_lib.cross(self.candles.fast, self.candles.slow)
            fxbs = self.candles.ta_lib.cross(self.candles.fast, self.candles.slow, above=False)
            pxaf = self.candles.ta_lib.cross(self.candles.close, self.candles.fast)
            pxbs = self.candles.ta_lib.cross(self.candles.close, self.candles.slow, above=False)
            self.candles.data[fxas.name] = fxas
            self.candles.data[fxbs.name] = fxbs
            self.candles.data[pxaf.name] = pxaf
            self.candles.data[pxbs.name] = pxbs
            trend = self.candles[-self.trend: -1]

            if all(c for c in trend.fast_XA_slow) and all(c for c in trend.close_XA_fast):
                self.entry.update(trend='bullish')

            elif all(c for c in trend.fast_XB_slow) and all(c for c in trend.close_XB_slow):
                self.entry.update(trend='bearish')
            else:
                self.entry.update(trend='ranging', snooze=self.trend_time_frame.time)
        except Exception as exe:
            logger.error(f'{exe}. Error in {self.__class__.__name__}.check_trend')

    async def confirm_trend(self):
        try:
            self.entry_candles = await self.symbol.copy_rates_from_pos(timeframe=self.entry_time_frame)
            self.entry_candles.ta.ema(length=self.entry_period, append=True, fillna=0)
            self.entry_candles.rename(**{f'EMA_{self.entry_period}': 'ema'})
            pxae = self.entry_candles.ta_lib.cross(self.entry_candles.close, self.entry_candles.ema)
            pxbe = self.entry_candles.ta_lib.cross(self.entry_candles.close, self.entry_candles.ema, above=False)
            self.entry_candles[pxae.name] = pxae
            self.entry_candles[pxbe.name] = pxbe
            if self.entry.bullish and pxae[-1].price_XA_ema:
                self.entry_candles[pxae.name] = pxae
                self.entry.update(snooze=self.interval, order_type=OrderType.BUY)
            elif self.entry.bearish and pxae[-1].price_XB_ema:
                self.entry_candles[pxbe.name] = pxbe
                self.entry.update(snooze=self.interval, order_type=OrderType.SELL)
            else:
                self.entry.update(snooze=self.entry_time_frame.time, order_type=None)
        except Exception as exe:
            logger.error(f'{exe}. Error in {self.__class__.__name__}.confirm_trend')

    async def watch_market(self):
        await self.check_trend()
        if not self.entry.new or self.entry.ranging:
            return
        await self.confirm_trend()

    async def trade(self):
        print(f'Trading {self.symbol}')
        while True:
            try:
                await self.watch_market()
                if not self.entry.new:
                    await asyncio.sleep(0.1)
                    continue

                if self.entry.order_type is None:
                    await self.sleep(self.entry.snooze)
                    continue

                await self.trader.place_trade(order_type=self.entry.order_type, pips=self.entry.pips, params=self.parameters)
                await self.sleep(self.entry.snooze)
            except Exception as err:
                logger.error(f"Error: {err}\t Symbol: {self.symbol} in {self.__class__.__name__}.trade")
                await self.sleep(self.trend_time_frame.time)
                continue
