from typing import List, Iterable
from .schema import TransactionRecord

def _tax_rate_for_region(region: str) -> float:
    # Just a simple tax table.
    table = {
        "ON": 0.13,
        "QC": 0.14975,
        "BC": 0.12,
    }
  
    return table.get(region, 0.10)

def _net_margin_for_record(record: TransactionRecord) -> float:
    # I'm using a basic margin calculation: 30% of revenue.
    return record.revenue * 0.30

def apply_financial_transformations(
    records: Iterable[TransactionRecord],
) -> List[TransactionRecord]:
    # This creates new TransactionRecord objects instead of modifying the originals.
    # It's a functional style: input in, new output out.
    return [
        TransactionRecord(
            branch_id=r.branch_id,
            transaction_date=r.transaction_date,
            customer_tier=r.customer_tier,
            item_count=r.item_count,
            revenue=r.revenue,
            is_active=r.is_active,
            region=r.region,
            net_margin=_net_margin_for_record(r),
            tax_amount=r.revenue * _tax_rate_for_region(r.region),
        )
        for r in records
    ]

def filter_active_transactions(
    records: Iterable[TransactionRecord],
) -> List[TransactionRecord]:
    # Only keeping records that are marked as active.
    return [r for r in records if r.is_active]
