from fix_values_dictionary import get_value_meaning
from fix_dictionary import get_field_info
def parse_fix_message(fix_string):

    """
Parse FIX message string into dictionary of tag-value pairs.

Splits message by delimiter and converts it into a lookup structure
for further processing.
"""
    # מפרקים לפי |
    pairs = fix_string.split("|")

    # ניצור dictionary ריק
    fix_dict = {}

    # עוברים על כל זוג tag=value
    for pair in pairs:

        # בודקים שיש = (כדי להימנע משורה ריקה בסוף)
        if "=" in pair:

            tag, value = pair.split("=")

            fix_dict[tag] = value

    return fix_dict

def enrich_fix_message(paresed_fix):
    
    """
Transform parsed FIX message into structured rows with field metadata.

For each tag-value pair, adds:
- FIX field name
- data type
- human-readable meaning (if available)

Returns list of dictionaries for display in tables or UI.
"""    
    enriched_rows = []
    
    for tag, value in paresed_fix.items():
        field_info = get_field_info(tag)
        field_name = field_info["name"]
        field_type = field_info["type"]
        meaning = get_value_meaning(tag, value)
        
        
        row = {
            "tag": tag,
            "field": field_name,
            "value": value,
            "type": field_type,
            "meaning": meaning
        }
        
        enriched_rows.append(row)
    return enriched_rows

def generate_message_summary(paresed_fix):
    
    """
Generate high-level summary of key FIX message attributes.

Extracts important business fields such as:
- message type
- side
- symbol
- quantity

Used to provide quick understanding of the order.
"""
    summary = {}
    
    # Type
    if "35" in paresed_fix:
        value = paresed_fix["35"]
        meaning = get_value_meaning("35", value)
        summary["message_type"] = meaning
    
    # Side
    if "54" in paresed_fix:
        value = paresed_fix["54"]
        meaning = get_value_meaning("54", value)
        summary["side"] = meaning
    
    # Symbol
    if "55" in paresed_fix:
        value = paresed_fix["55"]
        summary["symbol"] = value
    
    # Quantity
    if "38" in paresed_fix:
        value = paresed_fix["38"]
        summary["quantity"] = value
    
    # Order Type
    if "40" in paresed_fix:
        value = paresed_fix["40"]
        meaning = get_value_meaning("40", value)
        summary["order_type"] = meaning
    
    # Price
    if "44" in paresed_fix:
        value = paresed_fix["44"]
        summary["price"] = value
    
    # Order Status
    if "39" in paresed_fix:
        value = paresed_fix["39"]
        meaning = get_value_meaning("39", value)
        summary["order_status"] = meaning
    
    # ClOrdID
    if "11" in paresed_fix:
        value = paresed_fix["11"]
        summary["cl_ord_id"] = value
        
    # ExecID
    if "17" in paresed_fix:
        value = paresed_fix["17"]
        summary["exec_id"] = value

    # Order
    if "37" in paresed_fix:
        value = paresed_fix["37"]
        summary["order_id"] = value
        
    # TransactTime
    if "60" in paresed_fix:
        value = paresed_fix["60"]
        summary["transact_time"] = value
    
    # TimeInForce
    if "59" in paresed_fix:
        value = paresed_fix["59"]
        meaning = get_value_meaning("59", value)
        summary["time_in_force"] = meaning
    
    # LastQty
    if "32" in paresed_fix:
        value = paresed_fix["32"]
        summary["last_qty"] = value
    
    # LastPx
    if "31" in paresed_fix:
        value = paresed_fix["31"]
        summary["last_price"] = value
    
    # CumQty
    if "14" in paresed_fix:
        value = paresed_fix["14"]
        summary["cum_qty"] = value
    
    # LeavesQty - leaves_qty
    if "151" in paresed_fix:
        value = paresed_fix["151"]
        summary["leaves_qty"] = value
    
    # SenderCompID
    if "49" in paresed_fix:
        value = paresed_fix["49"]
        summary["sender_comp_id"] = value

    # TargetCompID
    if "56" in paresed_fix:
        value = paresed_fix["56"]
        summary["target_comp_id"] = value

    # orig_cl_ord_id
    if "41" in paresed_fix:
        value = paresed_fix["41"]
        summary["orig_cl_ord_id"] = value
    
    # text
    if "58" in paresed_fix:
        value = paresed_fix["58"]
        summary["text"] = value
    
    # sending_time
    if "52" in paresed_fix:
        value = paresed_fix["52"]
        summary["sending_time"] = value
    
    # reject_reason
    if "103" in paresed_fix:
        value = paresed_fix["103"]
        meaning = get_value_meaning("103", value)
        summary["reject_reason"] = meaning
    return summary

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
    if (ord_type == "3"or ord_type == "4") and not stop_price:
        warnings.append("Stop order missing Stop Price (tag 99)")
    
    # filled order must have last qty
    if status == "2" and "32" not in parsed_fix:
        warnings.append("Filled order but missing LastQty (tag 32)")

    # filled order must have LastPx
        if status == "2" and "31" not in parsed_fix:
            warnings.append("Filled order but missing LastPx (tag 31)")


    
    return warnings

    