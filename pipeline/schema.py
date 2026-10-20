from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TransactionRecord:
    """
    A single cleaned retail transaction after validation.
    Additional financial fields (net_margin, tax_amount) are added later
    during the transformation step.
    """
    branch_id: str
    transaction_date: datetime
    customer_tier: str
    item_count: int
    revenue: float
    is_active: bool
    region: str
    net_margin: float = 0.0
    tax_amount: float = 0.0
