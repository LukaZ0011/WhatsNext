
class CalendarEvent:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.description = None
        self.location = None
        self.title = None

def parseDateTime(dateString):
    

def parse_ics(file):
    eventList = []
    isNewEvent = False
    for line in file:
        if line.startswith("BEGIN:VEVENT") and not isNewEvent:
            isNewEvent = True
            event = CalendarEvent()
        if line.startswith("DTSTART;TZID") and isNewEvent:
            
        elif line.startswith("END:VEVENT") and isNewEvent:
            isNewEvent = False

                
        

def main():
    calendar = open("calendar.ics", "r")
    parse_ics(calendar)
    calendar.close()
    event = CalendarEvent()


if __name__ == "__main__":
    main()