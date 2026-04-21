VALUE_MEANINGS = {

    "35": {
        "D": "New Order Single",
        "8": "Execution Report",
        "F": "Cancel Request",
        "G": "Cancel Replace"
    },

    "54": {
        "1": "Buy",
        "2": "Sell"
    },

    "39": {
        "0": "New",
        "1": "Partially Filled",
        "2": "Filled",
        "4": "Cancelled",
        "8": "Rejected"
    },

    "40": {
        "1": "Market",
        "2": "Limit",
        "3": "Stop",
        "4": "Stop Limit"
    },
    
    #EXcType
    "150": {
        "0": "New",
        "1": "Partial Fill",
        "2": "Fill",
        "4": "Cancelled",
        "8": "Limit"
    },
    
    # TimeInForce
    "59": {
        "0": "Day",
        "1": "Good Till Cancel",
        "3": "Immediate Or Cancel",
        "4": "Fill Or Kill"
    },
    
   # OrdRejReason 
       "103": {
        "0": "Broker Option",
        "1": "Unknown Symbol",
        "2": "Exchange Closed",
        "3": "Order Exceeds Limit",
        "4": "Duplicate Order",
        "5": "Stale Order"
    }

}


def get_value_meaning(tag, value):
    """
Return human-readable meaning for a FIX tag value.

For enumerated fields (e.g. MsgType, Side), converts coded values
into descriptive text.
"""
    tag = str(tag)
    value = str(value)

    if tag in VALUE_MEANINGS:

        tag_values = VALUE_MEANINGS[tag]

        if value in tag_values:

            return tag_values[value]

    return ""