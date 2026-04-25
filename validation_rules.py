def rule_limit_order_without_price(parsed_fix):
    ord_type = parsed_fix.get("40")
    price = parsed_fix.get("44")

    if ord_type == "2" and not price:
        return "Limit order without Price (tag 44)"
    
    return None

def rule_market_order_with_price(parsed_fix):
    ord_type = parsed_fix.get("40")
    price = parsed_fix.get("44")
    
    if ord_type == "1" and price:
        return "Market order should not include Price (tag 44)"
    return None

def rule_stop_order_without_stop_price(parsed_fix):
    ord_type = parsed_fix.get("40")
    stop_price = parsed_fix.get("99")
    
    if (ord_type == "3" or ord_type == "4") and not stop_price:
        return "Stop order missing Stop Price (tag 99)"
    return None

def rule_filled_order_without_last_price(parsed_fix):
    status = parsed_fix.get("39")
    
    if status == "2" and "31" not in parsed_fix:
        return "Filled order but missing LastPx (tag 31)"
    
    return None
    
def rule_filled_order_without_last_qty(parsed_fix):
    status = parsed_fix.get("39")

    if status == "2" and "32" not in parsed_fix:
        return "Filled order but missing LastQty (tag 32)"
    
    return None