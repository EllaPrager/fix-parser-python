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

def rule_missing_order_type(parsed_fix):
    if "40" not in parsed_fix:
        return "Missing Order Type (tag 40)"
    return None

def rule_execution_report_missing_status(parsed_fix):
    msg_type = parsed_fix.get("35")
    status = parsed_fix.get("39")

    if msg_type == "8" and not status:
        return "Execution Report missing Order Status (tag 39)"
    return None

def rule_filled_order_missing_execution_data(parsed_fix):
    status = parsed_fix.get("39")

    if status == "2":
        if "31" not in parsed_fix and "32" not in parsed_fix:
            return "Filled order missing execution data (LastPx & LastQty)"
    return None

def rule_execution_report_missing_status(parsed_fix):
    msg_type = parsed_fix.get("35")
    status = parsed_fix.get("39")
    
    if msg_type == "8" and not status:
        return "Execution Report missing Order Status (tag 39)"

def rule_filled_order_missing_execution_data(parsed_fix):
    status = parsed_fix.get("39")
    
    if status == "2":
        has_last_px = "31" in parsed_fix
        has_last_qty = "32" in parsed_fix

        if not has_last_px and not has_last_qty:
            return "Filled order missing execution data (LastPx & LastQty)"
    
    return None

def rule_execution_report_missing_exec_id(parsed_fix):
    if parsed_fix.get("35") == "8" and "17" not in parsed_fix:
        return "Execution Report missing ExecID (tag 17)"
    
    return None
    
def rule_execution_report_missing_exec_type(parsed_fix):
    if parsed_fix.get("35") == "8" and "150" not in parsed_fix:
        return "Execution Report missing ExecType (tag 150)"
    
    return None

def rule_cancel_request_missing_orig_cl_ord_id(parsed_fix):
    if parsed_fix.get("35") == "F" and "41" not in parsed_fix:
        return "Cancel Request missing OrigClOrdID (tag 41)"
    
    return None

def rule_cancel_replace_missing_orig_cl_ord_id(parsed_fix):
    if parsed_fix.get("35") == "G" and "41" not in parsed_fix:
        return "Cancel Replace missing OrigClOrdID (tag 41)"
    
    return None
