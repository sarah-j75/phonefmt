# phonefmt

Phone numbers people type into forms are a mess: parens, dots, stray
spaces, an optional country code, sometimes an extension tacked on the
end. `phonefmt` takes that mess and turns it into a single canonical
form (E.164, like `+14155552671`) or tells you exactly why it can't.

Right now it only handles NANP numbers (US and Canada, `+1`). That
covers the numbers I actually need to deal with day to day. Other
country codes are rejected on purpose rather than half-guessed at --
see the roadmap below.

## Usage

```python
from phonefmt import normalize, PhoneFormatError

normalize("(415) 555-2671")      # "+14155552671"
normalize("415.555.2671")        # "+14155552671"
normalize("1-415-555-2671")      # "+14155552671"
normalize("+1 415 555 2671")     # "+14155552671"
normalize("415-555-2671 ext. 204")  # "+14155552671;ext=204"

try:
    normalize("415-CALL-NOW")
except PhoneFormatError as exc:
    print(exc)  # vanity/lettered numbers are not supported: '415-CALL-NOW'
```

`classify()` takes a normalized number and says whether it's toll-free,
premium-rate, or an ordinary line, based on NANP area code:

```python
from phonefmt import classify, normalize, TOLL_FREE

classify(normalize("1-800-555-0199"))  # 'toll-free'
classify(normalize("415-555-2671"))    # 'standard'
classify(normalize("900-555-0199"))    # 'premium'
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

Early, NANP only. `normalize()` turns messy input into E.164;
`classify()` tells you whether a normalized number is toll-free,
premium-rate, or an ordinary line.

## Roadmap

- [ ] international (non-NANP) country code support
- [ ] CLI entry point for one-off lookups
- [x] toll-free and premium area code classification
- [ ] publish package metadata for PyPI
