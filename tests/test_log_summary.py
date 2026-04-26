from log_summary import generate_log_summaries


def test_generate_log_summaries_multiple_messages():
    """Verify that summaries are generated for multiple parsed messages."""

    parsed_messages = [
        {"35": "D", "55": "EUR/USD", "54": "1", "38": "100"},
        {"35": "8", "55": "EUR/USD", "39": "2"}
    ]

    result = generate_log_summaries(parsed_messages)

    assert len(result) == 2
    assert result[0]["message_type"] == "New Order Single"
    assert result[1]["message_type"] == "Execution Report"


def test_generate_log_summaries_empty_input():
    """Verify that empty input returns an empty list."""

    result = generate_log_summaries([])

    assert result == []