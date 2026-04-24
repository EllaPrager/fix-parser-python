from validation_rules import (
    rule_limit_order_without_price,
    rule_market_order_with_price
)
def validate_fix_message(parsed_fix, fix_string):
    
    warnings = []
        
    ord_type = parsed_fix.get("40")
    price = parsed_fix.get("44")
    stop_price = parsed_fix.get("99")
    status = parsed_fix.get("39")
    

    if "55" not in parsed_fix:
        warnings.append("Missing Symbol (tag 55)")    
    
    if "54" not in parsed_fix:
        warnings.append("Missing Side (tag 54)")
    
    if "38" not in parsed_fix:
        warnings.append("Missing Order Quantity (tag 38)")
    
    if "35" not in parsed_fix:
        warnings.append("Missing Message Type (tag 35)")
    
    # Apply business validation rules (each rule returns a warning or None)

    rules = [
        rule_limit_order_without_price, # Limit orders must include price
        rule_market_order_with_price    # Market order should not have price
        

    ]

    for rule in rules:
        warning = rule(parsed_fix)

        if warning:
            warnings.append(warning)
    

    
    #Stop order must have StopPx (tag 99)
    if (ord_type == "3" or ord_type == "4") and not stop_price:
        warnings.append("Stop order missing Stop Price (tag 99)")
    
    # filled order must have last qty
    if status == "2" and "32" not in parsed_fix:
        warnings.append("Filled order but missing LastQty (tag 32)")

    # filled order must have LastPx
    if status == "2" and "31" not in parsed_fix:
        warnings.append("Filled order but missing LastPx (tag 31)")

    # Check BodyLength
    if "9" in parsed_fix:
        declared_length = int(parsed_fix["9"])
        
        message_body = fix_string.split("35=", 1)[-1]
        
        message_body = message_body.split("|10=",1)[0]
        
        actual_length = len(message_body)
        
        if declared_length != actual_length:
            warnings.append("BodyLength mismatch (tag 9)")

    # Check CheckSum
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


