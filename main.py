
from datetime import datetime
from datetime import date

class CalendarEvent:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.description = None
        self.location = None
        self.title = None

def getTodayEvents(eventList):
    todayList = []
    today = date.today()
    for event in eventList:
        if event.start_time.date() == today:
            todayList.append(event)
    return todayList

def printEvents(eventList):
    for event in eventList:
        print(f"Title: {event.title}")
        print(f"Start Time: {event.start_time}")
        print(f"End Time: {event.end_time}")
        print(f"Location: {event.location}")
        print(f"Description: {event.description}")
        print("-" * 40)


def parseDateTime(dateString):
    dt = datetime.strptime(dateString, "%Y%m%dT%H%M%S")
    return dt

def parse_ics(file):
    eventList = []
    isNewEvent = False
    for line in file:
        if line.startswith("BEGIN:VEVENT") and not isNewEvent:
            isNewEvent = True
            event = CalendarEvent()
        if line.startswith("DTSTART;TZID") and isNewEvent:
            event.start_time = parseDateTime(line.split(":")[1].strip())
        if line.startswith("DTEND;TZID") and isNewEvent:
            event.end_time = parseDateTime(line.split(":")[1].strip())
        if line.startswith("LOCATION") and isNewEvent:
            event.location = line.split(":")[1].strip()
        if line.startswith("DESCRIPTION") and isNewEvent:
            event.description = line.split(":")[1].strip()
        if line.startswith("SUMMARY") and isNewEvent:
            event.title = line.split(":")[1].strip()
        if line.startswith("END:VEVENT") and isNewEvent:
            isNewEvent = False
            eventList.append(event)
    return eventList

                
        

def main():
    calendar = open("calendar.ics", "r")
    eventList = parse_ics(calendar)
    calendar.close()
    today = getTodayEvents(eventList)
    printEvents(today)
    


if __name__ == "__main__":
    main()