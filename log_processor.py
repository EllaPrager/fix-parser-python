from log_parser import parse_fix_log
from log_summary import generate_log_summaries
from validator import validate_fix_message

def process_fix_log(log_text):
    """
    Process a FIX log and return structured data for each message.
    """
    
    parsed_messages = parse_fix_log(log_text)
    summaries = generate_log_summaries(parsed_messages)
    
    results = []
    
    for i, message in enumerate(parsed_messages):
        validation = validate_fix_message(message, "")
        
        results.append({
            "parsed": message,
            "summary": summaries[i],
            "validation": validation
        })
    
    return results