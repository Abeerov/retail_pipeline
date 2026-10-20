
import unittest
from datetime import datetime
from pipeline.schema import TransactionRecord

class TestSchema(unittest.TestCase):
    def test_record_creation(self):
        """
        Just checking that the TransactionRecord dataclass stores values correctly.
        """
        rec = TransactionRecord(
            branch_id="001",
            transaction_date=datetime(2026, 10, 14),
            customer_tier="GOLD",
            item_count=3,
            revenue=120.5,
            is_active=True,
            region="ON"
        )

        self.assertEqual(rec.branch_id, "001")
        self.assertEqual(rec.item_count, 3)
        self.assertEqual(rec.customer_tier, "GOLD")
        self.assertEqual(rec.revenue, 120.5)
        self.assertTrue(rec.is_active)
        self.assertEqual(rec.region, "ON")
        self.assertIsInstance(rec.transaction_date, datetime)

        # default fields
        self.assertEqual(rec.net_margin, 0.0)
        self.assertEqual(rec.tax_amount, 0.0)

    def test_record_is_immutable(self):
        """
        The dataclass is frozen, so trying to change a field should raise an error.
        """
        rec = TransactionRecord(
            branch_id="001",
            transaction_date=datetime(2026, 10, 14),
            customer_tier="GOLD",
            item_count=3,
            revenue=120.5,
            is_active=True,
            region="ON"
        )

        with self.assertRaises(Exception):
            rec.branch_id = "NEW"
