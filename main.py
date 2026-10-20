from datetime import datetime
from pipeline.validator import validate_records
from pipeline.transformer import (
    apply_financial_transformations,
    filter_active_transactions,
)
from pipeline.reporter import generate_summary_report

def load_raw_data():
    """
    Just some sample records to test the pipeline.
    In a real project these could come from a CSV, JSON file, or even a database.
    """
    return [
        {
            "branch_id": "BR001",
            "transaction_date": "2026-10-14",
            "customer_tier": "GOLD",
            "item_count": 3,
            "revenue": 120.50,
            "is_active": True,
            "region": "ON",
        },
        {
            "branch_id": "BR002",
            "transaction_date": "2026/10/14",
            "customer_tier": "SILVER",
            "item_count": 1,
            "revenue": -10.00,  # negative revenue → should be flagged
            "is_active": True,
            "region": "QC",
        },
        {
            "branch_id": None,  # missing branch → should be flagged
            "transaction_date": "2026-10-14",
            "customer_tier": "BRONZE",
            "item_count": 2,
            "revenue": 40.00,
            "is_active": False,
            "region": "ON",
        },
        {
            "branch_id": "BR003",
            "transaction_date": "2026-10-15",
            "customer_tier": "GOLD",
            "item_count": 5,
            "revenue": 300.00,
            "is_active": True,
            "region": "ON",
        },
    ]

def main():
    raw_records = load_raw_data()  # get raw input

    validated_records, malformed_records = validate_records(raw_records)  # clean the data

    transformed_records = apply_financial_transformations(validated_records)  # add financial fields

    active_records = filter_active_transactions(transformed_records)  # keep only active ones

    # print the final summary
    generate_summary_report(
        raw_records=raw_records,
        validated_records=validated_records,
        malformed_records=malformed_records,
        active_records=active_records,
    )

if __name__ == "__main__":
    main()
