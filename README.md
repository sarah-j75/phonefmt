# phonefmt

Phone numbers people type into forms are a mess: parens, dots, stray
spaces, an optional country code, sometimes an extension tacked on the
end. `phonefmt` takes that mess and turns it into a single canonical
form (E.164, like `+14155552671`) or tells you exactly why it can't.

Right now it only handles NANP numbers (US and Canada, `+1`). That
covers the numbers I actually need to deal with day to day. Other
country codes and extensions are rejected on purpose rather than
half-guessed at -- see the roadmap below.

## Usage

```python
from phonefmt import normalize, PhoneFormatError

normalize("(415) 555-2671")      # "+14155552671"
normalize("415.555.2671")        # "+14155552671"
normalize("1-415-555-2671")      # "+14155552671"
normalize("+1 415 555 2671")     # "+14155552671"

try:
    normalize("415-CALL-NOW")
except PhoneFormatError as exc:
    print(exc)  # vanity/lettered numbers are not supported: '415-CALL-NOW'
```

## Why not just use a regex and call it done

Because the awkward cases are where formatters like this actually
break: an 11-digit number that doesn't start with 1, an area code that
starts with 0, an extension quietly getting swallowed into the number,
international numbers that happen to also be 10 digits long. The test
suite in `tests/test_formatter.py` is a flat table of inputs and
expected outputs (or expected failures) specifically so those cases
stay visible and don't get lost in prose.

## Running the tests

Standard library only, no test runner to install:

```
python -m unittest discover tests
```

## Status

Early. Single function, NANP only. See below for what's next.
