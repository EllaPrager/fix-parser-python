"""
Unit tests for FIX message enrichment logic.
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enricher import enrich_fix_message

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
