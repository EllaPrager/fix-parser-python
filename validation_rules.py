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