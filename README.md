# Littlepay Stuff

Little process to read and write CSV's of trips - tap on, tap off, tap on again, forget to tap off, etc.

### Assumptions:
- Data is well formatted in the input CSV, but not necessarily ordered
- A person can go on the same bus/route/trip per day - system accomodates for multiple trips on the same combination.
- Trips can't go overnight (E.G can't tap on at 11:50PM and tap off at 12:40PM - this is an obvious use case that should be accounted for, since overnight trains/buses/trams totally exist, but got timeboxed before I figured out the logic for it lol)

### How to Run
We are *assuming* that you have Python3.7.x installed - if not, follow this handy guide (which is just an installation page lol) - https://www.python.org/downloads/

The script will take an input CSV (arugment pre-defined as `input.csv` within the folder), process all the taps, and spit out a CSV called `trips.csv` which contains all the trips, their status, price, time, etc. in the same root folder.

Then I have some helper scripts to just do everything for you (assuming you are on a unix machine) - 
- `setup.sh` creates a local env
- `run.sh` activates the local env and runs the program with default inputs
- `run_tests.sh` acrivates the local env and runs the test harness.

Else, you can invoke by directly writing:
- python3 main.py
- python -m unittest discover app/tests

