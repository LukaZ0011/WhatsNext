
from datetime import datetime
from datetime import date
from datetime import timedelta
import copy

class CalendarEvent:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.description = None
        self.location = None
        self.title = None
        self.rrule = None

def expandRecurringEvent(e):
    varFREQ = None
    varWKST = None
    varINTERVAL = 1
    varBYDAY = None
    varUNTIL = None
    
    #parse the rrule
    rrule = e.rrule.split(";")
    for part in rrule:
        if "FREQ" in part:
            varFREQ = part.split("=")[1].strip()
        if "WKST" in part:
            varWKST = part.split("=")[1].strip()
        if "INTERVAL" in part:
            varINTERVAL = int(part.split("=")[1].strip())
        if "BYDAY" in part:
            varBYDAY = part.split("=")[1].strip()
        if "UNTIL" in part:
            varUNTIL = parseDateTime(part.split("=")[1].strip())
    
    #skip dates that match the original start_time    
    if varUNTIL <= e.start_time:
            return [e]
    elif varUNTIL is None:
        varUNTIL = e.start_time

    recurringEvents = []
    
    current_start = e.start_time
    current_end = e.end_time
    
    #generate the events based on frequency / interval
    while current_start <= varUNTIL:
        recurrance = copy.deepcopy(e)
        recurrance.start_time = current_start
        recurrance.end_time = current_end
        recurringEvents.append(recurrance)
        if varFREQ == "WEEKLY":
            current_start += timedelta(weeks=varINTERVAL)
            current_end += timedelta(weeks=varINTERVAL)
        elif varFREQ == "DAILY":
            current_start += timedelta(days=varINTERVAL)
            current_end += timedelta(days=varINTERVAL)
            

    return recurringEvents

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
        print(f"RRule: {event.rrule}")
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
        if line.startswith("RRULE") and isNewEvent:
            event.rrule = line.split(":")[1].strip()
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
            if event.rrule:
                eventList.extend(expandRecurringEvent(event))
            else:
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