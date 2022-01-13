from scenario import Scenario

import unittest

class TestScenario(unittest.TestCase):
    def setUp(self):
        scenario_file_path = "test_scenario.json"
        self.scenario = Scenario(scenario_file_path)

    def test_grant_load(self):
        self.assertEqual(len(self.scenario.grants), 2)

if __name__ == "__main__":
    unittest.main()
