from validation_rules import (
    rule_filled_order_missing_execution_data,
    rule_filled_order_without_last_price,
    rule_filled_order_without_last_qty,
    rule_limit_order_without_price,
    rule_market_order_with_price,
    rule_stop_order_without_stop_price,
    rule_missing_order_type,
    rule_execution_report_missing_status,
    rule_execution_report_missing_exec_type,
    rule_execution_report_missing_exec_id,
    rule_cancel_request_missing_orig_cl_ord_id,
    rule_cancel_replace_missing_orig_cl_ord_id
)

from protocol_validations import (
    validate_body_length,
    validate_checksum
)

# Business validation rules (each rule returns a warning message or None)
BUSINESS_RULES = [
    # --- Execution data validation (highest priority) ---
    rule_filled_order_missing_execution_data,   #If both LastPx (31) and LastQty (32) are missing → return combined warning
    
    # --- Partial execution data validation ---
    rule_filled_order_without_last_price,       # If only LastPx (31) is missing 
    rule_filled_order_without_last_qty,         # If only LastQty (32) is missing
    
    # --- Order validation rules ---
    rule_limit_order_without_price,             # Limit orders (40=2) must include Price (44)
    rule_market_order_with_price,               # Market orders (40=1) must NOT include Price (44)
    rule_stop_order_without_stop_price,         # Stop orders (40=3/4) must include StopPx (99)
    rule_missing_order_type,                    # Order must include OrdType (40)
    
    # --- Execution Report validation (35=8) ---
    rule_execution_report_missing_status,       # Execution Report must include OrdStatus (39)
    rule_execution_report_missing_exec_type,    # Execution Report must include ExecType (150)
    rule_execution_report_missing_exec_id,      # Execution Report must include ExecID (17)
    
    # --- Cancel / Replace validation ---
    rule_cancel_request_missing_orig_cl_ord_id,     # Cancel Request (35=F) must include OrigClOrdID (41)
    rule_cancel_replace_missing_orig_cl_ord_id      # Cancel Replace (35=G) must include OrigClOrdID (41)
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