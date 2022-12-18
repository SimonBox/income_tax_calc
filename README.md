# Income Tax Calculation

License: Please don't use this software for any purpose. It is entirely experimental and has no functional value whatsoever. Thanks!

## What's it for?
This helps you calculate the income tax you may owe. Especially from the exercise and sale of shares that have been granted by your employer. The calculation includes AMT, which can be tricky. 
## How to use
Run:
```
python3 scenario_test.py
```
This will run the test scenario described in `test_scenario.json`. To run a scenario that is more relevant to you, create your own `my_scenario.json` file. Then edit `scenario_test.py` to refer to this file and the year for which you are calculating.
## Editing Scenarios
Scenarios include two types of event `Grant` and `Transaction`. Transactions themselves have two types `Exercise` and `Sale`. Examples of the schema for these events can be found in `test_scenarios.json`. Events must be correctly time ordered. Transactions must have grants associated with them.

The field `other_income` should be used to add income from other sources (e.g. salary) for the year being calculated.
## Editing Tax Constants
The file `tax_constants.json` contains the income tax bands and AMT thresholds etc for the IRC and for the state of California in 2020. These constants change from time to time and may need to be updated for subsequent years. For other states than California these constants may be added in the same way. But you with either need to alias the state as "California" or improve the source code to support multiple states.  
