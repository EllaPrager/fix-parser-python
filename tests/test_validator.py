"""
Unit tests for FIX message validation rules.
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from validator import validate_fix_message
from parser import parse_fix_message

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
    """Verifies that a valid parsed FIX message returns no validation warnings."""
    parsed_fix = {
        "35": "D",
        "40": "1",
        "49": "B",
        "56": "C",
        "11": "1",
        "55": "MSFT",
        "54": "1",
        "38": "10"
    }

    result = validate_fix_message(parsed_fix, "")

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
    

def test_validate_fix_message_missing_order_type():
    parsed_fix = {
        "35": "D",
        "54": "1",
        "55": "EUR/USD",
        "38": "1000000",
    }

    result = validate_fix_message(parsed_fix, "")

    assert "Missing Order Type (tag 40)" in result
    
def test_validate_fix_message_execution_report_missing_status():
    """Verify that an execution report without OrdStatus returns a warning."""
    
    parsed_fix = {
        "35": "8",
        "55": "EUR/USD",
        "54": "1",
        "38": "1000000"
    }
    
    result = validate_fix_message(parsed_fix, "")
    
    assert "Execution Report missing Order Status (tag 39)" in result

def test_validate_fix_message_filled_order_missing_execution_data():
    """Verify that a filled order missing both LastPx and LastQty returns a combined warning."""

    parsed_fix = {
        "35": "8",
        "39": "2",
        "55": "EUR/USD",
        "54": "1",
        "38": "1000000"
    }

    result = validate_fix_message(parsed_fix, "")

    assert "Filled order missing execution data (LastPx & LastQty)" in result
    
def test_validate_fix_message_filled_order_missing_last_priece():
    """Verify that a filled order missing LastPx returns a combined warning."""
    
    parsed_fix = {
        "35": "8",
        "39": "2",
        "32": "100",
        "55": "EUR/USD",
        "54": "1",
        "38": "1000000"
    }

    result = validate_fix_message(parsed_fix, "")

    assert "Filled order but missing LastPx (tag 31)" in result


def test_validate_fix_message_valid_execution_report_returns_no_warnings():
    """Verify that a valid execution report returns no validation warnings."""

    parsed_fix = {
        "35": "8",
        "150": "2",
        "39": "2",
        "17": "E123",
        "31": "1.1050",
        "32": "100",
        "55": "EUR/USD",
        "54": "1",
        "38": "100",
        "40": "1"
    }
    
    result = validate_fix_message(parsed_fix, "")
    
    assert result == []
    
def test_validate_fix_message_execution_report_missing_exec_type():
    """Verify that an execution report without ExecType returns a warning."""

    parsed_fix = {
        "35": "8",
        "39": "2",
        "17": "E123",
        "31": "1.1050",
        "32": "100",
        "55": "EUR/USD",
        "54": "1",
        "38": "100",
        "40": "1"
    }

    result = validate_fix_message(parsed_fix, "")

    assert "Execution Report missing ExecType (tag 150)" in result
    
def test_validate_fix_message_execution_report_missing_exec_id():
    """Verify that an execution report without ExecID returns a warning."""

    parsed_fix = {
        "35": "8",
        "39": "2",
        "150": "2",
        "31": "1.1050",
        "32": "100",
        "55": "EUR/USD",
        "54": "1",
        "38": "100",
        "40": "1"
    }

    result = validate_fix_message(parsed_fix, "")

    assert "Execution Report missing ExecID (tag 17)" in result
    
def test_validate_fix_message_cancel_request_missing_orig_cl_ord_id():
    """Verify that a cancel request without OrigClOrdID returns a warning."""

    parsed_fix = {
        "35": "F",
        "55": "EUR/USD",
        "54": "1",
        "38": "100"
    }

    result = validate_fix_message(parsed_fix, "")

    assert "Cancel Request missing OrigClOrdID (tag 41)" in result
    
def test_validate_fix_message_cancel_replace_missing_orig_cl_ord_id():
    """Verify that a cancel/replace request without OrigClOrdID returns a warning."""

    parsed_fix = {
        "35": "G",
        "55": "EUR/USD",
        "54": "1",
        "38": "100"
    }
    
    result = validate_fix_message(parsed_fix, "")
    
    assert "Cancel Replace missing OrigClOrdID (tag 41)" in result