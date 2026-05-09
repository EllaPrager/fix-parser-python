def validate_body_length(parsed_fix, fix_string, delimiter="|"):
    """
    Validate FIX BodyLength (tag 9).

    Compares the declared body length from the FIX message
    against the actual calculated body length.

    Supports configurable FIX delimiters.
    """

    if "9" not in parsed_fix:
        return None

    declared_length = int(parsed_fix["9"])

    message_body = fix_string.split("35=", 1)[-1]
    message_body = message_body.split(f"{delimiter}10=", 1)[0]

    actual_length = len(message_body)

    if declared_length != actual_length:
        return "BodyLength mismatch (tag 9)"

    return None


def validate_checksum(parsed_fix, fix_string, delimiter="|"):
    """
    Validate FIX CheckSum (tag 10).

    Converts the FIX message into SOH-delimited format
    and calculates the checksum according to the FIX protocol
    specification.

    Supports configurable FIX delimiters.
    """

    if "10" not in parsed_fix:
        return None

    declared_checksum = parsed_fix["10"]

    fix_with_soh = fix_string.replace(delimiter, "\x01")

    message_without_checksum = fix_with_soh.split("\x0110=", 1)[0]

    checksum_total = sum(bytearray(message_without_checksum, "ascii"))

    actual_checksum = checksum_total % 256
    formatted_checksum = f"{actual_checksum:03}"

    if formatted_checksum != declared_checksum:
        return "CheckSum mismatch (tag 10)"

    return None