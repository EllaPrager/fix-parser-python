import json
def load_fix_dictionary():
    """
    Load FIX 4.4 field dictionary from JSON file.

    Returns:
        dict: lookup dictionary by tag number
    """
    try:
        with open("fix44_fields.json") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("FIX dictionary file not found")
        return {}
    except json.JSONDecodeError:
        print("FIX dictionary file is not valid JSON")
        return {}

    # Taking the fields_list
    fields_list = data["Fields"]
    
    # Creating new dict - search by tag
    lookup_dict = {}
    
    # Loop through all the fields in the list
    for field in fields_list:
        tag = str(field["Tag"])
        name = field["Name"]
        field_type = field["Type"]
        
        # instert to the new dict by tag
        lookup_dict[tag] = {
            "name": name,
            "type": field_type
        }
        
    return lookup_dict


def get_field_info(tag):
    """
Return metadata for a given FIX tag.

Includes field name and data type based on FIX dictionary.
"""
    fix_dict = load_fix_dictionary()
    tag = str(tag)
    
    field_info = fix_dict.get(tag)
    
    if field_info is None:
        return {
            "name": "Unknown",
            "type": "Unknown"
        }
    return field_info   