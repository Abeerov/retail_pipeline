
import unittest
from pipeline.validator import validate_records

class TestValidator(unittest.TestCase):
    def test_valid_records(self):
        """
        A simple test to make sure a clean record passes validation.
        """
        raw = [
            {
                "branch_id": "BR001",
                "transaction_date": "2026-10-14",
                "customer_tier": "GOLD",
                "item_count": 2,
                "revenue": 50.0,
                "is_active": True,
                "region": "ON"
            }
        ]
        validated, malformed = validate_records(raw)
        self.assertEqual(len(validated), 1)
        self.assertEqual(len(malformed), 0)

    def test_invalid_record(self):
        """
        This record is missing a branch_id, so it should be flagged.
        """
        raw = [
            {
                "branch_id": None,
                "transaction_date": "2026-10-14",
                "customer_tier": "GOLD",
                "item_count": 2,
                "revenue": 50.0,
                "is_active": True,
                "region": "ON"
            }
        ]
        validated, malformed = validate_records(raw)
        self.assertEqual(len(validated), 0)
        self.assertEqual(len(malformed), 1)
        self.assertIn("error", malformed[0])
