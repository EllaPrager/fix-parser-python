from validation_rules import (
    rule_limit_order_without_price,
    rule_market_order_with_price,
    rule_stop_order_without_stop_price,
    rule_filled_order_without_last_price,
    rule_filled_order_without_last_qty
)

# Business validation rules (each rule returns a warning or None)
BUSINESS_RULES = [
    rule_limit_order_without_price,         # Limit orders must include price (tag 44)
    rule_market_order_with_price,           # Market orders must NOT include price (tag 44)
    rule_stop_order_without_stop_price,     # Stop orders must include StopPx (tag 99)
    rule_filled_order_without_last_price,   # Filled orders must include LastPx (tag 31)
    rule_filled_order_without_last_qty      # Filled orders must include LastQty (tag 32)
]

def validate_fix_message(parsed_fix, fix_string):
    
    warnings = []    

    if "55" not in parsed_fix:
        warnings.append("Missing Symbol (tag 55)")    
    
    if "54" not in parsed_fix:
        warnings.append("Missing Side (tag 54)")
    
    if "38" not in parsed_fix:
        warnings.append("Missing Order Quantity (tag 38)")
    
    if "35" not in parsed_fix:
        warnings.append("Missing Message Type (tag 35)")


    for rule in BUSINESS_RULES:
        warning = rule(parsed_fix)

        if warning:
            warnings.append(warning)
    
    # Protocol-level validations
    if "9" in parsed_fix:
        declared_length = int(parsed_fix["9"])
        
        message_body = fix_string.split("35=", 1)[-1]
        
        message_body = message_body.split("|10=", 1)[0]
        
        actual_length = len(message_body)
        
        if declared_length != actual_length:
            warnings.append("BodyLength mismatch (tag 9)")

    if "10" in parsed_fix:
        declared_checksum = parsed_fix["10"]
    
        fix_with_soh = fix_string.replace("|", "\x01")
    
        message_without_checksum = fix_with_soh.split("\x0110=", 1)[0]
    
        checksum_total = sum(bytearray(message_without_checksum, "ascii"))
            
        actual_checksum = checksum_total % 256
        formatted_checksum = f"{actual_checksum:03}"

        if formatted_checksum != declared_checksum:
            warnings.append("CheckSum mismatch (tag 10)")    
    return warnings


