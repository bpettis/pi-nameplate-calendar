from icalendar import Calendar
from datetime import datetime, timezone, timedelta, time
from dateutil.rrule import rrulestr
from dotenv import load_dotenv
import requests, os
import tzlocal

load_dotenv()
CALENDAR_URL = os.getenv("CALENDAR_URL", None)
ICS_FILE = os.getenv("ICS_FILE", "calendar.ics")
BUSINESS_START = time(9, 30)
BUSINESS_END = time(16, 30)

local_tz = tzlocal.get_localzone()


def find_free_windows(cal, now, days_ahead=14, min_duration=timedelta(minutes=55)):
    """Find next 3 free windows within business hours."""
    
    business_start = BUSINESS_START
    business_end = BUSINESS_END

    window_start = now
    window_end = now + timedelta(days=days_ahead)

    busy_periods = []

    # 1. Collect all event occurrences
    for component in cal.walk():
        if component.name != "VEVENT":
            continue

        for start, end in get_occurrences(component, window_start, window_end):
            busy_periods.append((start, end))

    # 2. Sort events
    busy_periods.sort()

    free_windows = []

    current_day = now.date()

    while len(free_windows) < 3 and current_day <= window_end.date():
        day_start = datetime.combine(current_day, business_start, tzinfo=local_tz)
        day_end = datetime.combine(current_day, business_end, tzinfo=local_tz)

        # Don't consider time before "now" on current day
        if current_day == now.date():
            day_start = max(day_start, now)

        # Skip if we're already past business hours
        if day_start >= day_end:
            current_day += timedelta(days=1)
            continue

        # 3. Filter busy periods for this day
        day_busy = []
        for start, end in busy_periods:
            if end <= day_start or start >= day_end:
                continue

            # Clip to business hours
            s = max(start, day_start)
            e = min(end, day_end)
            day_busy.append((s, e))

        # 4. Merge overlapping busy periods
        day_busy.sort()
        merged = []

        for period in day_busy:
            if not merged:
                merged.append(period)
            else:
                last_start, last_end = merged[-1]
                cur_start, cur_end = period

                if cur_start <= last_end:
                    merged[-1] = (last_start, max(last_end, cur_end))
                else:
                    merged.append(period)

        # 5. Find gaps
        cursor = day_start

        for start, end in merged:
            if start > cursor:
                gap = (cursor, start)
                if gap[1] - gap[0] >= min_duration:
                    free_windows.append(gap)
                    if len(free_windows) == 3:
                        return free_windows

            cursor = max(cursor, end)

        # Gap after last event
        if cursor < day_end:
            gap = (cursor, day_end)
            if gap[1] - gap[0] >= min_duration:
                free_windows.append(gap)
                if len(free_windows) == 3:
                    return free_windows

        current_day += timedelta(days=1)

    return free_windows


def format_time(dt):
    """Format time like '3 PM' or '3:30 PM'."""
    if dt.minute == 0:
        return dt.strftime("%-I %p")
    return dt.strftime("%-I:%M %p")


def format_window(start, end, now):
    """Return friendly string like 'Today (6/29) 3–4:30 PM'."""
    # Month/day format (no leading zeros)
    date_str = start.strftime("%-m/%-d")

    if start.date() == now.date():
        day_label = f"Today ({date_str})"
    elif start.date() == (now + timedelta(days=1)).date():
        day_label = f"Tomorrow ({date_str})"
    else:
        day_label = f"{start.strftime('%A')} ({date_str})"

    start_str = format_time(start)
    end_str = format_time(end)

    return f"{day_label} {start_str}–{end_str}"


def normalize_dt(dt):
    """Convert date/datetime to timezone-aware datetime in local timezone."""
    if isinstance(dt, datetime):
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = datetime(dt.year, dt.month, dt.day, tzinfo=timezone.utc)

    return dt.astimezone(local_tz)


def get_duration(component, start):
    """Determine event duration."""
    end_prop = component.get("dtend")

    if end_prop:
        end = normalize_dt(end_prop.dt)
        return end - start

    # fallback duration
    return timedelta(hours=1)



def build_rrule(component, start):
    """Convert RRULE field into dateutil rule (robust)."""
    rrule_field = component.get("rrule")
    if not rrule_field:
        return None

    # Proper RFC-compliant RRULE string
    rule_bytes = rrule_field.to_ical()
    rule_str = rule_bytes.decode()

    return rrulestr(rule_str, dtstart=start)



def get_exdates(component):
    """Get excluded dates."""
    excluded = set()
    exdates = component.get("exdate")

    if exdates:
        for ex in exdates.dts:
            excluded.add(normalize_dt(ex.dt))

    return excluded


def get_rdates(component):
    """Get additional recurrence dates."""
    dates = []
    rdates = component.get("rdate")

    if rdates:
        for r in rdates.dts:
            dates.append(normalize_dt(r.dt))

    return dates


def get_occurrences(component, window_start, window_end):
    """Yield event occurrences within window."""
    start = normalize_dt(component.get("dtstart").dt)
    duration = get_duration(component, start)

    rule = build_rrule(component, start)


    
    excluded = get_exdates(component)

    # Non-recurring event
    if not rule:
        yield (start, start + duration)
    else:
        for occ_start in rule.between(window_start, window_end, inc=True):
            occ_start = occ_start.astimezone(local_tz)

            if occ_start in excluded:
                continue

            yield (occ_start, occ_start + duration)

    # Add RDATE occurrences
    for extra_start in get_rdates(component):
        if window_start <= extra_start <= window_end:
            yield (extra_start, extra_start + duration)




def main():
    # Load calendar
    with open(ICS_FILE, "rb") as f:
        cal = Calendar.from_ical(f.read())

    now = datetime.now(local_tz)

    # Limit recurrence expansion window (important!)
    window_start = now - timedelta(days=1)
    window_end = now + timedelta(days=1)

    current_events = []

    # Iterate VEVENTS
    for component in cal.walk():
        if component.name != "VEVENT":
            continue

        for start, end in get_occurrences(component, window_start, window_end):
            if start <= now <= end:
                current_events.append((component, start, end))

    # Sort by start time
    current_events.sort(key=lambda x: x[1])

    # Output
    if current_events:
        print("Current events:\n")
        for event, start, end in current_events:
            print("Summary:", event.get("summary"))
            print("Start:", start)
            print("End:", end)
            print("Location:", event.get("location"))
            print("-" * 40)
    else:
        print("No events are currently in progress.")


    
    print("\nNext available time windows:\n")

    free_windows = find_free_windows(cal, now, days_ahead=14, min_duration=timedelta(minutes=30))

    if free_windows:
        for start, end in free_windows:
            print(format_window(start, end, now))
    else:
        print("No suitable free windows found.")



if __name__ == "__main__":
    main()