import unittest

from phonefmt import PREMIUM, STANDARD, TOLL_FREE, PhoneFormatError, classify, normalize

# (e164, expected classification)
CASES = [
    ("+18005551234", TOLL_FREE),
    ("+18335551234", TOLL_FREE),
    ("+18445551234", TOLL_FREE),
    ("+18555551234", TOLL_FREE),
    ("+18665551234", TOLL_FREE),
    ("+18775551234", TOLL_FREE),
    ("+18885551234", TOLL_FREE),
    ("+18005551234;ext=204", TOLL_FREE),
    ("+19005551234", PREMIUM),
    ("+14155552671", STANDARD),
    ("+12125551234", STANDARD),
]


class ClassifyTableTests(unittest.TestCase):
    def test_cases(self):
        for e164, expected in CASES:
            with self.subTest(e164=e164):
                self.assertEqual(classify(e164), expected)

    def test_rejects_non_nanp(self):
        with self.assertRaises(PhoneFormatError):
            classify("+442079460958")

    def test_rejects_malformed_input(self):
        with self.assertRaises(PhoneFormatError):
            classify("not a number")

    def test_composes_with_normalize(self):
        self.assertEqual(classify(normalize("(800) 555-1234")), TOLL_FREE)


if __name__ == "__main__":
    unittest.main()
