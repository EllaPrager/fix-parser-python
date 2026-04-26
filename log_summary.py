from summary import generate_message_summary

def generate_log_summaries(parsed_messages):
    """
    Generate summaries for a list of parsed FIX messages.
    """
    
    summaries = []
    
    for message in parsed_messages:
        summary = generate_message_summary(message)
        summaries.append(summary)
    
    return summaries