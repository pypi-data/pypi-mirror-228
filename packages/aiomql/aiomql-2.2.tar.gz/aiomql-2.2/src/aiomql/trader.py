from abc import ABC, abstractmethod
from typing import TypeVar

from .order import Order
from .symbol import Symbol as _Symbol
from .ram import RAM

Symbol = TypeVar('Symbol', bound=_Symbol)


class Trader(ABC):
    """ Helper class for creating a Trader object. Handles the creation of an order and the placing of trades

    Attributes:
        symbol (Symbol): Financial instrument class Symbol class or any subclass of it.
        ram (RAM): RAM instance
        order (Order): Trade order

    Class Attributes:
        name (str): A name for the strategy.
        account (Account): Account instance.
        mt5 (MetaTrader): MetaTrader instance.
        config (Config): Config instance.
    """

    def __init__(self, *, symbol: Symbol, ram: RAM = None):
        """
        Trader class initializer method. Initializes the order object and RAM instance

        Args:
            symbol (Symbol): Financial instrument
            ram (RAM): Risk Assessment and Management instance
        """
        self.symbol = symbol
        self.order = Order(symbol=symbol.name)
        self.ram = ram or RAM()

    @abstractmethod
    async def place_trade(self, *args, **kwargs):
        """Send trade to the broker
        """
