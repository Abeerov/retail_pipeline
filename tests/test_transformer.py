import unittest
from datetime import datetime
from pipeline.schema import TransactionRecord
from pipeline.transformer import apply_financial_transformations

class TestTransformer(unittest.TestCase):
    def test_financial_transformations(self):
        """
        Making sure the transformer adds the correct financial fields
        without changing the original record.
        """
        rec = TransactionRecord(
            branch_id="BR001",
            transaction_date=datetime.now(),
            customer_tier="GOLD",
            item_count=3,
            revenue=100.0,
            is_active=True,
            region="ON"
        )

        transformed = apply_financial_transformations([rec])[0]

        # margin should be 30% of revenue
        self.assertAlmostEqual(transformed.net_margin, 30.0)

        # tax for ON should be 13%
        self.assertAlmostEqual(transformed.tax_amount, 100.0 * 0.13)

        # original record should still have default values
        self.assertEqual(rec.net_margin, 0.0)
        self.assertEqual(rec.tax_amount, 0.0)

        # transformed record should be different
        self.assertNotEqual(rec.net_margin, transformed.net_margin)
