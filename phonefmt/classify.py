"""Classify NANP numbers by their area code.

This only makes sense for NANP numbers: toll-free and premium-rate
prefixes are an NANP-specific convention. Other numbering plans have
their own, incompatible rules for this, which is one more reason
international support (see README) needs its own handling rather than
reusing this.
"""

from .formatter import PhoneFormatError

TOLL_FREE = "toll-free"
PREMIUM = "premium"
STANDARD = "standard"

# The full set of toll-free area codes assigned so far. 800 is the
# original; the rest were added as it filled up. There is no pattern
# to guess from, so this has to be a literal list.
_TOLL_FREE_AREA_CODES = frozenset({"800", "833", "844", "855", "866", "877", "888"})

# 900 is the only NANP area code set aside for premium-rate services
# (pay-per-call/pay-per-minute lines).
_PREMIUM_AREA_CODES = frozenset({"900"})


def classify(e164: str) -> str:
    """Return TOLL_FREE, PREMIUM, or STANDARD for a NANP E.164 number.

    Expects the output of normalize(), e.g. '+14155552671' or
    '+18005551234;ext=9'. Raises PhoneFormatError for anything that
    isn't a well-formed NANP E.164 number, including non-NANP numbers.
    """
    if not e164.startswith("+1"):
        raise PhoneFormatError(f"not a NANP E.164 number: {e164!r}")

    digits = e164[2:].split(";", 1)[0]
    if len(digits) != 10 or not digits.isdigit():
        raise PhoneFormatError(f"not a NANP E.164 number: {e164!r}")

    area_code = digits[:3]
    if area_code in _TOLL_FREE_AREA_CODES:
        return TOLL_FREE
    if area_code in _PREMIUM_AREA_CODES:
        return PREMIUM
    return STANDARD
