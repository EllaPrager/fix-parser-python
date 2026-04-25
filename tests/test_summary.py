"""
Unit tests for FIX message summary generation.
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from summary import generate_message_summary
from parser import parse_fix_message

def test_generate_message_summary_returns_expected_values():
    """Verify that the summary contains the expected business fields."""
    parsed_fix = {
        "35": "D",
        "54": "1",
        "55": "EUR/USD",
        "38": "1000000",
        "40": "2",
        "44": "1.1050",
        "11": "ABC123"
    }

    result = generate_message_summary(parsed_fix)

    assert result["message_type"] == "New Order Single"
    assert result["side"] == "Buy"
    assert result["symbol"] == "EUR/USD"
    assert result["quantity"] == "1000000"
    assert result["order_type"] == "Limit"
    assert result["price"] == "1.1050"
    assert result["cl_ord_id"] == "ABC123"


def test_generate_message_summary_returns_only_existing_fields():
    """Verify that the summary includes only fields present in the message."""
    parsed_fix = {
        "35": "8",
        "39": "2"
    }

    result = generate_message_summary(parsed_fix)

    assert result["message_type"] == "Execution Report"
    assert result["order_status"] == "Filled"
    assert "symbol" not in result
    assert "side" not in result
    assert "price" not in result

