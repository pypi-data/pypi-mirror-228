from math import ceil, log10

from ...symbol import Symbol
from ...core.exceptions import VolumeError


class ForexSymbol(Symbol):
    """Subclass of Symbol for Forex Symbols. Handles the conversion of currency and the computation of stop loss,
     take profit and volume.
    """
    @property
    def pip(self):
        """Returns the pip value of the symbol. This is ten times the point value for forex symbols.

        Returns:
            float: The pip value of the symbol.
        """
        return self.point * 10
    async def compute_volume(self, *, amount: float, pips: float) -> float:
        """Compute volume given an amount to risk and target pips. Round the computed volume to the nearest step.

        Args:
            amount (float): Amount to risk. Given in terms of the account currency.
            pips (float): Target pips.

        Returns:
            float: volume

        Raises:
            VolumeError: If the computed volume is less than the minimum volume or greater than the maximum volume.
        """
        if (base := self.currency_profit) != (quote := self.account.currency):
            amount = await self.currency_conversion(amount=amount, base=base, quote=quote)

        volume = amount / (self.pip * self.trade_contract_size * pips)
        step = ceil(abs(log10(self.volume_step)))
        volume = round(volume, step)

        if (volume < self.volume_min) or (volume > self.volume_max):
            raise VolumeError(f'Incorrect Volume. Computed Volume: {volume}; Symbol Max Volume: {self.volume_max}; '
                             f'Symbol Min Volume: {self.volume_min}')

        return volume
