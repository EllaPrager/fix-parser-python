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



