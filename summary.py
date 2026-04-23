from fix_values_dictionary import get_value_meaning 
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
     
    # BeginString
    if "8" in paresed_fix:
        value = paresed_fix["8"]
        summary["begin_string"] = value
    
    # BodyLength
    if "9" in paresed_fix:
        value = paresed_fix["9"]
        summary["body_length"] = value
        
    #MsgSeqNum
    if "34" in paresed_fix:
        value = paresed_fix["34"]
        summary["msg_seq_num"] = value
    
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
        
    # exec_type
    if "150" in paresed_fix:
        value = paresed_fix["150"]
        meaning = get_value_meaning("150", value)
        summary["exec_type"] = meaning
   
       # CheckSum
    if "10" in paresed_fix:
        value = paresed_fix["10"]
        summary["check_sum"] = value
   
    return summary

    

if __name__ == "__main__":
    from parser import parse_fix_message
    
    test_message = "8=FIX.4.4|9=125|34=12|35=D|49=BROKER|56=CLIENT|11=123|55=MSFT|10=128"
    parsed = parse_fix_message(test_message)
    summary = generate_message_summary(parsed)
    
    print(summary)
