from validation_rules import (
    rule_limit_order_without_price,
    rule_market_order_with_price,
    rule_stop_order_without_stop_price,
    rule_filled_order_without_last_price,
    rule_filled_order_without_last_qty,
    rule_filled_order_missing_execution_data,
    rule_missing_order_type
    
)

from protocol_validations import (
    validate_body_length,
    validate_checksum
)

# Business validation rules (each rule returns a warning or None)
BUSINESS_RULES = [
    rule_limit_order_without_price,         # Limit orders must include price (tag 44)
    rule_market_order_with_price,           # Market orders must NOT include price (tag 44)
    rule_stop_order_without_stop_price,     # Stop orders must include StopPx (tag 99)
    rule_filled_order_without_last_price,   # Filled orders must include LastPx (tag 31)
    rule_filled_order_without_last_qty,     # Filled orders must include LastQty (tag 32)
    rule_filled_order_missing_execution_data,
    rule_missing_order_type
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
    protocol_validations = [
        validate_body_length,
        validate_checksum
    ]

    for validation in protocol_validations:
        warning = validation(parsed_fix, fix_string)

        if warning:
            warnings.append(warning)    
    return warnings