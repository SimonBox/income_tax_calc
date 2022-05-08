from scenario import Scenario

import unittest

class TestScenario(unittest.TestCase):
    def setUp(self):
        scenario_file_path = "test_scenario.json"
        self.scenario = Scenario(scenario_file_path)

    def test_grant_load(self):
        self.assertEqual(len(self.scenario.grants), 2)

    def test_tax_calc(self):
        self.scenario.calculate_tax(2020)
    
    def test_tax_calc_private(self):
        scenario_file_path = "aurora_scen_006.json"
        scenario = Scenario(scenario_file_path)
        scenario.display_tax_data(2022)

if __name__ == "__main__":
    unittest.main()
