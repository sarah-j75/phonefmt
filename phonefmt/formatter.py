"""Normalize messy North American phone number strings to E.164.

Scope for now is NANP (US/Canada, +1) only. Extensions and other
country codes are rejected rather than guessed at -- see README.
"""

import re

_PUNCTUATION = re.compile(r"[\s\-.()]")
_TRAILING_EXT = re.compile(r"(ext\.?|x|extension)\s*\d+\s*$", re.IGNORECASE)


class PhoneFormatError(ValueError):
    """Raised when input can't be turned into a valid NANP number."""


def normalize(raw: str) -> str:
    """Return a NANP number as E.164, e.g. '+14155552671'.

    Accepts the usual mess: parens, dots, dashes, stray whitespace,
    an optional leading 1 or +1. Rejects anything with letters,
    extensions, or a non-NANP country code -- those need a human
    to look at them rather than a guess.
    """
    if raw is None:
        raise PhoneFormatError("input is None")

    text = raw.strip()
    if not text:
        raise PhoneFormatError("empty input")

    if _TRAILING_EXT.search(text):
        raise PhoneFormatError(f"extensions are not supported: {raw!r}")

    if any(ch.isalpha() for ch in text):
        raise PhoneFormatError(f"vanity/lettered numbers are not supported: {raw!r}")

    has_plus = text.startswith("+")
    body = text[1:] if has_plus else text
    digits = _PUNCTUATION.sub("", body)

    if not digits.isdigit():
        raise PhoneFormatError(f"unexpected characters in: {raw!r}")

    if has_plus and not digits.startswith("1"):
        raise PhoneFormatError(f"only +1 (NANP) numbers are supported: {raw!r}")

    if len(digits) == 11:
        if not digits.startswith("1"):
            raise PhoneFormatError(f"11-digit numbers must start with 1: {raw!r}")
        digits = digits[1:]
    elif len(digits) != 10:
        raise PhoneFormatError(f"expected 10 digits, got {len(digits)}: {raw!r}")

    area_code, exchange_code = digits[0:3], digits[3:6]
    if area_code[0] in "01":
        raise PhoneFormatError(f"invalid area code {area_code!r}: {raw!r}")
    if exchange_code[0] in "01":
        raise PhoneFormatError(f"invalid exchange code {exchange_code!r}: {raw!r}")

    return "+1" + digits
