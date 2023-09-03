"""
Risk Assessment and Management
"""
from .account import Account


class RAM:
    account: Account = Account()
    risk_to_reward: float
    risk: float

    def __init__(self, *, risk_to_reward: float = 1, risk: float = 0.01):
        self.risk_to_reward = risk_to_reward
        self.risk = risk

    async def amount(self) -> float:
        """Calculate the amount to risk per trade

        Returns:
            float: Amount to risk per trade
        """
        await self.account.refresh()
        return self.account.margin_free * self.risk
