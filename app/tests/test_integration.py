from app.tap import Tap
from app.trip import Trip
from main import getTapsFromCsv, getTripsFromTaps, processEverything

import os
import csv
import unittest


class TestMain(unittest.TestCase):
    # Functional Tests
    def test_tap_is_same_trip_valid(self):
        firstStop = Tap(1, '22-01-2018 13:00:00', "ON", "Stop1", "Company1", "Bus1", "5500005555555559")
        secondStop = Tap(2, '22-01-2018 13:30:00', "ON", "Stop2", "Company1", "Bus1", "5500005555555559")

        incompleteTrip = Trip(firstStop)

        self.assertTrue(incompleteTrip.isTapPartOfTrip(secondStop))

    def test_tap_is_same_trip_invalid_different_pan(self):
        firstStop = Tap(1, '22-01-2018 13:00:00', "ON", "Stop1", "Company1", "Bus1", "5500005555555559")
        secondStop = Tap(2, '22-01-2018 13:30:00', "ON", "Stop2", "Company1", "Bus1", "5500005555555542")

        incompleteTrip = Trip(firstStop)

        self.assertFalse(incompleteTrip.isTapPartOfTrip(secondStop))

    def test_tap_is_same_trip_invalid_different_company(self):
        firstStop = Tap(1, '22-01-2018 13:00:00', "ON", "Stop1", "Company1", "Bus1", "5500005555555559")
        secondStop = Tap(2, '22-01-2018 13:30:00', "ON", "Stop2", "Company99", "Bus1", "5500005555555542")

        incompleteTrip = Trip(firstStop)

        self.assertFalse(incompleteTrip.isTapPartOfTrip(secondStop))

    def test_tap_is_same_trip_invalid_different_bus(self):
        firstStop = Tap(1, '22-01-2018 13:00:00', "ON", "Stop1", "Company1", "Bus1", "5500005555555559")
        secondStop = Tap(2, '22-01-2018 13:30:00', "ON", "Stop2", "Company1", "Bus4", "5500005555555542")

        incompleteTrip = Trip(firstStop)

        self.assertFalse(incompleteTrip.isTapPartOfTrip(secondStop))

    # Reading/Writing CSV
    def test_reading_taps_from_CSV(self):
        taps = getTapsFromCsv('app/tests/test_data.csv')

        self.assertEqual(len(taps), 9)
        for tap in taps:
            # Could also check the values are consistent with the seed data input...timeboxed tho
            self.assertTrue(isinstance(tap, Tap))

    def test_converting_taps_into_trips(self):
        taps = [
            Tap(1, '22-01-2018 13:00:00', "ON", "Stop1", "Company1", "Bus1", "5500005555555559"),
            Tap(2, '22-01-2018 13:30:00', "OFF", "Stop2", "Company1", "Bus1", "5500005555555559")
        ]

        trips = getTripsFromTaps(taps)

        # Only one total trip entered
        self.assertEqual(len(trips), 1)

        tripToTest = trips[0]
        self.assertEqual(tripToTest.getStatus().name, "COMPLETE")
        self.assertTrue(tripToTest.isComplete())
        self.assertFalse(tripToTest.isCancelled())
        self.assertFalse(tripToTest.isIncomplete())

    # Big test
    def test_output_csv_format(self):
        # In case it didn't get cleaned up last time
        if os.path.exists("test_output.csv"):
            os.remove("test_output.csv")

        processEverything('app/tests/test_data.csv', 'test_output.csv')

        # Lets check the CSV was formatted correctly? Just gonna check header values for now
        with open('test_output.csv') as file:
            csv_reader = csv.reader(file, delimiter=',')
            row = next(csv_reader)
            self.assertEqual(row[0], 'Started')
            self.assertEqual(row[1], 'Finished')
            self.assertEqual(row[2], 'DurationSecs')
            self.assertEqual(row[3], 'FromStopId')
            self.assertEqual(row[4], 'ToStopId')
            self.assertEqual(row[5], 'ChargeAmount')
            self.assertEqual(row[6], 'CompanyId')
            self.assertEqual(row[7], 'BusID')
            self.assertEqual(row[8], 'PAN')
            self.assertEqual(row[9], 'Status')

        # Finally, get rid of temp data
        os.remove("test_output.csv")

    # Maybe more integration tests are required, E.G checking output values given a set of input data...but I
    # have some Elden Ring to play and I'm timeboxed - maybe another time :)
