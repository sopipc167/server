from googlecalendar import get_calendar

calendar = get_calendar()
events = calendar.get_monthly_events(year=2022, month=9)

print(events)
