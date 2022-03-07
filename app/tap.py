from datetime import datetime

from app.exceptions import AppException

# Format of the expected dates in input.csv
DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"

class Tap:
    def __init__(self, id, dateTimeUTC, tapType, stopId, companyId, busId, PAN):
        self.PAN = PAN
        self.busId = busId
        self.companyId = companyId
        self.stopId = stopId
        self.tapType = tapType

        # Handles whether a mere string is passed, or an actual datetime object - both work.
        if isinstance(dateTimeUTC, datetime):
            self.dateTimeUTC = dateTimeUTC
        else:
            self.dateTimeUTC = datetime.strptime(dateTimeUTC, DATETIME_FORMAT)

        self.id = id

    # Used for parsing an array of parameters, instead of individual arguments - good for taking array inputs from CSV
    # Assuming all data is correct and perfect - which our spec says it is!
    @classmethod
    def fromArray(cls, array):
        try:
            id = array[0]
            dateTimeUTC = array[1]
            tapType = array[2]
            stopId = array[3]
            companyId = array[4]
            busID = array[5]
            PAN = array[6]
        except IndexError as e:  # Something wasn't formatted correctly - catch it, and re-package in our exception
            print("Something went wrong here...the spec said it would be fine tho :'( ")
            raise AppException(e)

        return cls(id, dateTimeUTC, tapType, stopId, companyId, busID, PAN)