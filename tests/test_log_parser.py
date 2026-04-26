"""
Unit tests for FIX log parsing logic.

Covers:
- Parsing multiple FIX messages from a log
- Ignoring empty lines
- Handling empty input
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from log_parser import parse_fix_log

def test_parse_fix_log_multiple_messages():
    """Verify that multiple FIX messages are parsed into a list of dictionaries."""
    log_text = "35=D|55=EUR/USD|54=1\n35=8|55=EUR/USD|39=2"

    result = parse_fix_log(log_text)

    assert len(result) == 2
    assert result[0]["35"] == "D"
    assert result[1]["35"] == "8"


def test_parse_fix_log_ignores_empty_lines():
    """Verify that empty lines in the log are ignored during parsing."""
    log_text = "\n35=D|55=EUR/USD|\n\n35=8|55=EUR/USD|\n"

    result = parse_fix_log(log_text)

    assert len(result) == 2


def test_parse_fix_log_empty_input():
    """Verify that an empty log input returns an empty list."""
    log_text = ""

    result = parse_fix_log(log_text)

    assert result == []