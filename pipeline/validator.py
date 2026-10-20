from datetime import datetime
from typing import List, Tuple, Dict, Any
from .schema import TransactionRecord

def _parse_date(date_str: str) -> datetime:
    # Trying a couple of date formats because real data isn't always consistent.
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    # If none of the formats work, I let the caller know what went wrong.
    raise ValueError(f"Invalid date format: {date_str}")

def _is_valid_record(raw: Dict[str, Any]) -> Tuple[bool, str]:
    # Making sure the record has a branch ID.
    if not raw.get("branch_id"):
        return False, "Missing branch_id"

    # Revenue should exist and never be negative.
    if raw.get("revenue") is None or raw["revenue"] < 0:
        return False, "Revenue is missing or negative"

    # Same idea for item_count.
    if raw.get("item_count") is None or raw["item_count"] < 0:
        return False, "Item count is missing or negative"

    # Checking the date format.
    try:
        _parse_date(raw["transaction_date"])
    except Exception as e:
        return False, f"Bad date: {e}"

    # If we reach this point, the record looks okay.
    return True, ""

def validate_records(
    raw_records: List[Dict[str, Any]]
) -> Tuple[List[TransactionRecord], List[Dict[str, Any]]]:

    validated: List[TransactionRecord] = []
    malformed: List[Dict[str, Any]] = []

    for raw in raw_records:
        is_valid, reason = _is_valid_record(raw)

        if not is_valid:
            
            malformed.append({**raw, "error": reason})
            continue

        try:
            # Building the final TransactionRecord object.
            record = TransactionRecord(
                branch_id=str(raw["branch_id"]),
                transaction_date=_parse_date(str(raw["transaction_date"])),
                customer_tier=str(raw.get("customer_tier", "UNKNOWN")),
                item_count=int(raw["item_count"]),
                revenue=float(raw["revenue"]),
                is_active=bool(raw.get("is_active", True)),
                region=str(raw.get("region", "UNKNOWN")),
            )
            validated.append(record)

        except Exception as e:
            # Catching any unexpected construction errors.
            malformed.append({**raw, "error": f"Construction error: {e}"})

    return validated, malformed
