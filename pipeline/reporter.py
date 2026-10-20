from typing import List, Dict, Any
from collections import Counter
from .schema import TransactionRecord


def _total_gross_sales(records: List[TransactionRecord]) -> float:
    return sum(r.revenue for r in records)


def _clean_record_retention_percentage(
    raw_records: List[Dict[str, Any]],
    validated_records: List[TransactionRecord],
) -> float:
    if not raw_records:
        return 0.0
    return (len(validated_records) / len(raw_records)) * 100.0


def _top_performing_branch(records: List[TransactionRecord]) -> str:
    if not records:
        return "N/A"
    branch_totals: Dict[str, float] = {}
    for r in records:
        branch_totals.setdefault(r.branch_id, 0.0)
        branch_totals[r.branch_id] += r.revenue
    return max(branch_totals.items(), key=lambda kv: kv[1])[0]


def _customer_tier_breakdown(records: List[TransactionRecord]) -> Dict[str, int]:
    tiers = Counter(r.customer_tier for r in records)
    return dict(tiers)


def generate_summary_report(
    raw_records: List[Dict[str, Any]],
    validated_records: List[TransactionRecord],
    malformed_records: List[Dict[str, Any]],
    active_records: List[TransactionRecord],
) -> None:
    total_gross = _total_gross_sales(validated_records)
    retention_pct = _clean_record_retention_percentage(raw_records, validated_records)
    top_branch = _top_performing_branch(validated_records)
    tier_breakdown = _customer_tier_breakdown(validated_records)

    print("\n=== Retail Network Operational Summary ===")
    print(f"Total raw records ingested:      {len(raw_records)}")
    print(f"Valid, clean records retained:   {len(validated_records)}")
    print(f"Malformed records flagged:       {len(malformed_records)}")
    print(f"Clean record retention:          {retention_pct:.2f}%")
    print()
    print(f"Total gross sales (validated):   ${total_gross:,.2f}")
    print(f"Top-performing branch:           {top_branch}")
    print()
    print("Customer tier breakdown (clean records):")
    for tier, count in tier_breakdown.items():
        print(f"  - {tier}: {count} transactions")
    print()
    print(f"Active transactions (post-transform): {len(active_records)}")
    print("========================================\n")
