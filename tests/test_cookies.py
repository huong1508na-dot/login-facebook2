import unittest
from app import parse_cookies


class CookieTests(unittest.TestCase):
    def test_preserves_equals_and_facebook_scope(self):
        parsed = parse_cookies("Cookie: c_user=123; xs=fake=token==;")
        self.assertEqual(parsed[1]["value"], "fake=token==")
        self.assertTrue(all(c["domain"] == ".facebook.com" and c["secure"] for c in parsed))

    def test_rejects_invalid_input_without_echoing_secret(self):
        for raw in ["", "c_user=123", "c_user=123; xs=secret; xs=other", "c_user=123; xs=secret\r\nX: bad", "c_user=123; xs=secret; malformed"]:
            with self.subTest(raw=raw):
                with self.assertRaises(ValueError) as caught:
                    parse_cookies(raw)
                self.assertNotIn("secret", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
