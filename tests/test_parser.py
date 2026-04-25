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
    
def test_parse_fix_message_ignores_empty_part_at_end():
    """Verify that a trailing delimiter does not break parsing."""
    fix_message = "35=D|54=1|55=EUR/USD|"

    result = parse_fix_message(fix_message)

    assert result == {
        "35": "D",
        "54": "1",
        "55": "EUR/USD"
    }
    
def test_validate_fix_message_valid_message_returns_no_warnings():
    """Verifies that a valid FIX message returns no validation warnings"""
    fix_message = "8=FIX.4.4|9=35|35=D|49=B|56=C|11=1|55=MSFT|54=1|38=10|10=087"

    parsed_fix = parse_fix_message(fix_message)

    result = validate_fix_message(parsed_fix, fix_message)

    assert result == []
    

    


def test_validate_fix_message_multiple_errors():
    """Verifies that multiple validation errors are detected in a single FIX message"""
    
    fix_message = "8=FIX.4.4|9=999|35=D|49=B|56=C|11=1|55=MSFT|10=999"
    
    parsed_fix = parse_fix_message(fix_message)
    
    result = validate_fix_message(parsed_fix, fix_message)
    
    assert "Missing Side (tag 54)" in result
    assert "Missing Order Quantity (tag 38)" in result
    assert "BodyLength mismatch (tag 9)" in result
    assert "CheckSum mismatch (tag 10)" in result
    
