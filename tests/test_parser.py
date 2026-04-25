"""
Unit tests for FIX message parsing logic.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parser import parse_fix_message

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
    
