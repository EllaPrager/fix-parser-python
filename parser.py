def parse_fix_message(fix_string, delimiter="|"):

    """
    Parse FIX message string into dictionary of tag-value pairs.

    Splits message by delimiter and converts it into a lookup structure
    for further processing.
    """

    pairs = fix_string.split(delimiter)

    fix_dict = {}

    for pair in pairs:

        if "=" in pair:

            tag, value = pair.split("=", 1)

            fix_dict[tag] = value

    return fix_dict