import csv

from app.tap import Tap
from app.trip import Trip
from app.exceptions import AppException

OUTPUT_HEADERS = ['Started', 'Finished', 'DurationSecs', 'FromStopId', 'ToStopId', 'ChargeAmount', 'CompanyId', 'BusID', 'PAN', 'Status']


def getTapsFromCsv(filename):
    with open(filename) as file:
        csv_reader = csv.reader(file, delimiter=',')
        taps = []
        header_passed = False
        for row in csv_reader:
            if not header_passed:  # Ignore the header line - we're assuming data is all fine and nothing is missing.
                header_passed = True
            else:
                row = [col.strip() for col in row]  # Strip all leading/trailing whitespaces from input
                newTap = Tap.fromArray(row)
                taps.append(newTap)

        # We can't assume that all taps will have been in order...maybe these were from some queue, maybe it was from a
        # multiple databases; some may have been processed earlier or later. Sort everything based on time just in case.
        taps.sort(key=lambda x: x.dateTimeUTC)

        return taps


def writeTripsToCsv(trips, outputFilename):
    with open(outputFilename, mode='w') as file:
        file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Write the headers first
        file_writer.writerow(OUTPUT_HEADERS)

        for trip in trips:
            file_writer.writerow(trip.formatForCsv())


# From an array of Taps, convert them all into Trip entities
def getTripsFromTaps(taps):
    trips = []
    for tap in taps:
        # Has the user got a pending incomplete trip that fits this tap?
        existingTrip = next(filter(lambda x: x.isTapPartOfTrip(tap), trips), None)  # magic one liner for python nerds

        try:
            # If we found an incomplete trip that matches, add it to this one
            if existingTrip is not None:
                existingTrip.addTap(tap)
            # Else, create a new trip and add it to the list
            else:
                newTrip = Trip()
                newTrip.addTap(tap)
                trips.append(newTrip)
        except AppException as e:
            print(f"Can't add tap ID {tap.id} due to {e}, skipping...")

    return trips


def processEverything(inputFilename="input.csv", outputFilename="trips.csv"):
    # Import all the taps
    taps = getTapsFromCsv(inputFilename)

    # ...and process taps into trips
    trips = getTripsFromTaps(taps)

    # Export all trips to the output filename
    writeTripsToCsv(trips, outputFilename)


def main():
    try:
        processEverything()
    except AppException as e:
        print(f"Something went wrong: {e}")


if __name__ == "__main__":
    main()
