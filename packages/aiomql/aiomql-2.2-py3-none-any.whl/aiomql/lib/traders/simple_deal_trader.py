import logging
from datetime import datetime

from ...utils import dict_to_string
from ...trader import Trader
from ...core.constants import OrderType, OrderTime

from .trade_result import TradeResult

logger = logging.getLogger()


class DealTrader(Trader):
    """A base class for placing trades based on the number of pips to target"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order.type_time = OrderTime.DAY

    async def create_order(self, order_type: OrderType, pips: float):
        """Using the number of target pips it determines the lot size, stop loss and take profit for the order,
        and updates the order object with the values.

        Args:
            order_type (OrderType): Type of order
            pips (float): Target pips
        """
        amount = await self.ram.amount()
        volume = await self.symbol.compute_volume(amount=amount, pips=pips)
        self.order.volume = volume
        self.order.type = order_type
        await self.set_order_limits(pips=pips)

    async def set_order_limits(self, pips: float):
        """Sets the stop loss and take profit for the order.

        Args:
            pips: Target pips
        """
        pips = pips * self.symbol.pip
        sl, tp = pips, pips * self.ram.risk_to_reward
        tick = await self.symbol.info_tick()
        if self.order.type == OrderType.BUY:
            self.order.sl, self.order.tp = tick.ask - sl, tick.ask + tp
            self.order.price = tick.ask
        else:
            self.order.sl, self.order.tp = tick.bid + sl, tick.bid - tp
            self.order.price = tick.bid

    async def place_trade(self, order_type: OrderType, pips: float, params: dict = None):
        """Places a trade based on the number of points to target. The order is created, checked and sent.
        """
        try:
            await self.create_order(order_type=order_type, pips=pips)
            check = await self.order.check()
            if check.retcode != 0:
                logger.warning(f"Symbol: {self.order.symbol}\nResult:\n{dict_to_string(check.get_dict(include={'comment', 'retcode'}), multi=True)}")
                return

            result = await self.order.send()
            if result.retcode != 10009:
                logger.warning(f"Symbol: {self.order.symbol}\nResult:\n{dict_to_string(result.get_dict(include={'comment', 'retcode'}), multi=True)}")
                return
            params = params or {}
            params['date'] = (date := datetime.utcnow())
            params['time'] = date.timestamp()
            logger.info(f"Symbol: {self.order.symbol}\nOrder: {dict_to_string(result.dict, multi=True)}\n")
            await TradeResult(result=result, parameters=params).save()
            return
        except Exception as err:
            logger.error(f"{err}. Symbol: {self.order.symbol}\n {self.__class__.__name__}.place_trade")
