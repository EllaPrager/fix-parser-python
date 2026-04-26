from parser import parse_fix_message

def parse_fix_log(log_text):
    """
    Parse a FIX log containing multiple messages into a list of dictionaries.
    """
    
    messages = []
    
    lines = log_text.strip().split("\n")
    
    for line in lines:
        if not line.strip():
            continue
        
        parsed_message = parse_fix_message(line)
        messages.append(parsed_message)
    
    return messages
    