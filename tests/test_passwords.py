import unittest

from cybernova.passwords import analyse_password


class PasswordTests(unittest.TestCase):
    def test_strong_password_scores_well(self):
        report = analyse_password("Orbit!Cedar7-Lantern")
        self.assertEqual(report.score, 5)
        self.assertEqual(report.label, "Excellent")

    def test_common_pattern_is_penalised(self):
        regular = analyse_password("NovaSecure!2026")
        common = analyse_password("Password!2026")
        self.assertLess(common.score, regular.score)
        self.assertTrue(any("common" in tip.lower() for tip in common.suggestions))

    def test_empty_password_does_not_crash(self):
        report = analyse_password("")
        self.assertEqual(report.score, 0)
        self.assertEqual(report.label, "Very weak")


if __name__ == "__main__":
    unittest.main()

