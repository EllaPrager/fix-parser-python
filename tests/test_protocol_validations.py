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