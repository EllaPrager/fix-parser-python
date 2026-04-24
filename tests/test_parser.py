"""
Unit tests for FIX parser, enrichment, summary generation, and validation logic.
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parser import parse_fix_message
from enricher import enrich_fix_message
from summary import generate_message_summary
from validator import validate_fix_message



def test_parse_fix_message_returns_dictionary():
    """Verify that a valid FIX string is parsed into a dictionary."""
    fix_message = "35=D|54=1|55=EUR/USD|38=1000000|44=1.1050"

    result = parse_fix_message(fix_message)

    assert result == {
        "35": "D",
        "54": "1",
        "55": "EUR/USD",
        "38": "1000000",
        "44": "1.1050"
    }


def test_parse_fix_message_ignores_empty_part_at_end():
    """Verify that a trailing delimiter does not break parsing."""
    fix_message = "35=D|54=1|55=EUR/USD|"

    result = parse_fix_message(fix_message)

    assert result == {
        "35": "D",
        "54": "1",
        "55": "EUR/USD"
    }


def test_enrich_fix_message_adds_field_type_and_meaning():
    """Verify that parsed FIX fields are enriched with metadata and meanings."""
    parsed_fix = {
        "35": "D",
        "54": "1",
        "55": "EUR/USD"
    }

    result = enrich_fix_message(parsed_fix)

    assert len(result) == 3

    assert result[0]["tag"] == "35"
    assert result[0]["field"] == "MsgType"
    assert result[0]["value"] == "D"
    assert result[0]["type"] == "String"
    assert result[0]["meaning"] == "New Order Single"

    assert result[1]["tag"] == "54"
    assert result[1]["field"] == "Side"
    assert result[1]["value"] == "1"
    assert result[1]["type"] == "char"
    assert result[1]["meaning"] == "Buy"

    assert result[2]["tag"] == "55"
    assert result[2]["field"] == "Symbol"
    assert result[2]["value"] == "EUR/USD"
    assert result[2]["type"] == "String"
    assert result[2]["meaning"] == ""


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


def test_validate_fix_message_missing_required_fields():
    """Verify that missing required tags return validation warnings."""
    parsed_fix = {}
    fix_string = ""
    
    result = validate_fix_message(parsed_fix, fix_string)

    assert "Missing Symbol (tag 55)" in result
    assert "Missing Side (tag 54)" in result
    assert "Missing Order Quantity (tag 38)" in result
    assert "Missing Message Type (tag 35)" in result


def test_validate_fix_message_limit_order_without_price():
    """Verify that a limit order without price returns a warning."""
    parsed_fix = {
        "35": "D",
        "54": "1",
        "55": "EUR/USD",
        "38": "1000000",
        "40": "2"
    }
    
    fix_string = ""

    result = validate_fix_message(parsed_fix, fix_string)

    assert "Limit order without Price (tag 44)" in result


def test_validate_fix_message_market_order_with_price():
    """Verify that a market order with price returns a warning."""
    parsed_fix = {
        "35": "D",
        "54": "1",
        "55": "EUR/USD",
        "38": "1000000",
        "40": "1",
        "44": "1.1050"
    }

    fix_string = ""

    result = validate_fix_message(parsed_fix, fix_string)

    assert "Market order should not include Price (tag 44)" in result


def test_validate_fix_message_stop_order_without_stop_price():
    """Verify that a stop order without StopPx returns a warning."""
    parsed_fix = {
        "35": "D",
        "54": "1",
        "55": "EUR/USD",
        "38": "1000000",
        "40": "3"
    }
    fix_string = ""

    result = validate_fix_message(parsed_fix, fix_string)

    assert "Stop order missing Stop Price (tag 99)" in result


def test_validate_fix_message_filled_order_missing_last_qty():
    """Verify that a filled order without LastQty returns a warning."""
    parsed_fix = {
        "35": "8",
        "39": "2",
        "54": "1",
        "55": "EUR/USD",
        "38": "1000000"
    }

    fix_string = ""
    
    result = validate_fix_message(parsed_fix, fix_string)

    assert "Filled order but missing LastQty (tag 32)" in result
    
def test_validate_fix_message_valid_message_returns_no_warnings():
    """Verifies that a valid FIX message returns no validation warnings"""
    fix_message = "8=FIX.4.4|9=35|35=D|49=B|56=C|11=1|55=MSFT|54=1|38=10|10=087"

    parsed_fix = parse_fix_message(fix_message)

    result = validate_fix_message(parsed_fix, fix_message)

    assert result == []
    
def test_validate_fix_message_body_length_mismatch():
    """Verifies that an incorrect BodyLength triggers a validation warning"""
    fix_message = "8=FIX.4.4|9=999|35=D|49=B|56=C|11=1|55=MSFT|54=1|38=10|10=090"
    
    parsed_fix = parse_fix_message(fix_message)
    
    result = validate_fix_message(parsed_fix, fix_message)
    
    assert "BodyLength mismatch (tag 9)" in result
    
def test_validate_fix_message_checksum_mismatch():
    """Verifies that an incorrect CheckSum triggers a validation warning"""
    fix_message = "8=FIX.4.4|9=35|35=D|49=B|56=C|11=1|55=MSFT|54=1|38=10|10=999"
    
    parsed_fix = parse_fix_message(fix_message)
    
    result = validate_fix_message(parsed_fix, fix_message)
    
    assert "CheckSum mismatch (tag 10)" in result

def test_validate_fix_message_multiple_errors():
    """Verifies that multiple validation errors are detected in a single FIX message"""
    
    fix_message = "8=FIX.4.4|9=999|35=D|49=B|56=C|11=1|55=MSFT|10=999"
    
    parsed_fix = parse_fix_message(fix_message)
    
    result = validate_fix_message(parsed_fix, fix_message)
    
    assert "Missing Side (tag 54)" in result
    assert "Missing Order Quantity (tag 38)" in result
    assert "BodyLength mismatch (tag 9)" in result
    assert "CheckSum mismatch (tag 10)" in result
    
def test_validate_fix_message_limit_order_without_price():
    
    fix_message = "8=FIX.4.4|9=50|35=D|40=2|49=B|56=C|11=1|55=MSFT|54=1|38=10|10=090"
    
    parsed_fix = parse_fix_message(fix_message)

    result = validate_fix_message(parsed_fix, fix_message)

    assert any("Limit order without Price (tag 44)" in w for w in result)
    
def test_validate_fix_message_market_order_with_price():
    """Verifies that a market order with a price triggers a validation warning"""
    fix_message = "8=FIX.4.4|9=60|35=D|40=1|44=100|49=B|56=C|11=1|55=MSFT|54=1|38=10|10=999"

    parsed_fix = parse_fix_message(fix_message)
    
    result = validate_fix_message(parsed_fix, fix_message)

    assert "Market order should not include Price (tag 44)" in result
