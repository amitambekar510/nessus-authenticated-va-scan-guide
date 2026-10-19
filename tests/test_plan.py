import unittest
from scripts.build_plan import markdown

class PlanningTests(unittest.TestCase):
    def test_valid(self):
        p={"environment":"lab","os":"Linux","host_count":2,"scanner":"Licensed Nessus","authentication":"Vault-managed SSH","approval":"authorized","change_window":"approved window","reporting":"risk-ranked results"}
        out=markdown(p)
        self.assertIn("Review Plan",out)
        self.assertIn("To collect",out)
    def test_missing_approval(self):
        p={"environment":"lab","host_count":2}
        with self.assertRaises(ValueError):markdown(p)
    def test_escape_html(self):
        p={"environment":"<script>","os":"Linux","host_count":1,"scanner":"Nessus","authentication":"SSH","approval":"yes","change_window":"night","reporting":"review"}
        self.assertNotIn("<script>",markdown(p))
