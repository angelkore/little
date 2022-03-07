import unittest
from datetime import datetime

from app.trip import Trip
from app.tap import Tap, DATETIME_FORMAT

class TestTap(unittest.TestCase):
    # Init tests
    def test_tap_init(self):
        testTap = Tap(1, '22-01-2018 13:00:00', "ON", "Stop1", "Company1", "Bus1", "5500005555555559")
        self.assertTrue(isinstance(testTap, Tap))

        self.assertEqual(testTap.tapType, "ON")
        self.assertEqual(testTap.stopId, "Stop1")
        self.assertEqual(testTap.companyId, "Company1")
        self.assertEqual(testTap.busId, "Bus1")
        self.assertEqual(testTap.PAN, "5500005555555559")
        self.assertEqual(testTap.id, 1)

        # Check the datetime var while we are here
        self.assertTrue(isinstance(testTap.dateTimeUTC, datetime))

        datetimeInitialized = datetime.strptime('22-01-2018 13:00:00', DATETIME_FORMAT)
        self.assertEqual(testTap.dateTimeUTC, datetimeInitialized)

    def test_tap_init_from_csv(self):
        csvData = [1, '22-01-2018 13:00:00', "ON", "Stop1", "Company1", "Bus1", "5500005555555559"]
        testTap = Tap.fromArray(csvData)

        self.assertTrue(isinstance(testTap, Tap))
        self.assertEqual(testTap.tapType, "ON")
        self.assertEqual(testTap.stopId, "Stop1")
        self.assertEqual(testTap.companyId, "Company1")
        self.assertEqual(testTap.busId, "Bus1")
        self.assertEqual(testTap.PAN, "5500005555555559")
        self.assertEqual(testTap.id, 1)

        # Check the datetime var while we are here
        self.assertTrue(isinstance(testTap.dateTimeUTC, datetime))

        datetimeInitialized = datetime.strptime('22-01-2018 13:00:00', DATETIME_FORMAT)
        self.assertEqual(testTap.dateTimeUTC, datetimeInitialized)


