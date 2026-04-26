"""
Unit tests for FIX log processing logic.

Covers:
- Full log processing pipeline
- Parsed message output
- Summary output
- Validation output
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from log_processor import process_fix_log

def test_process_fix_log_multiple_messages():
    """Verify that a FIX log is processed into parsed, summary, and validation output."""

    log_text = "35=D|40=1|55=EUR/USD|54=1|38=100\n35=8|150=2|39=2|17=E123|31=1.1050|32=100|55=EUR/USD|54=1|38=100|40=1"

    result = process_fix_log(log_text)

    assert len(result) == 2

    assert "parsed" in result[0]
    assert "summary" in result[0]
    assert "validation" in result[0]

    assert result[0]["summary"]["message_type"] == "New Order Single"
    assert result[1]["summary"]["message_type"] == "Execution Report"