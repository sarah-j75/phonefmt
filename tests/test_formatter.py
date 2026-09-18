import unittest

from phonefmt import PhoneFormatError, normalize

# (input, expected output). expected of None means normalize() must raise.
CASES = [
    ("(415) 555-2671", "+14155552671"),
    ("415.555.2671", "+14155552671"),
    ("415-555-2671", "+14155552671"),
    ("4155552671", "+14155552671"),
    ("1-415-555-2671", "+14155552671"),
    ("+1-415-555-2671", "+14155552671"),
    ("+1 (415) 555-2671", "+14155552671"),
    ("  415  555   2671  ", "+14155552671"),
    ("415 555 2671\n", "+14155552671"),
    ("", None),
    ("   ", None),
    ("555-2671", None),
    ("415-555-26710", None),
    ("0415-555-2671", None),
    ("1415-555-2671", None),
    ("415-055-2671", None),
    ("415-CALL-NOW", None),
    ("415-555-2671 ext. 204", "+14155552671;ext=204"),
    ("415-555-2671x204", "+14155552671;ext=204"),
    ("415-555-2671 x 204", "+14155552671;ext=204"),
    ("415-555-2671 extension 204", "+14155552671;ext=204"),
    ("(415) 555-2671 EXT 9", "+14155552671;ext=9"),
    ("+1 415 555 2671 ext. 204", "+14155552671;ext=204"),
    ("415-555-2671 ext.", None),
    ("ext. 204", None),
    ("415-555-2671 ext. 12345678", None),
    ("+44 20 7946 0958", None),
    ("2-415-555-2671", None),
]


class NormalizeTableTests(unittest.TestCase):
    def test_cases(self):
        for raw, expected in CASES:
            with self.subTest(raw=raw):
                if expected is None:
                    with self.assertRaises(PhoneFormatError):
                        normalize(raw)
                else:
                    self.assertEqual(normalize(raw), expected)

    def test_none_input_raises(self):
        with self.assertRaises(PhoneFormatError):
            normalize(None)


if __name__ == "__main__":
    unittest.main()