class TestTrip(unittest.TestCase):

    # Money tests
    def test_trip_complete_fare_1_to_2(self):
        firstStop = Tap(1, '22-01-2018 13:00:00', "ON", "Stop1", "Company1", "Bus1", "5500005555555559")
        secondStop = Tap(2, '22-01-2018 13:30:00', "ON", "Stop2", "Company1", "Bus1", "5500005555555559")
        testTrip = Trip(firstStop, secondStop)

        self.assertEqual(testTrip.calculateFare(), 3.25)
        self.assertTrue(testTrip.isComplete())

    def test_trip_complete_fare_2_to_3(self):
        firstStop = Tap(1, '22-01-2018 13:00:00', "ON", "Stop2", "Company1", "Bus1", "5500005555555559")
        secondStop = Tap(2, '22-01-2018 13:30:00', "ON", "Stop3", "Company1", "Bus1", "5500005555555559")
        testTrip = Trip(firstStop, secondStop)

        self.assertEqual(testTrip.calculateFare(), 5.5)
        self.assertTrue(testTrip.isComplete())

    def test_trip_complete_fare_1_to_3(self):
        firstStop = Tap(1, '22-01-2018 13:00:00', "ON", "Stop1", "Company1", "Bus1", "5500005555555559")
        secondStop = Tap(2, '22-01-2018 13:30:00', "ON", "Stop3", "Company1", "Bus1", "5500005555555559")
        testTrip = Trip(firstStop, secondStop)

        self.assertEqual(testTrip.calculateFare(), 7.3)
        self.assertTrue(testTrip.isComplete())

    def test_trip_cancelled_fare_is_zero_dollars(self):
        firstStop = Tap(1, '22-01-2018 13:00:00', "ON", "Stop1", "Company1", "Bus1", "5500005555555559")
        secondStop = Tap(2, '22-01-2018 13:30:00', "ON", "Stop1", "Company1", "Bus1", "5500005555555559")
        testTrip = Trip(firstStop, secondStop)

        self.assertEqual(testTrip.calculateFare(), 0)
        self.assertTrue(testTrip.isCancelled())

    def test_trip_incomplete_fare_stop_1_is_max_dollars(self):
        firstStop = Tap(1, '22-01-2018 13:00:00', "ON", "Stop1", "Company1", "Bus1", "5500005555555559")
        testTrip = Trip(firstStop)

        self.assertEqual(testTrip.calculateFare(), 7.3)

    def test_trip_incomplete_fare_stop_3_is_max_dollars(self):
        firstStop = Tap(1, '22-01-2018 13:00:00', "ON", "Stop3", "Company1", "Bus1", "5500005555555559")
        testTrip = Trip(firstStop)

        self.assertEqual(testTrip.calculateFare(), 7.3)

    def test_trip_incomplete_fare_stop_2_is_correct_dollars(self):
        firstStop = Tap(1, '22-01-2018 13:00:00', "ON", "Stop2", "Company1", "Bus1", "5500005555555559")
        testTrip = Trip(firstStop)

        self.assertEqual(testTrip.calculateFare(), 5.5)

    # Time tests
    def test_trip_time_taken(self):
        firstStop = Tap(1, '22-01-2018 13:00:00', "ON", "Stop1", "Company1", "Bus1", "5500005555555559")
        secondStop = Tap(2, '22-01-2018 13:30:12', "ON", "Stop2", "Company1", "Bus1", "5500005555555559")
        testTrip = Trip(firstStop, secondStop)

        self.assertEqual(testTrip.getTimeTakenInSeconds(), 1812)

    # Helper tests
    def test_trip_is_fare_complete(self):
        firstStop = Tap(1, '22-01-2018 13:00:00', "ON", "Stop1", "Company1", "Bus1", "5500005555555559")
        secondStop = Tap(2, '22-01-2018 13:30:00', "OFF", "Stop2", "Company1", "Bus1", "5500005555555559")
        testTrip = Trip(firstStop, secondStop)

        self.assertTrue(testTrip.isComplete())

    def test_trip_is_fare_complete_invalid(self):
        firstStop = Tap(1, '22-01-2018 13:00:00', "ON", "Stop1", "Company1", "Bus1", "5500005555555559")
        testTrip = Trip(firstStop)

        self.assertFalse(testTrip.isComplete())

    def test_trip_is_fare_incomplete_invalid(self):
        firstStop = Tap(1, '22-01-2018 13:00:00', "ON", "Stop1", "Company1", "Bus1", "5500005555555559")
        secondStop = Tap(2, '22-01-2018 13:30:00', "OFF", "Stop2", "Company1", "Bus1", "5500005555555559")
        testTrip = Trip(firstStop, secondStop)

        self.assertFalse(testTrip.isIncomplete())

    def test_trip_is_fare_incomplete(self):
        firstStop = Tap(1, '22-01-2018 13:00:00', "ON", "Stop1", "Company1", "Bus1", "5500005555555559")
        testTrip = Trip(firstStop)

        self.assertFalse(testTrip.isComplete())


    def test_trip_is_fare_cancelled_invalid(self):
        firstStop = Tap(1, '22-01-2018 13:00:00', "ON", "Stop1", "Company1", "Bus1", "5500005555555559")
        secondStop = Tap(2, '22-01-2018 13:30:00', "OFF", "Stop2", "Company1", "Bus1", "5500005555555559")
        testTrip = Trip(firstStop, secondStop)

        self.assertFalse(testTrip.isCancelled())

    def test_trip_is_fare_cancelled(self):
        firstStop = Tap(1, '22-01-2018 13:00:00', "ON", "Stop1", "Company1", "Bus1", "5500005555555559")
        secondStop = Tap(2, '22-01-2018 13:30:00', "OFF", "Stop1", "Company1", "Bus1", "5500005555555559")
        testTrip = Trip(firstStop, secondStop)

        self.assertTrue(testTrip.isCancelled())

