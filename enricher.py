from fix_dictionary import get_field_info
from fix_values_dictionary import get_value_meaning
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