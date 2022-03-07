from app.exceptions import AppException, ValidationException
from app.enums import TapType, TripStatus


class Trip:
    # STOP ID's - hardcoded for now.
    STOPS = ["Stop1", "Stop2", "Stop3"]

    # 2D Matrix representing the costs for heading from one stop to another.
    # Can be indexed directly (like STOP_COSTS[stop1][stop3]) to find the cost of travelling from
    # stop 1 to stop 3. Fake graph theory, but it works :D
    STOP_COSTS = {
        STOPS[0]: {STOPS[0]: 0, STOPS[1]: 3.25, STOPS[2]: 7.30},
        STOPS[1]: {STOPS[0]: 3.25, STOPS[1]: 0, STOPS[2]: 5.50},
        STOPS[2]: {STOPS[0]: 7.30, STOPS[1]: 5.50, STOPS[2]: 0}
    }

    def __init__(self, startTap=None, endTap=None):
        self.startTap = startTap
        self.endTap = endTap

    # These getter functions are just safer ways of accessing the vars.
    # All of these variables will
    def getCompanyId(self):
        if self.startTap is not None:
            return self.startTap.companyId
        return None

    def getBusId(self):
        if self.startTap is not None:
            return self.startTap.busId
        return None

    def getPAN(self):
        if self.startTap is not None:
            return self.startTap.PAN
        return None

    def getDatetime(self):
        if self.startTap is not None:
            return self.startTap.dateTimeUTC
        return None

    def getStatus(self):
        if self.isComplete():
            if self.isCancelled():
                return TripStatus.CANCELLED
            else:
                return TripStatus.COMPLETE
        else:
            return TripStatus.INCOMPLETE

    def getTimeTakenInSeconds(self):
        if self.isComplete():
            return (self.endTap.dateTimeUTC - self.startTap.dateTimeUTC).seconds
        return None

    # Add a tap to the trip - contains in-built validation to make sure the tap is a part of this trip, E.G
    # can't add taps to a completed trip, can't tap OFF when not tapped ON, etc
    def addTap(self, tap):
        self.__validateTap(tap)
        if self.startTap is None:
            self.startTap = tap
        else:
            self.endTap = tap

    def __validateTap(self, tap):
        if self.isComplete():
            raise ValidationException("Can't add more taps to a completed trip.")

        if self.startTap is not None and not self.isTapPartOfTrip(tap):
            raise ValidationException("This tap is not a part of this trip.")

        # Add the tap
        if tap.tapType == TapType.ON.name:
            if self.startTap is None:
                return True
            else:
                raise ValidationException("Can't have more than one ON tap.")

        elif tap.tapType == TapType.OFF.name:
            if self.getDatetime() is not None and not tap.dateTimeUTC.date() == self.getDatetime().date():
                raise ValidationException("Can't add an OFF tap to a trip for another day.")

            if self.startTap is None:
                raise ValidationException("Can't add an OFF tap to a trip that doesn't have an ON tap")

            if self.endTap is None:
                return True
            else:
                raise ValidationException("Can't have more than one OFF tap.")
        else:
            raise ValidationException(f'{tap.tapType} is not a valid tap type.')

    # A completed trip has two taps - one on, and one off
    def isComplete(self):
        return self.startTap is not None and self.endTap is not None

    # A cancelled trip starts and finishes at the same place
    def isCancelled(self):
        if self.startTap is not None and self.endTap is not None:
            return self.startTap.stopId == self.endTap.stopId
        return False

    # An incomplete trip only has a Tap on event
    def isIncomplete(self):
        if self.startTap is not None and self.endTap is None:
            return True
        return False

    # Lots of work here.
    # NOTE - Each company would have it's own fee structure - for the moment it will process it the same way for each
    # company regardless, but perhaps in future this would not be hardcoded. Maybe in some generic company interface?
    def calculateFare(self):
        # Longer trips get the maximum possible distance applied - we find that by looking at that stop's row
        # entry in the matrix, and figuring out what the most expensive possible route they could have taken was.
        if self.isIncomplete():
            return max(self.STOP_COSTS[self.startTap.stopId].values())

        return self.STOP_COSTS[self.startTap.stopId][self.endTap.stopId]

    # Logic for determining if a tap can be attributed to be the same trip
    def isTapPartOfTrip(self, tap):
        if self.startTap is None:
            raise AppException("Trip has no taps to compare.")

        return (
                    self.getBusId() == tap.busId and
                    self.getPAN() == tap.PAN and
                    self.getCompanyId() == tap.companyId and
                    self.startTap.dateTimeUTC < tap.dateTimeUTC and
                    not self.isComplete()
                )

    def formatForCsv(self):
        if self.startTap is None:
            raise AppException("No taps in this trip!")

        # There can be incomplete taps - account for this when getting data by figuring out if the
        # trip is complete or not
        if not self.isIncomplete():
            endTime = self.endTap.dateTimeUTC
            timeTaken = self.getTimeTakenInSeconds()
            lastStopId = self.endTap.stopId

        # Else: everything is None!
        else:
            endTime = None
            timeTaken = None
            lastStopId = None

        # Now to return the array!
        return [
            self.startTap.dateTimeUTC,
            endTime,  # End Time of Trip || CAN BE NONE
            timeTaken,  # Time delta in seconds for the duration of the trip || CAN BE NONE
            self.startTap.stopId,
            lastStopId,  # Last Stop ID || CAN BE NONE
            "{:.2f}".format(self.calculateFare()),
            self.getCompanyId(),
            self.getBusId(),
            self.getPAN(),
            self.getStatus().name
        ]