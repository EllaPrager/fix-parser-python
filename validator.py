def validate_fix_message(parsed_fix):
    
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
    
    # limit order must have price
    if ord_type == "2" and not price:
        warnings.append("Limit order without Price (tag 44)")
    
    # Market order should not have price
    if ord_type == "1" and price:
        warnings.append("Market order should not include Price (tag 44)")
    
    #Stop order must have StopPx (tag 99)
    if (ord_type == "3" or ord_type == "4") and not stop_price:
        warnings.append("Stop order missing Stop Price (tag 99)")
    
    # filled order must have last qty
    if status == "2" and "32" not in parsed_fix:
        warnings.append("Filled order but missing LastQty (tag 32)")

    # filled order must have LastPx
    if status == "2" and "31" not in parsed_fix:
        warnings.append("Filled order but missing LastPx (tag 31)")

    return warnings